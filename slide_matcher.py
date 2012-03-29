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
        surf = cv2.SURF(_hessianThreshold=3500, _extended=True)
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
        candidates = []

        for v_time, v_slide in self.video_slides.items():
            distances = []
            for i_num, i_slide in self.image_slides.items():
                # Use FLANN detector to find nearest neighbours
                neighbours = self._get_nearest_neighbours_flann(v_slide.descriptors, i_slide.descriptors, 0.9)
                score = len(neighbours)
                distances.append((score, i_slide.image_path))

            distances = sorted(distances)
            candidates.append((v_slide.image_path, distances[-1][1], distances))

        for cnd in sorted(candidates):
            print cnd

    def _get_nearest_neighbours_flann(self, descriptors1, descriptors2, treshold = 0.6):
        # Build index
        flann = cv2.flann_Index(features=descriptors2, params=dict(algorithm = 1, trees = 4))  # FLANN_INDEX_KDTREE = 1
        indexes2, distances = flann.knnSearch(descriptors1, 2, params={})    # Find 2 nearest neighbours
        indexes1 = numpy.arange(len(descriptors1))                          # Prepare indexes for zip
        pairs = zip(indexes1, indexes2[:, 0], distances[:, 0], distances[:,0] / distances[:,1]) # Build pairs of indexes with first neighbour with distance
        return filter(lambda item: item[3] > treshold, pairs)