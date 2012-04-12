import logging
from audiosync import utils, sync

logger = logging.getLogger(__name__)

class SlideSyncer(object):
    def __init__(self, original_video, slide_video):
        self.original_video_file = original_video
        self.slide_video_file = slide_video

    def get_synced_timings(self, slide_data):
        logger.debug("Loading files %s and %s" % (self.original_video_file, self.slide_video_file))
        # Load audio files first
        original_audio, original_sr = utils.get_audio_from_file(self.original_video_file)
        slide_audio, slide_sr = utils.get_audio_from_file(self.slide_video_file)

        logger.debug("Preprocessing info...")
        # Preprocess audio files
        original_audio, original_sr = sync.preprocess_audio(original_audio, original_sr)
        slide_audio, slide_sr = sync.preprocess_audio(slide_audio, slide_sr)

        logger.debug("Starting offset calculations...")
        updated_slides = []
        count = 0
        for slide_time, slide_name in slide_data.items():
            updated_time = sync.find_offset((original_audio, original_sr), (slide_audio, slide_sr), slide_time)
            # Clamp number to duration
            if updated_time < 0: updated_time = 0.0
            updated_slides.append((updated_time, slide_name))
            count += 1
            logger.debug("%s/%s" % (count, len(slide_data)))

        return updated_slides