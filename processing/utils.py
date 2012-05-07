import json
import logging
import os
import zipfile

logger = logging.getLogger(__name__)
def package_slides(output_file, slide_data):
    zip_file = zipfile.ZipFile(output_file, mode="w", compression=zipfile.ZIP_DEFLATED)

    # Prevents duplicate files in the archive
    included_files = set()

    timings = {}
    for time, file in slide_data:
        if time < 0: continue   # Skip negatively timed slides
        filename = unicode(os.path.basename(file))
        if not filename in included_files:
            zip_file.write(file, arcname=filename.encode("utf-8"))
            included_files.add(filename)
        timings[time] = os.path.basename(file)

    timings_json = json.dumps(timings, sort_keys=True)
    logger.info("JSON timings: %s", timings_json)
    zip_file.writestr("timings.txt", timings_json)
    zip_file.close()
