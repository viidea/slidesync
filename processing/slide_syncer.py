import bisect
import logging
from audiosync import utils, sync, correlate

logger = logging.getLogger(__name__)

class SlideSyncer(object):
    def __init__(self, original_video, slide_video, global_method=True):
        self.original_video_file = original_video
        self.slide_video_file = slide_video
        self.global_method = global_method

    def get_synced_timings(self, slide_data):
        logger.debug("Loading files %s and %s" % (self.original_video_file, self.slide_video_file))
        # Load audio files first
        original_audio, original_file_sr = utils.get_audio_from_file(self.original_video_file)
        original_audio, original_sr = sync.preprocess_audio(original_audio, original_file_sr)
        slide_audio, original_slide_sr = utils.get_audio_from_file(self.slide_video_file)
        slide_audio, slide_sr = sync.preprocess_audio(slide_audio, original_slide_sr)
        assert original_file_sr == original_slide_sr

        if self.global_method:
            updated_slides = self._get_synced_timings_global(slide_data, original_audio, slide_audio, slide_sr)
        else:
            updated_slides = self._get_synced_timings_local(slide_data, original_audio, slide_audio, slide_sr)

        assert len(updated_slides) > 0

        if updated_slides[0][0] > 0:
            # Pull down first slide to 0 if all slides are positive
            updated_slides[0] = (0, updated_slides[0][1])
        else:
            # Pull up incoming slide if there are negatively timed slides
            zero_index = bisect.bisect_left([time for time,image in updated_slides], 0)
            assert zero_index > 0
            updated_slides[zero_index - 1] = (0, updated_slides[zero_index - 1][1])

        return updated_slides

    def _get_synced_timings_global(self, slide_data, original_audio, slide_audio, samplerate):
        global_offset, corr = correlate.get_offset(original_audio, slide_audio, samplerate)
        logger.info("Found offset %s", global_offset)

        updated_slides = []
        for slide_time, slide_name in slide_data.items():
            slide_time = slide_time - global_offset
            updated_slides.append((slide_time, slide_name))
        return sorted(updated_slides)

    def _get_synced_timings_local(self, slide_data, original_audio, slide_audio, samplerate):
        raise NotImplementedError("Local timings are not implemented yet")

#        logger.debug("Starting offset calculations...")
#        updated_slides = []
#        count = 0
#        for slide_time, slide_name in slide_data.items():
#            updated_time = sync.find_offset((original_audio, original_sr), (slide_audio, slide_sr), slide_time)
#            print slide_time, "=>", updated_time
#            # Clamp number to duration
#            if updated_time < 0: updated_time = 0.0
#            updated_slides.append((updated_time, slide_name))
#            count += 1
#            logger.debug("%s/%s" % (count, len(slide_data)))