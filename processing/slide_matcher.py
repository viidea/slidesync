import logging
import cv2
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
    DESCRIPTOR_SIZE = 64

    video_slides = {}
    image_slides = {}

    progress_cb = None

    def __init__(self, video_slides, image_slides, progress_cb = None):

        for video_slide in video_slides:
            time, path = video_slide
            self.video_slides[time] = Slide(time, path)

        for image_slide in image_slides:
            time, path = image_slide
            self.image_slides[time] = Slide(time, path)

        numpy.seterr(all="raise")
        self.progress_cb = progress_cb

    def match_slides(self):
        logger.info("Extracting features from video slides...")
        self._extract_features(self.video_slides)
        logger.info("Extracting features from image slides...")
        self._extract_features(self.image_slides)
        logger.info("Calculating distance matrix...")
        if self.progress_cb is not None:
            self.progress_cb(0, 0)
        return self._calculate_distance_matrix()

    def _extract_features(self, slides):
        surf = cv2.SURF(hessianThreshold=80, extended=False)
        #numpy.seterr(all="raise")
        for i in range(0, len(slides.values())):
            slide = slides.values()[i]
            logger.debug("Extracting from %s..." % slide.image_path)
            image = cv2.imread(slide.image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            keypoints, descriptors = surf.detect(image, None, None)
            # Reshape descriptors so they'll make sense
            if not len(descriptors) == 0:
                descriptors.shape = (-1, surf.descriptorSize())
            else:
                # Fake descriptors for empty images
                descriptors = numpy.zeros((1, surf.descriptorSize()), dtype=numpy.float32)
            slide.keypoints = keypoints
            slide.descriptors = descriptors

            if self.progress_cb is not None:
                self.progress_cb(i + 1, max=len(slides.values()))

    def _calculate_distance_matrix(self):
        mapping, flann_index = self._get_flann_index(self.image_slides)

        matches = {}
        for v_time, v_slide in self.video_slides.items():
            # Use FLANN detector to find nearest neighbours
            nearest_image = self._get_nearest_image_flann(flann_index, v_slide.descriptors, -1)
            matches[v_slide.timing] = self.image_slides[nearest_image].timing
        return matches


    def _get_flann_index(self, images):
        flann_params = dict(algorithm = 1,  # FLANN_INDEX_LSH
                           trees = 4)
        matcher = cv2.FlannBasedMatcher(flann_params, {})
        mapping = {}

        logger.debug("Calculating FLANN index for %d images...", len(images))
        for i_num, image in images.items():
            matcher.add([image.descriptors])

        matcher.train()
        return mapping, matcher

    def _get_nearest_image_flann(self, matcher, descriptors, threshold = 0.6):
        matches = matcher.knnMatch(descriptors, 2) # Find descriptor matches
        # Queue all images which have matches with distance difference greater than threshold
        images = [m[0].imgIdx for m in matches if len(m) == 2 and (m[0].distance / m[1].distance) > threshold]
        # Return image index with most occuriences
        return max(set(images), key=images.count)