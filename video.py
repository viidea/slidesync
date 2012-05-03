import logging
import pyvideo

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
    fps = None
    duration = None

    def __init__(self, width, height, fps, channels, samplerate, duration):
        self.width = width
        self.height = height
        self.audio_channels = channels
        self.audio_samplerate = samplerate
        self.fps = fps
        self.duration = duration

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "[V:%sx%s %s fps][A:%sch %sHz] %s s" % (self.width, self.height, self.fps, self.audio_channels, self.audio_samplerate, self.duration)

class VideoFile(object):
    info = None
    _current_frame = None
    _current_frame_timestamp = None
    _fps = None

    def __init__(self, filepath):
        self.filepath = unicode(filepath)
        self.load()

    def load(self):
        try:
            self.source = pyvideo.load(self.filepath)
        except pyvideo.exceptions.MediaException as e:
            raise VideoLoadException("Unknown video format.\n%s" % (e,))
        except IOError as e:
            raise VideoLoadException("Could not load video file.\n%s" % (e,))

        self._determine_fps()
        self.info = VideoInfo(self.source.video_format.width,
                              self.source.video_format.height,
                              self._fps,
                              self.source.audio_format.channels,
                              self.source.audio_format.sample_rate,
                              self.source.duration)

    def seek_to(self, timestamp):
        self.source.seek(timestamp)

    def get_frame(self):
        # Try to get next un-broken frame
        while self._current_frame is None:
            if self._current_frame_timestamp is None:
                break
            self.get_next_frame()

        return self._current_frame_timestamp, self._current_frame

    def get_next_frame(self):
        self._current_frame_timestamp = self.source.get_next_video_timestamp()
        self._current_frame = self.source.get_next_video_frame()
        return self._current_frame_timestamp, self._current_frame

    def _determine_fps(self):
        """
        This consumes one frame to determine FPS
        """
        while self._current_frame_timestamp is None and self._current_frame is None:
            self.get_next_frame()

        current_timestamp = self._current_frame_timestamp
        diff = self.source.get_next_video_timestamp() - current_timestamp
        self._fps = 1.0 / diff
        return self._fps

    def get_info(self):
        return self.info