from cv2 import cv
import logging
import os
import tempfile

logger = logging.getLogger(__name__)

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

        while True:
            for i in range(0, self.SKIP_COUNT):
                timestamp, frame = self._video_file.get_next_frame()

            if timestamp is None:
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
                filepath = os.path.join(tmp_dir, "%s (%s).png" % (timestamp, difference,))
                cv.SaveImage(filepath, cv_frame)
                self._send_callback(timestamp)

                slides.append((timestamp, filepath))
            else:
                self._send_callback(timestamp)

            current_frame = cv_frame

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