import Queue
from cv2 import cv
import logging
import os
import tempfile
from threading import Thread

logger = logging.getLogger(__name__)

class VideoProcessor(Thread):
    frame_queue = Queue.Queue(maxsize=100)
    done = False

    def __init__(self, video):
        Thread.__init__(self)
        self._video = video

    def run(self):
        timestamp = -1
        while timestamp is not None:
            timestamp, frame = self._video.get_next_frame()
            self.frame_queue.put((timestamp, frame,))
        self.done = True

class ImageSave(Thread):
    image_queue = Queue.Queue()
    done = False

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            try:
                image_path, image = self.image_queue.get(timeout=2)
                cv.SaveImage(image_path, image)
            except Queue.Empty:
                pass

            if self.done:
                return

class SlideExtractor(object):
    SKIP_COUNT = 50
    _treshold = 10

    def __init__(self, video_file, cropbox=None, callback=None, grayscale=False, treshold=10):
        self._video_file = video_file
        self._callback = callback
        self._cropbox = cropbox
        self._treshold = treshold

        if grayscale:
            self._channels = 1
        else:
            self._channels = 3

    def extract_slides(self):
        self.tmp_dir = self._create_temp_dir()
        self._video_file.seek_to(1.0)

        if self._cropbox is not None:
            x, y, width, height = self._cropbox
        else:
            x = 0
            y = 0
            width = self._video_file.info.width
            height = self._video_file.info.height

        pixel_count = width * height * self._channels
        current_frame = None
        timestamp = None
        frame = None

        slides = []

        video_thread = VideoProcessor(self._video_file)
        video_thread.setDaemon(True)
        video_thread.start()

        image_save_thread = ImageSave()
        image_save_thread.setDaemon(True)
        image_save_thread.start()

        while not video_thread.done:
            for i in range(0, self.SKIP_COUNT):
                if video_thread.done:
                    break

                try:
                    timestamp, frame = video_thread.frame_queue.get(timeout=5)
                except Queue.Empty:
                    break

            if video_thread.done:
                logger.info("Extraction done!")
                break

            assert frame.format == "RGB"
            # Crop frame if possible
            region = frame.get_region(x, y, width, height)
            cv_frame = cv.CreateImage((width, height), cv.IPL_DEPTH_8U, 3)      # Allocate image
            cv.SetData(cv_frame, region.get_data("RGB", width * 3), width * 3)  # Set data from frame
            cv.Smooth(cv_frame, cv_frame, smoothtype=cv.CV_GAUSSIAN, param1=7)
            if self._channels == 1:     # Grayscale
                gray_frame = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, 1)
                cv.CvtColor(cv_frame, gray_frame, cv.CV_RGB2GRAY)
                self._fix_contrast(gray_frame)
                cv.Threshold(gray_frame, gray_frame, 50, 255, cv.CV_THRESH_BINARY)
                cv_frame = gray_frame
            else:
                r = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, 1)
                g = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, 1)
                b = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, 1)
                cv.Split(cv_frame, r, g, b, None)
                self._fix_contrast(r)
                self._fix_contrast(g)
                self._fix_contrast(b)
                cv.Merge(b, g, r, None, cv_frame)

            if current_frame is None:
                difference = 2**30      # Make sure to grab first frame
            else:
                # Calculate image diff
                diff = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, self._channels)
                cv.AbsDiff(current_frame, cv_frame, diff)
                difference = sum(cv.Sum(diff)) / pixel_count        # Normalize difference with pixel count

            if difference > self._treshold:
                # Save frame to disk
                cv_original_frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 3)
                cv.SetData(cv_original_frame, frame.data, frame.width * 3)
                cv.CvtColor(cv_original_frame, cv_original_frame, cv.CV_RGB2BGR)
                filepath = os.path.join(self.tmp_dir, "%s (%s).png" % (timestamp, difference,))
                image_save_thread.image_queue.put((filepath, cv_original_frame))
                slides.append((timestamp, filepath))

            self._send_callback(timestamp)
            current_frame = cv_frame

        image_save_thread.done = True
        return slides

    def _create_temp_dir(self):
        try:
            return tempfile.mkdtemp(prefix="sync-")
        except IOError:
            logger.warning("Failed to create temporary directory for slide extraction!")
        except OSError as e:
            logger.error(e)

    def _send_callback(self, timestamp):
        if self._callback is not None:
            self._callback(timestamp, max=self._video_file.get_info().duration)

    def _fix_contrast(self, image):
        minval, maxval, minloc, maxloc = cv.MinMaxLoc(image)
        range = maxval - minval
        range_factor = 255.0 * (1.0 / range)
        cv.SubS(image, minval, image)
        cv.Scale(image, image, scale=range_factor)
