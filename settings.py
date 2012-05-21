import ConfigParser
import ast
import os

RECENT_FILES_SECTION = "Recent files"

RENDERED_VIDEOS_KEY = "Rendered videos"
SLIDE_VIDEOS_KEY = "Slide videos"
SLIDE_DIRECTORIES_KEY = "Slide directories"
def store_recent_files(rendered_videos, slide_videos, slide_directories):
    config = ConfigParser.SafeConfigParser()
    config.add_section(RECENT_FILES_SECTION)
    config.set(RECENT_FILES_SECTION, RENDERED_VIDEOS_KEY, unicode(rendered_videos))
    config.set(RECENT_FILES_SECTION, SLIDE_VIDEOS_KEY, unicode(slide_videos))
    config.set(RECENT_FILES_SECTION, SLIDE_DIRECTORIES_KEY, unicode(slide_directories))

    with open("settings.ini", "w") as configfile:
        config.write(configfile)

def load_recent_files():
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(open("settings.ini", "r"))
        rendered_videos = ast.literal_eval(config.get(RECENT_FILES_SECTION, RENDERED_VIDEOS_KEY))
        slide_videos = ast.literal_eval(config.get(RECENT_FILES_SECTION, SLIDE_VIDEOS_KEY))
        slide_directories = ast.literal_eval(config.get(RECENT_FILES_SECTION, SLIDE_DIRECTORIES_KEY))
        return rendered_videos, slide_videos, slide_directories
    except (IOError, ValueError):
        return [], [], []

