import json
import os
import zipfile

def package_slides(output_file, slide_data):
    zip_file = zipfile.ZipFile(output_file, mode="w", compression=zipfile.ZIP_DEFLATED)

    timings = {}
    for time, file in slide_data:
        zip_file.write(file, arcname=unicode(os.path.basename(file)).encode("utf-8"))
        timings[time] = os.path.basename(file)

    timings_json = json.dumps(timings)
    print "JSON timings: ", timings_json
    zip_file.writestr("timings.json", timings_json)
    zip_file.close()