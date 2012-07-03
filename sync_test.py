import os
import sys
from audiosync import sync, utils, correlate

@profile
def work(f1, f2):
    print "Loading first audio..."
    file1_audio, file1_orig_sr = utils.get_audio_from_file(f1)
    file1_audio = file1_audio[0:file1_orig_sr * 3600]
    print "Preprocessing first audio..."
    file1_audio, file1_sr = sync.preprocess_audio(file1_audio, file1_orig_sr, bandpass=False)
    print "Loading second audio..."
    file2_audio, file2_orig_sr = utils.get_audio_from_file(f2)
    file2_audio = file2_audio[0:file2_orig_sr * 3600]
    print "Preprocessing second audio..."
    file2_audio, file2_sr = sync.preprocess_audio(file2_audio, file2_orig_sr, bandpass=False)

    print file1_sr, " - ", file2_sr
    global_offset = correlate.get_offset(file1_audio, file2_audio, file1_sr)
    print "Found offset", global_offset

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Not enough arguments."

    raw_input("Press Enter to continue...")

    file1 = os.path.abspath(sys.argv[1])
    file2 = os.path.abspath(sys.argv[2])

    work(file1, file2)