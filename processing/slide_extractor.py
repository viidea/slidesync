import Queue
from cv2 import cv
import logging
import os
import tempfile
from threading import Thread
import numpy

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

            # Flush audio data
            while True:
                audio_frame = self._video.get_audio_data()
                if audio_frame is None or audio_frame.timestamp > timestamp:
                    break

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
                logger.info("Saving %s", image_path)
                cv.SaveImage(image_path, image)
            except Queue.Empty:
                pass

            if self.done:
                return

class SlideExtractor(object):
    FRAME_SKIP = 25

    def __init__(self, video_file, cropbox=None, callback=None, treshold=50):
        self._video_file = video_file
        self._callback = callback
        self._cropbox = cropbox
        self._treshold = treshold

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

        pixel_count = width * height * 3
        current_frame = None

        slides = []
        video_thread = VideoProcessor(self._video_file)
        video_thread.setDaemon(True)
        video_thread.start()

        diff_signal = []
        frame_counter = -1
        while not video_thread.done:
            if video_thread.done:
                break

            try:
                timestamp, frame = video_thread.frame_queue.get(timeout=5)
            except Queue.Empty:
                break

            frame_counter += 1
            if frame_counter % self.FRAME_SKIP != 0:
                continue

            assert frame.format == "RGB"
            # Crop frame if possible
            region = frame.get_region(x, y, width, height)
            cv_frame = cv.CreateImage((width, height), cv.IPL_DEPTH_8U, 3)      # Allocate image
            cv.SetData(cv_frame, region.get_data("RGB", width * 3), width * 3)  # Set data from frame
            cv.Smooth(cv_frame, cv_frame, smoothtype=cv.CV_GAUSSIAN, param1=7)  # Gaussian filter to remove noise

            if current_frame is None:
                difference = 2**30      # Make sure to grab first frame
            else:
                # Calculate image diff
                diff = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, 3)
                cv.AbsDiff(current_frame, cv_frame, diff)
                difference = sum(cv.Sum(diff)) / pixel_count        # Normalize difference with pixel count

            diff_signal.append((frame_counter, difference))
            current_frame = cv_frame
            self._send_callback(timestamp)

        self._send_callback(0)
        peaks_idx = set(_get_diff_peaks([val for _, val in diff_signal]))
        logger.info("Found peaks: %s", peaks_idx)

        # Transform list indexes to frame counter numbers
        peaks = set()
        for idx in peaks_idx:
            peaks.add(diff_signal[idx][0])

        # Save images connected to peaks
        self._video_file.seek_to(1.0)
        video_thread = VideoProcessor(self._video_file)
        video_thread.setDaemon(True)
        video_thread.start()

        image_save_thread = ImageSave()
        image_save_thread.setDaemon(True)
        image_save_thread.start()

        frame_counter = -1
        while not video_thread.done:
            if video_thread.done:
                break

            try:
                timestamp, frame = video_thread.frame_queue.get(timeout=5)
            except Queue.Empty:
                break

            frame_counter += 1
            if frame_counter in peaks:
                cv_frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 3)
                cv.SetData(cv_frame, frame.data, frame.width * 3)
                cv.CvtColor(cv_frame, cv_frame, cv.CV_RGB2BGR)
                filepath = os.path.join(self.tmp_dir, "%s.png" % (timestamp,))
                image_save_thread.image_queue.put((filepath, cv_frame))
                slides.append((timestamp, filepath))

            self._send_callback(timestamp)

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
            if not timestamp:
                self._callback(0, max=0, min=0)
            else:
                self._callback(timestamp, max=self._video_file.get_info().duration)

def _get_diff_peaks(diff_signal):
    if diff_signal[0] == 2**30:
        del diff_signal[0]

    std_dev = numpy.std(diff_signal)
    diff_signal = _smooth(diff_signal, 2)
    # Do tresholding to remove noise
    diff_signal = numpy.where(diff_signal > 0.3 * std_dev, diff_signal, 0)
    peaks = _find_peaks(diff_signal)
    return peaks

def _find_peaks(x):
    peaks = []
    prev_diff = -1

    for i in range(len(x) - 1):
        diff = x[i] - x[i+1]
        if diff > 0 and prev_diff < 0:
            peaks.append(i)

        prev_diff = diff

    return numpy.asarray(peaks)

def _smooth(x,beta):
     """ kaiser window smoothing """
     window_len=5
     # extending the data at beginning and at the end
     # to apply the window at the borders
     s = numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
     w = numpy.kaiser(window_len,beta)
     y = numpy.convolve(w/w.sum(),s,mode='valid')
     return y[2:len(y)-2]