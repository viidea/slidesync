import json
import logging
import os
import zipfile

logger = logging.getLogger(__name__)
def package_slides(output_file, slides, slide_data):
    zip_file = zipfile.ZipFile(output_file, mode="w", compression=zipfile.ZIP_DEFLATED)

    # Prevents duplicate files in the archive
    for slide in slides:
        filename = unicode(os.path.basename(slide))
        zip_file.write(slide, arcname=filename.encode("utf-8"))

    timings = {}
    for time, file in slide_data:
        timings[time] = os.path.basename(file)

    # Check for timings.txt and add it
    if len(slides) > 0:
        slide_path = os.path.dirname(slides[0])
        titles = os.path.join(slide_path, "slides.txt")
        if os.path.exists(titles):
            zip_file.write(titles, arcname="slides.txt")

    timings_json = json.dumps(timings, sort_keys=True)
    logger.info("JSON timings: %s", timings_json)
    zip_file.writestr("timings.txt", timings_json)
    zip_file.close()