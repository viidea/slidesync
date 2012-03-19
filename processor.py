from cv2 import cv

class VideoProcessor(object):
    SKIP_COUNT = 25

    def __init__(self, video_file, callback=None):
        self.video_file = video_file
        self.callback = callback

    def start(self):
        while self.video_file.get_frame()[0] is not None:
            for i in range(0, self.SKIP_COUNT):
                timestamp, frame = self.video_file.get_next_frame()

            # Convert frame to openCV
            cv_frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 3)      # Allocate image
            cv.SetData(cv_frame, frame.data, frame.pitch)                                   # Set data from frame
            cv.CvtColor(cv_frame, cv_frame, cv.CV_RGB2BGR)                                  # OpenCV expects BGR, convert
            cv.SaveImage("/tmp/%s.png" % (timestamp,), cv_frame)                            # Test save


