import logging
import os
import sys
from PyQt4 import QtGui
from threading import Thread
import threading
from PyQt4.QtCore import QDir, Qt, QString
from PyQt4.QtGui import QMessageBox
import time
import datetime
from slide_extractor import SlideExtractor
from slide_matcher import SlideMatcher
import video
from video_view import VideoView

logger = logging.getLogger(__name__)

class MainWindow(QtGui.QMainWindow):
    video_file = None

    # TODO: remove debug
    slides = [(2.2, '/tmp/sync/2.2 (1073741824).png'), (200.2, '/tmp/sync/200.2 (4.74319468641).png'), (206.2, '/tmp/sync/206.2 (133.433372532).png'), (222.2, '/tmp/sync/222.2 (5.924389518).png'), (260.2, '/tmp/sync/260.2 (6.29094584785).png'), (362.2, '/tmp/sync/362.2 (7.35102932636).png'), (436.2, '/tmp/sync/436.2 (6.95023954704).png'), (618.2, '/tmp/sync/618.2 (9.37152656794).png'), (676.2, '/tmp/sync/676.2 (8.71631387921).png'), (798.2, '/tmp/sync/798.2 (8.23237369338).png'), (896.2, '/tmp/sync/896.2 (10.9022742451).png'), (898.2, '/tmp/sync/898.2 (34.614716899).png'), (900.2, '/tmp/sync/900.2 (45.1613915505).png'), (902.2, '/tmp/sync/902.2 (29.928226626).png'), (904.2, '/tmp/sync/904.2 (76.8059306039).png'), (906.2, '/tmp/sync/906.2 (17.5022590012).png'), (908.2, '/tmp/sync/908.2 (149.320444251).png'), (910.2, '/tmp/sync/910.2 (81.8942704704).png'), (940.2, '/tmp/sync/940.2 (75.151228223).png'), (942.2, '/tmp/sync/942.2 (13.705784698).png'), (946.2, '/tmp/sync/946.2 (57.2899462834).png'), (948.2, '/tmp/sync/948.2 (190.351716028).png'), (950.2, '/tmp/sync/950.2 (27.1294200058).png'), (984.2, '/tmp/sync/984.2 (45.3479754646).png'), (1010.2, '/tmp/sync/1010.2 (38.790886324).png'), (1034.2, '/tmp/sync/1034.2 (37.2802272067).png'), (1042.2, '/tmp/sync/1042.2 (5.96042610337).png'), (1046.2, '/tmp/sync/1046.2 (4.12350464576).png'), (1052.2, '/tmp/sync/1052.2 (4.90845673635).png'), (1058.2, '/tmp/sync/1058.2 (6.18731562137).png'), (1062.2, '/tmp/sync/1062.2 (4.86482868757).png'), (1076.2, '/tmp/sync/1076.2 (70.5558870499).png'), (1082.2, '/tmp/sync/1082.2 (41.5325101626).png'), (1086.2, '/tmp/sync/1086.2 (11.958764518).png'), (1090.2, '/tmp/sync/1090.2 (11.4927402729).png'), (1092.2, '/tmp/sync/1092.2 (13.473641115).png'), (1104.2, '/tmp/sync/1104.2 (20.1962565331).png'), (1122.2, '/tmp/sync/1122.2 (8.2550007259).png'), (1132.2, '/tmp/sync/1132.2 (56.5922379501).png'), (1134.2, '/tmp/sync/1134.2 (10.4740207607).png'), (1136.2, '/tmp/sync/1136.2 (5.82769091173).png'), (1138.2, '/tmp/sync/1138.2 (7.44112078978).png'), (1140.2, '/tmp/sync/1140.2 (18.6307041231).png'), (1144.2, '/tmp/sync/1144.2 (57.9821051103).png'), (1152.2, '/tmp/sync/1152.2 (9.01902076074).png'), (1170.2, '/tmp/sync/1170.2 (96.6150587979).png'), (1172.2, '/tmp/sync/1172.2 (4.8605981417).png'), (1182.2, '/tmp/sync/1182.2 (141.774858449).png'), (1186.2, '/tmp/sync/1186.2 (76.950283101).png'), (1188.2, '/tmp/sync/1188.2 (4.55731634727).png'), (1190.2, '/tmp/sync/1190.2 (5.20927918118).png'), (1192.2, '/tmp/sync/1192.2 (11.0130858014).png'), (1194.2, '/tmp/sync/1194.2 (5.65566419861).png'), (1196.2, '/tmp/sync/1196.2 (6.68742450639).png'), (1212.2, '/tmp/sync/1212.2 (4.45774535424).png'), (1214.2, '/tmp/sync/1214.2 (77.6945332462).png'), (1222.2, '/tmp/sync/1222.2 (9.3043960511).png'), (1224.2, '/tmp/sync/1224.2 (28.1228992451).png'), (1226.2, '/tmp/sync/1226.2 (4.01006170151).png'), (1260.2, '/tmp/sync/1260.2 (4.31550377468).png'), (1276.2, '/tmp/sync/1276.2 (107.70061266).png'), (1292.2, '/tmp/sync/1292.2 (137.164976771).png'), (1310.2, '/tmp/sync/1310.2 (24.3320876887).png'), (1330.2, '/tmp/sync/1330.2 (26.0538864692).png'), (1374.2, '/tmp/sync/1374.2 (157.941013357).png'), (1376.2, '/tmp/sync/1376.2 (25.2111157085).png'), (1380.2, '/tmp/sync/1380.2 (136.243217189).png'), (1412.2, '/tmp/sync/1412.2 (20.7571370499).png'), (1414.2, '/tmp/sync/1414.2 (84.0901204994).png'), (1454.2, '/tmp/sync/1454.2 (37.6108754355).png'), (1462.2, '/tmp/sync/1462.2 (9.36471907666).png'), (1464.2, '/tmp/sync/1464.2 (6.26389445412).png'), (1468.2, '/tmp/sync/1468.2 (15.3517465157).png'), (1480.2, '/tmp/sync/1480.2 (30.4438988095).png'), (1482.2, '/tmp/sync/1482.2 (4.46881678281).png'), (1484.2, '/tmp/sync/1484.2 (7.02030632985).png'), (1490.2, '/tmp/sync/1490.2 (4.64150624274).png'), (1498.2, '/tmp/sync/1498.2 (8.55151640534).png'), (1514.2, '/tmp/sync/1514.2 (4.56169933217).png'), (1516.2, '/tmp/sync/1516.2 (4.78073315912).png'), (1526.2, '/tmp/sync/1526.2 (124.823924216).png'), (1606.2, '/tmp/sync/1606.2 (131.877949332).png'), (1630.2, '/tmp/sync/1630.2 (4.9006293554).png'), (1632.2, '/tmp/sync/1632.2 (4.98217116725).png'), (1652.2, '/tmp/sync/1652.2 (9.57050740418).png'), (1664.2, '/tmp/sync/1664.2 (4.85427047038).png'), (1700.2, '/tmp/sync/1700.2 (112.335266405).png'), (1702.2, '/tmp/sync/1702.2 (4.28692436121).png'), (1720.2, '/tmp/sync/1720.2 (4.36457026713).png'), (1740.2, '/tmp/sync/1740.2 (122.929137631).png'), (1808.2, '/tmp/sync/1808.2 (15.7086657956).png'), (1810.2, '/tmp/sync/1810.2 (4.64385017422).png'), (1812.2, '/tmp/sync/1812.2 (12.7428527875).png'), (1814.2, '/tmp/sync/1814.2 (175.900330285).png'), (1816.2, '/tmp/sync/1816.2 (94.3697437573).png'), (1828.2, '/tmp/sync/1828.2 (86.6817363531).png'), (1830.2, '/tmp/sync/1830.2 (5.17278382695).png'), (1832.2, '/tmp/sync/1832.2 (4.07739256678).png'), (1836.2, '/tmp/sync/1836.2 (5.24592479675).png'), (1878.2, '/tmp/sync/1878.2 (75.969695122).png'), (1880.2, '/tmp/sync/1880.2 (74.02860482).png'), (1882.2, '/tmp/sync/1882.2 (23.719418554).png'), (1902.2, '/tmp/sync/1902.2 (38.8647248839).png'), (1956.2, '/tmp/sync/1956.2 (45.5171588269).png'), (1958.2, '/tmp/sync/1958.2 (5.12465301974).png'), (1966.2, '/tmp/sync/1966.2 (4.40586164344).png'), (1972.2, '/tmp/sync/1972.2 (121.342261905).png'), (2016.2, '/tmp/sync/2016.2 (53.8655480546).png'), (2034.2, '/tmp/sync/2034.2 (44.6505560395).png'), (2036.2, '/tmp/sync/2036.2 (69.776235482).png'), (2052.2, '/tmp/sync/2052.2 (79.863561266).png'), (2054.2, '/tmp/sync/2054.2 (15.1697553717).png'), (2064.2, '/tmp/sync/2064.2 (28.8390585075).png'), (2076.2, '/tmp/sync/2076.2 (41.1049535424).png'), (2082.2, '/tmp/sync/2082.2 (4.16091826365).png'), (2104.2, '/tmp/sync/2104.2 (31.2714626887).png'), (2106.2, '/tmp/sync/2106.2 (26.3967653891).png'), (2148.2, '/tmp/sync/2148.2 (31.8136113531).png'), (2162.2, '/tmp/sync/2162.2 (12.2227772938).png'), (2164.2, '/tmp/sync/2164.2 (4.76758347851).png'), (2190.2, '/tmp/sync/2190.2 (13.1751038037).png'), (2192.2, '/tmp/sync/2192.2 (11.6995993031).png'), (2202.2, '/tmp/sync/2202.2 (4.15349593496).png'), (2222.2, '/tmp/sync/2222.2 (28.0710227933).png'), (2306.2, '/tmp/sync/2306.2 (16.7695826074).png'), (2336.2, '/tmp/sync/2336.2 (13.3348845819).png'), (2364.2, '/tmp/sync/2364.2 (10.4580270035).png'), (2380.2, '/tmp/sync/2380.2 (10.6660743322).png'), (2412.2, '/tmp/sync/2412.2 (11.9039568815).png'), (2424.2, '/tmp/sync/2424.2 (9.93964285714).png'), (2436.2, '/tmp/sync/2436.2 (14.0528382695).png'), (2438.2, '/tmp/sync/2438.2 (32.2720826074).png'), (2512.2, '/tmp/sync/2512.2 (33.4764859175).png'), (2540.2, '/tmp/sync/2540.2 (13.6936026423).png'), (2550.2, '/tmp/sync/2550.2 (25.8847205285).png'), (2560.2, '/tmp/sync/2560.2 (16.976097561).png'), (2566.2, '/tmp/sync/2566.2 (81.2110271487).png'), (2568.2, '/tmp/sync/2568.2 (53.060050813).png'), (2572.2, '/tmp/sync/2572.2 (53.0880574913).png'), (2580.2, '/tmp/sync/2580.2 (53.3824600755).png'), (2582.2, '/tmp/sync/2582.2 (67.2801567944).png'), (2584.2, '/tmp/sync/2584.2 (66.6816231127).png'), (2588.2, '/tmp/sync/2588.2 (52.6740374564).png'), (2592.2, '/tmp/sync/2592.2 (77.2982186411).png'), (2598.2, '/tmp/sync/2598.2 (10.9161469222).png'), (2600.2, '/tmp/sync/2600.2 (4.45693597561).png'), (2612.2, '/tmp/sync/2612.2 (7.68732070267).png'), (2616.2, '/tmp/sync/2616.2 (7.88301321138).png'), (2618.2, '/tmp/sync/2618.2 (26.8120593786).png'), (2620.2, '/tmp/sync/2620.2 (26.1675704123).png'), (2624.2, '/tmp/sync/2624.2 (19.3204660279).png'), (2626.2, '/tmp/sync/2626.2 (18.9143350755).png'), (2628.2, '/tmp/sync/2628.2 (18.5402293844).png'), (2630.2, '/tmp/sync/2630.2 (14.0279377178).png'), (2638.2, '/tmp/sync/2638.2 (68.1733122822).png'), (2642.2, '/tmp/sync/2642.2 (105.22197953).png'), (2644.2, '/tmp/sync/2644.2 (66.5877134146).png'), (2646.2, '/tmp/sync/2646.2 (5.26296022067).png'), (2670.2, '/tmp/sync/2670.2 (103.303420441).png'), (2710.2, '/tmp/sync/2710.2 (15.549389518).png'), (2712.2, '/tmp/sync/2712.2 (26.4182353368).png'), (2714.2, '/tmp/sync/2714.2 (8.65346980256).png'), (2716.2, '/tmp/sync/2716.2 (12.4222771487).png'), (2718.2, '/tmp/sync/2718.2 (10.3767966028).png'), (2720.2, '/tmp/sync/2720.2 (4.74899535424).png'), (2722.2, '/tmp/sync/2722.2 (8.82289924506).png'), (2724.2, '/tmp/sync/2724.2 (6.63679297329).png'), (2726.2, '/tmp/sync/2726.2 (4.13032157375).png'), (2734.2, '/tmp/sync/2734.2 (5.10410351336).png'), (2800.2, '/tmp/sync/2800.2 (38.921642712).png'), (2802.2, '/tmp/sync/2802.2 (26.5056874274).png'), (2804.2, '/tmp/sync/2804.2 (85.9908275261).png'), (2810.2, '/tmp/sync/2810.2 (34.0269374274).png'), (2812.2, '/tmp/sync/2812.2 (33.503779036).png'), (2816.2, '/tmp/sync/2816.2 (67.5709487515).png'), (2818.2, '/tmp/sync/2818.2 (5.48532665505).png'), (2820.2, '/tmp/sync/2820.2 (5.32636759582).png'), (2832.2, '/tmp/sync/2832.2 (11.5580328107).png'), (2834.2, '/tmp/sync/2834.2 (43.9371885889).png'), (2836.2, '/tmp/sync/2836.2 (147.626283391).png'), (2872.2, '/tmp/sync/2872.2 (7.08094439605).png'), (2912.2, '/tmp/sync/2912.2 (5.10647285134).png'), (2970.2, '/tmp/sync/2970.2 (33.7369722706).png'), (3058.2, '/tmp/sync/3058.2 (41.3529319106).png'), (3162.2, '/tmp/sync/3162.2 (22.0111280488).png'), (3164.2, '/tmp/sync/3164.2 (5.51442726481).png'), (3236.2, '/tmp/sync/3236.2 (8.27820194541).png'), (3256.2, '/tmp/sync/3256.2 (9.63548925668).png'), (3288.2, '/tmp/sync/3288.2 (5.85231925087).png'), (3318.2, '/tmp/sync/3318.2 (15.5598105401).png'), (3344.2, '/tmp/sync/3344.2 (16.8235380372).png'), (3392.2, '/tmp/sync/3392.2 (14.5853230256).png'), (3430.2, '/tmp/sync/3430.2 (11.3894025842).png'), (3464.2, '/tmp/sync/3464.2 (8.99148591754).png'), (3594.2, '/tmp/sync/3594.2 (6.56609393148).png'), (3628.2, '/tmp/sync/3628.2 (4.71991289199).png'), (3660.2, '/tmp/sync/3660.2 (5.500646777).png'), (3694.2, '/tmp/sync/3694.2 (4.24971109175).png'), (3886.2, '/tmp/sync/3886.2 (8.08744047619).png'), (3892.2, '/tmp/sync/3892.2 (7.43509727062).png'), (3930.2, '/tmp/sync/3930.2 (9.83986062718).png'), (3932.2, '/tmp/sync/3932.2 (4.53633928571).png'), (3958.2, '/tmp/sync/3958.2 (7.06694323461).png'), (3960.2, '/tmp/sync/3960.2 (9.73271196283).png'), (3962.2, '/tmp/sync/3962.2 (4.22432128339).png'), (3978.2, '/tmp/sync/3978.2 (7.73169570267).png'), (3988.2, '/tmp/sync/3988.2 (129.296957753).png'), (3996.2, '/tmp/sync/3996.2 (49.8856823461).png'), (4000.2, '/tmp/sync/4000.2 (90.5102221254).png'), (4038.2, '/tmp/sync/4038.2 (16.5131039489).png'), (4040.2, '/tmp/sync/4040.2 (9.9300043554).png'), (4042.2, '/tmp/sync/4042.2 (31.2047786005).png'), (4044.2, '/tmp/sync/4044.2 (87.6284233449).png'), (4046.2, '/tmp/sync/4046.2 (32.6510576365).png'), (4048.2, '/tmp/sync/4048.2 (14.6575036295).png'), (4050.2, '/tmp/sync/4050.2 (9.36005081301).png')]

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.setGeometry(300, 300, 1280, 800)
        self.setWindowTitle("VSync")
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)

        # Prepare toolbar
        loadFileAction = QtGui.QAction("Load video...", self)
        loadFileAction.setShortcut("Ctrl+L")
        loadFileAction.triggered.connect(self.click_load_video)
        self.toolbar = self.addToolBar("Main")
        self.toolbar.addAction(loadFileAction)

        extractAction = QtGui.QAction("Extract slides", self)
        extractAction.triggered.connect(self.extract_slides)
        self.toolbar.addAction(extractAction)

        matchAction = QtGui.QAction("Match slides", self)
        matchAction.triggered.connect(self.match_slides)
        self.toolbar.addAction(matchAction)

        # Prepare status bar
        self.status_label = QtGui.QLabel("Status")
        self.status_label.setAlignment(Qt.AlignLeft)
        self.statusBar().addWidget(self.status_label, stretch=1)
        # Processing statusbar progres bar
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setMinimumWidth(200)
        self.progress_bar.setVisible(False)
        self.progress_bar.setAlignment(Qt.AlignRight)
        self.statusBar().addWidget(self.progress_bar)
        # Video format statusbar widget
        self.video_label = QtGui.QLabel("")
        self.video_label.setMinimumWidth(150)
        self.video_label.setAlignment(Qt.AlignRight)
        self.statusBar().addWidget(self.video_label)
        self.status_ready()

        self.video_view = VideoView()
        self.setCentralWidget(self.video_view)
        self.show()

    def click_load_video(self):
        filename = QtGui.QFileDialog().getOpenFileName(self, "Open video file", QDir.homePath())
        if filename == "":
            return      # User canceled the dialog

        self.status_label.setText("Loading %s..." % (filename,))

        try:
            self.video_file = video.VideoFile(filename)
        except video.VideoException as e:
            msgBox = QMessageBox(QMessageBox.Critical, "Error :(", "Video file could not be opened.")
            msgBox.setDetailedText(unicode(e))
            msgBox.exec_()
            return

        self.status_ready()
        self.video_label.setText(unicode(self.video_file.get_info()))
        self.video_view.show_frame(self.video_file.get_next_frame()[1])

    def update_progress(self, value, frame=None):
        if frame is not None:
            self.video_view.show_frame(frame)
        self.progress_bar.setValue(value)
        self.app.processEvents()

    def extract_slides(self):
        self.status_label.setText("Extracting slides...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(self.video_file.get_info().duration)
        self.progress_bar.setMinimum(0.0)

        start = datetime.datetime.now()
        extractor = SlideExtractor(self.video_file, cropbox=(220, 50, 820, 560), grayscale=False, callback=self.update_progress)
        self.slides = extractor.extract_slides()    # TODO: fix
        logger.debug("Slides: %s" % (self.slides,))
        end = datetime.datetime.now()
        self.status_ready()

        processing_time = end - start
        msgBox = QMessageBox(QMessageBox.Information, "Woot", "Extracting took %s " % (processing_time,))
        msgBox.exec_()

    def match_slides(self):
        if self.slides is None:
            return

        self.status_label.setText("Matching slides...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)

        start = datetime.datetime.now()

        # Get slide files first
        # TODO: make interface for this

        image_slides = []
        num = 0

        DIR = "/storage/djangomeet/Django14/"
        for file in sorted(os.listdir(DIR)):
            filename, extension = os.path.splitext(file)
            if extension == ".png":
                logger.debug("Found slide %s" % file)
                image_slides.append((num, os.path.join(DIR, file)))
                num += 1

        matcher = SlideMatcher(self.slides, image_slides)
        matcher.match_slides()

        end = datetime.datetime.now()
        self.status_ready()

        processing_time = end - start
        msgBox = QMessageBox(QMessageBox.Information, "Woot", "Matching took %s " % (processing_time,))
        msgBox.exec_()

    def status_ready(self):
        self.status_label.setText("Ready.")
        self.progress_bar.setVisible(False)
        self.status_label.update()

def main():
    """
    Main application entry point
    """
    logging.basicConfig(level=logging.DEBUG)

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()