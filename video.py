import logging
import pyglet

logger = logging.getLogger(__name__)

class VideoException(Exception):
    pass

class VideoLoadException(VideoException, IOError):
    pass

class VideoInfo(object):
    width = None
    height = None
    audio_channels = None
    audio_samplerate = None

    def __init__(self, width, height, channels, samplerate):
        self.width = width
        self.height = height
        self.audio_channels = channels
        self.audio_samplerate = samplerate

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "[V:%sx%s][A:%sch %sHz]" % (self.width, self.height, self.audio_channels, self.audio_samplerate)

class VideoFile(object):
    info = None
    current_frame = None
    current_frame_timestamp = None

    def __init__(self, filepath):
        self.filepath = unicode(filepath)
        self.load()

    def load(self):
        try:
            self.source = pyglet.media.load(self.filepath)
        except pyglet.media.MediaException as e:
            raise VideoLoadException("Unknown video format.\n%s" % (e,))
        except IOError as e:
            raise VideoLoadException("Could not load video file.\n%s" % (e,))

        self.info = VideoInfo(self.source.video_format.width, self.source.video_format.width, self.source.audio_format.channels, self.source.audio_format.sample_rate)

    def get_frame(self):
        if self.current_frame_timestamp is None or self.current_frame is None:
            return self.get_next_frame()
        return self.current_frame_timestamp, self.current_frame

    def get_next_frame(self):
        self.current_frame_timestamp = self.source.get_next_video_timestamp()
        self.current_frame = self.source.get_next_video_frame()
        logger.debug("[VideoFile] Got frame at %s." % (self.current_frame_timestamp,))
        return self.current_frame_timestamp, self.current_frame

    def get_info(self):
        return self.info