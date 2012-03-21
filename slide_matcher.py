import logging

logger = logging.getLogger(__name__)

class Slide(object):
    timing = None
    image_path = None
    descriptors = None

    def __init__(self, timing, image_path):
        self.timing = timing
        self.image_path = image_path

    def __hash__(self):
        return self.timing.__hash__()

    def __eq__(self, other):
        return self.timing.__eq__(other)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "-%s- [%s]" % (self.timing, self.image_path)


class SlideMatcher(object):
    video_slides = {}
    image_slides = {}

    def __init__(self, video_slides, image_slides):

        for video_slide in video_slides:
            time, path = video_slide
            self.video_slides[time] = Slide(time, path)

        for image_slide in image_slides:
            time, path = image_slide
            self.image_slides[time] = Slide(time, path)

    def match_slides(self):
        logger.debug(self.image_slides)
        logger.debug(self.video_slides)
