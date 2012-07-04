from matplotlib import pyplot
import numpy
from scipy.ndimage import filters

def find_peaks(x):
    peaks = []
    prev_diff = 0

    for i in range(len(x) - 1):
        diff = x[i] - x[i+1]
        if diff > 0 and prev_diff < 0:
            peaks.append(i)

        prev_diff = diff

    return numpy.asarray(peaks)

def smooth(x,beta):
     """ kaiser window smoothing """
     window_len=7
     # extending the data at beginning and at the end
     # to apply the window at the borders
     s = numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
     w = numpy.kaiser(window_len,beta)
     y = numpy.convolve(w/w.sum(),s,mode='valid')
     return y[3:len(y)-3]

def load_dat(filename):
    f = open(filename, "rb")

    x = []
    y = []
    for line in f.readlines():
        data = line.split()
        x.append(int(data[0]))
        y.append(float(data[1]))

    x = numpy.asarray(x)
    y = numpy.asarray(y)
    return x,y

def test_extractor_fun():
    x, y = load_dat("diffs.dat")
    std_dev = numpy.std(y)
    print "Standard deviation: ", std_dev

    y_smooth = smooth(y, 4)
    y_tresh = numpy.where(y_smooth > std_dev * 0.5, y_smooth, 0)
    peaks = find_peaks(y_tresh)
    y_p = y[peaks]
    pyplot.plot(x, y, "r", x, y_tresh, "b", peaks, y_p, "go")

    pyplot.show()

if __name__ == "__main__":
    test_extractor_fun()
