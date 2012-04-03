from collections import defaultdict
import logging
import cv
import cv2
import numpy
from numpy.core.numeric import array
from numpy.matlib import zeros
import operator

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
    DESCRIPTOR_SIZE = 64

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
        surf = cv2.SURF(_hessianThreshold=300)
        numpy.seterr(all="raise")
        for slide in slides.values():
            logger.debug("Extracting from %s..." % slide.image_path)
            image = cv2.imread(slide.image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            keypoints, descriptors = surf.detect(image, None, False)
            # Reshape descriptors so they'll make sense
            descriptors.shape = (-1, surf.descriptorSize())
            slide.keypoints = keypoints
            slide.descriptors = descriptors

    def _calculate_distance_matrix(self):
        mapping, flann_index = self._get_flann_index(self.image_slides)

        results = []
        for v_time, v_slide in self.video_slides.items():
            # Use FLANN detector to find nearest neighbours
            neighbours = self._get_nearest_neighbours_flann(flann_index, v_slide.descriptors, -1)

            counts = defaultdict(int)
            for neighbour in neighbours:
                counts[mapping[neighbour[1]]] += 1
            list = [(val, self.image_slides[idx].image_path) for idx, val in counts.items()]
            results.append((v_slide.image_path, sorted(list)))

        for result in sorted(results):
            print result


    def _get_flann_index(self, images):
        descriptors = tuple([image.descriptors for i_num, image in images.items()])
        # Stack descriptors together
        stack = numpy.vstack(descriptors)

        mapping = {}
        idx = 0
        for i_num, image in images.items():
            for i in range(0, len(image.descriptors)):
                mapping[idx] = i_num
                idx += 1

        flann = cv2.flann_Index(features=stack, params=dict(algorithm = 1, trees = 4))
        return mapping, flann

    def _get_nearest_neighbours_flann(self, index, descriptors, treshold = 0.6):
        # Build index
        indexes, distances = index.knnSearch(descriptors, 2, params={})    # Find 2 nearest neighbours
        indexes1 = numpy.arange(len(descriptors))                          # Prepare indexes for zip
        pairs = zip(indexes1, indexes[:, 0], distances[:, 0], distances[:,0] / (distances[:,1] + numpy.finfo(float).eps)) # Build pairs of indexes with first neighbour with distance
        return filter(lambda item: item[3] > treshold, pairs)