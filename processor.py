from cv2 import cv

class VideoProcessor(object):
    SKIP_COUNT = 25
    TRESHOLD = 1

    def __init__(self, video_file, callback=None, grayscale=False):
        self.video_file = video_file
        self.callback = callback
        if grayscale:
            self.channels = 1
        else:
            self.channels = 3

    def start(self):
        pixel_count = self.video_file.info.width * self.video_file.info.height * self.channels

        current_frame = None
        timestamp = None
        frame = None
        while True:
            for i in range(0, self.SKIP_COUNT):
                timestamp, frame = self.video_file.get_next_frame()

            if timestamp is None:
                print "Done!"
                break

            assert frame.format == "RGB"

            # Convert frame to openCV
            color_frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 3)      # Allocate image
            cv.SetData(color_frame, frame.data, frame.pitch)                                   # Set data from frame
            cv_frame = cv.CreateImage(cv.GetSize(color_frame), cv.IPL_DEPTH_8U, self.channels) # Converted image

            if self.channels == 1:
                cv.CvtColor(color_frame, cv_frame, cv.CV_RGB2GRAY)
            else:
                cv.CvtColor(color_frame, cv_frame, cv.CV_RGB2BGR)

            if current_frame is None:
                current_frame = cv_frame

            # Calculate image diff
            diff = cv.CreateImage(cv.GetSize(cv_frame), cv.IPL_DEPTH_8U, self.channels)
            cv.AbsDiff(current_frame, cv_frame, diff)
            difference = sum(cv.Sum(diff)) / pixel_count        # Normalize difference with pixel count

            if difference > self.TRESHOLD:
                current_frame = cv_frame
                cv.SaveImage("/tmp/%s.png" % (timestamp,) , cv_frame)

            print difference