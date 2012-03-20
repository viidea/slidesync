from cv2 import cv
import logging
import os
import numpy

logger = logging.getLogger(__name__)

class VideoProcessor(object):
    SKIP_COUNT = 50
    TRESHOLD = 4

    def __init__(self, video_file, cropbox=None, callback=None, grayscale=False):
        self._video_file = video_file
        self._callback = callback
        self._cropbox = cropbox

        if grayscale:
            self._channels = 1
        else:
            self._channels = 3

    def _create_temp_dir(self):
        try:
            os.mkdir("/tmp/sync/")
        except IOError:
            logger.error("Failed to create temporary directory for slide extraction!")

    def extract_slides(self):
        self._create_temp_dir()

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

        while True:
            for i in range(0, self.SKIP_COUNT):
                timestamp, frame = self._video_file.get_next_frame()

            if timestamp is None:
                logger.info("Extraction done!")
                break

            assert frame.format == "RGB"
            # Crop frame if possible
            region = frame.get_region(x, y, width, height).get_image_data()
            cv_frame = cv.CreateImage((width, height), cv.IPL_DEPTH_8U, 3)      # Allocate image
            cv.SetData(cv_frame, region.get_data("RGB", width * 3), width * 3)  # Set data from frame

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

            cv.Smooth(cv_frame, cv_frame, smoothtype=cv.CV_GAUSSIAN)

            if current_frame is None:
                current_frame = cv_frame

            # Calculate image diff
            diff = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, self._channels)
            cv.AbsDiff(current_frame, cv_frame, diff)
            difference = sum(cv.Sum(diff)) / pixel_count        # Normalize difference with pixel count

            if difference > self.TRESHOLD:
                # Save frame to disk
                frame.save("/tmp/sync/%s (%s).png" % (timestamp, difference,))
            current_frame = cv_frame

    def _fix_contrast(self, image):
        minval, maxval, minloc, maxloc = cv.MinMaxLoc(image)
        range = maxval - minval
        range_factor = 255.0 * (1.0 / range)
        cv.SubS(image, minval, image)
        cv.Scale(image, image, scale=range_factor)