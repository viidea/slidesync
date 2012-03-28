import logging
import cv
import numpy
from numpy.core.numeric import array
from numpy.matlib import zeros

logger = logging.getLogger(__name__)

class Slide(object):
    timing = None
    image_path = None
    keypoints = None
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
        logger.info("Extracting features from video slides...")
        self._extract_features(self.video_slides)
        logger.info("Extracting features from image slides...")
        self._extract_features(self.image_slides)
        logger.info("Calculating distance matrix...")
        self._calculate_distance_matrix()

    def _extract_features(self, slides):
        for slide in slides.values():
            logger.debug("Extracting from %s..." % slide.image_path)
            image = cv.LoadImageM(slide.image_path, iscolor=cv.CV_LOAD_IMAGE_GRAYSCALE)
            keypoints, descriptors = cv.ExtractSURF(image, None, cv.CreateMemStorage(), (0, 3000, 3, 1))
            slide.keypoints = keypoints
            slide.descriptors = descriptors

    def _calculate_distance_matrix(self):
        distances = {}
        count = 0
        for i_num, i_slide in self.image_slides.items():
            count += 1
            distances[i_num] = {}
            for v_time, v_slide in self.video_slides.items():
                dst = self._calculate_descriptor_set_distance(v_slide.keypoints, v_slide.descriptors, i_slide.keypoints, i_slide.descriptors)
                if dst is not None:
                    distances[i_num][v_time] = dst

            print distances[i_num]
            logger.debug("%s/%s" % (count, len(self.video_slides)))
        return distances

    def _calculate_descriptor_set_distance(self, v_keypoints, v_descriptors, i_keypoints, i_descriptors):
        distances = []
        # Find matching descriptors and discard non-matching
        for i_d in i_descriptors:
            dst = []
            for v_d in v_descriptors:
                distance = self._get_descriptor_distance(i_d, v_d)
                dst.append(distance)
                if len(dst) > 10:           # We only need to find first two candidates
                    dst = sorted(dst)[:2]

            # Ignore descriptors that don't have enough difference between first and second match - bad matches
            dst = sorted(dst)
            if len(dst) < 2 or dst[0] < dst[1] * 0.6:
                continue

            distances.append(dst[0])

        if len(distances) > 0:
            return len(distances), sum(distances) / len(distances)
        return None

    def _get_descriptor_distance(self, a, b):
        a_arr = numpy.array(a)
        b_arr = numpy.array(b)
        return numpy.linalg.norm(a_arr-b_arr)
