import logging
import cv
import numpy

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
        for v_time, v_slide in self.video_slides.items():
            count += 1
            distances[v_time] = {}
            for i_time, i_slide in self.image_slides.items():
                distances[v_time][i_time] = self._calculate_descriptor_set_distance(v_slide.keypoints, v_slide.descriptors, i_slide.keypoints, i_slide.descriptors)

            print distances[v_time]
            logger.debug("%s/%s" % (count, len(self.video_slides)))
        return distances

    def _calculate_descriptor_set_distance(self, v_keypoints, v_descriptors, i_keypoints, i_descriptors):
        distances = []
        for v in range(0, len(v_descriptors)):
            v_d = v_descriptors[v]
            v_k = v_keypoints[v]
            distances.append(self._get_neighbour_distance(v_k, v_d, i_keypoints, i_descriptors))
        return sum(distances) / len(distances)

    def _get_neighbour_distance(self, v_keypoint, v_descriptor, i_keypoints, i_descriptors):
        assert len(i_keypoints) == len(i_descriptors)
        best = float("inf")

        for i in range(0, len(i_descriptors)):
            if v_keypoint[2] != i_keypoints[i][2]:      # Laplacian
                continue

            dist = self._get_descriptor_distance(v_descriptor, i_descriptors[i])
            if dist < best:
                best = dist

        if best == float("inf"):
            return 0
        else:
            return best

    def _get_descriptor_distance(self, d1, d2):
        assert len(d1) == len(d2)
        vals = []
        for i in range(0, len(d1)):
            num = d1[i] - d2[i]
            num = num*num
            vals.append(num)
        return sum(vals)

