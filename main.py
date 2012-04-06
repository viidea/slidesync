import logging
import os
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QDir, Qt
from PyQt4.QtGui import QMessageBox
import datetime
from slide_extractor import SlideExtractor
from slide_matcher import SlideMatcher
import video
from widgets.slide_button import SlideButton

logger = logging.getLogger(__name__)

class MainWindow(QtGui.QMainWindow):
    video_file = None

    # TODO: remove debug
    video_slides = [(2.0, '/tmp/sync/2.0 (1073741824).png'), (200.0, '/tmp/sync/200.0 (4.7381206446).png'), (206.0, '/tmp/sync/206.0 (133.417068815).png'), (222.0, '/tmp/sync/222.0 (5.90510307782).png'), (260.0, '/tmp/sync/260.0 (6.28900261324).png'), (362.0, '/tmp/sync/362.0 (7.35271341463).png'), (436.0, '/tmp/sync/436.0 (6.94161803136).png'), (618.0, '/tmp/sync/618.0 (9.36480037747).png'), (676.0, '/tmp/sync/676.0 (8.7093612079).png'), (798.0, '/tmp/sync/798.0 (8.23363530778).png'), (896.0, '/tmp/sync/896.0 (11.1702656794).png'), (898.0, '/tmp/sync/898.0 (35.2613632404).png'), (900.0, '/tmp/sync/900.0 (45.1867799071).png'), (902.0, '/tmp/sync/902.0 (29.9405255517).png'), (904.0, '/tmp/sync/904.0 (76.9001785714).png'), (906.0, '/tmp/sync/906.0 (17.940268583).png'), (908.0, '/tmp/sync/908.0 (148.350195993).png'), (910.0, '/tmp/sync/910.0 (81.15334277).png'), (940.0, '/tmp/sync/940.0 (73.753757259).png'), (942.0, '/tmp/sync/942.0 (14.8620920441).png'), (946.0, '/tmp/sync/946.0 (57.2611563589).png'), (948.0, '/tmp/sync/948.0 (190.888604094).png'), (950.0, '/tmp/sync/950.0 (26.6223744193).png'), (984.0, '/tmp/sync/984.0 (45.3339655923).png'), (1010.0, '/tmp/sync/1010.0 (38.7970107433).png'), (1034.0, '/tmp/sync/1034.0 (37.2762993612).png'), (1042.0, '/tmp/sync/1042.0 (5.39681837979).png'), (1046.0, '/tmp/sync/1046.0 (4.63113240418).png'), (1052.0, '/tmp/sync/1052.0 (4.98980691057).png'), (1058.0, '/tmp/sync/1058.0 (6.05390606852).png'), (1062.0, '/tmp/sync/1062.0 (5.52389227642).png'), (1076.0, '/tmp/sync/1076.0 (70.5215643148).png'), (1082.0, '/tmp/sync/1082.0 (41.5366819106).png'), (1086.0, '/tmp/sync/1086.0 (11.9621254355).png'), (1090.0, '/tmp/sync/1090.0 (9.45242450639).png'), (1092.0, '/tmp/sync/1092.0 (15.0839351045).png'), (1104.0, '/tmp/sync/1104.0 (20.1765585075).png'), (1122.0, '/tmp/sync/1122.0 (8.24537456446).png'), (1132.0, '/tmp/sync/1132.0 (56.4492203833).png'), (1134.0, '/tmp/sync/1134.0 (9.30322952962).png'), (1138.0, '/tmp/sync/1138.0 (8.34893800813).png'), (1140.0, '/tmp/sync/1140.0 (16.8280328107).png'), (1144.0, '/tmp/sync/1144.0 (57.9800500871).png'), (1152.0, '/tmp/sync/1152.0 (9.09116724739).png'), (1170.0, '/tmp/sync/1170.0 (28.5020339721).png'), (1172.0, '/tmp/sync/1172.0 (70.2634102787).png'), (1182.0, '/tmp/sync/1182.0 (141.098807346).png'), (1186.0, '/tmp/sync/1186.0 (76.9492973287).png'), (1192.0, '/tmp/sync/1192.0 (11.7791594077).png'), (1194.0, '/tmp/sync/1194.0 (6.40362587108).png'), (1196.0, '/tmp/sync/1196.0 (6.20081736353).png'), (1214.0, '/tmp/sync/1214.0 (79.6229188444).png'), (1222.0, '/tmp/sync/1222.0 (9.87044279907).png'), (1224.0, '/tmp/sync/1224.0 (29.2044410569).png'), (1226.0, '/tmp/sync/1226.0 (4.00559088269).png'), (1242.0, '/tmp/sync/1242.0 (4.54396849593).png'), (1260.0, '/tmp/sync/1260.0 (5.73917392567).png'), (1262.0, '/tmp/sync/1262.0 (6.62993321719).png'), (1276.0, '/tmp/sync/1276.0 (107.723228804).png'), (1292.0, '/tmp/sync/1292.0 (137.134844657).png'), (1310.0, '/tmp/sync/1310.0 (24.3197089141).png'), (1330.0, '/tmp/sync/1330.0 (15.7786636179).png'), (1332.0, '/tmp/sync/1332.0 (14.4140084204).png'), (1374.0, '/tmp/sync/1374.0 (140.465209785).png'), (1376.0, '/tmp/sync/1376.0 (13.5966332753).png'), (1380.0, '/tmp/sync/1380.0 (136.236588995).png'), (1414.0, '/tmp/sync/1414.0 (84.6471392276).png'), (1454.0, '/tmp/sync/1454.0 (37.5135460221).png'), (1462.0, '/tmp/sync/1462.0 (9.40198678862).png'), (1464.0, '/tmp/sync/1464.0 (6.71910060976).png'), (1468.0, '/tmp/sync/1468.0 (15.7115309233).png'), (1480.0, '/tmp/sync/1480.0 (29.9799745935).png'), (1482.0, '/tmp/sync/1482.0 (5.14528455285).png'), (1484.0, '/tmp/sync/1484.0 (7.62331083043).png'), (1490.0, '/tmp/sync/1490.0 (5.04878847271).png'), (1498.0, '/tmp/sync/1498.0 (8.54592987805).png'), (1526.0, '/tmp/sync/1526.0 (124.788774681).png'), (1606.0, '/tmp/sync/1606.0 (132.745868902).png'), (1630.0, '/tmp/sync/1630.0 (4.87637993612).png'), (1632.0, '/tmp/sync/1632.0 (5.01387993612).png'), (1648.0, '/tmp/sync/1648.0 (4.10456083043).png'), (1652.0, '/tmp/sync/1652.0 (6.88284262485).png'), (1662.0, '/tmp/sync/1662.0 (4.13255662021).png'), (1664.0, '/tmp/sync/1664.0 (4.92934088269).png'), (1700.0, '/tmp/sync/1700.0 (112.308745645).png'), (1720.0, '/tmp/sync/1720.0 (4.36554878049).png'), (1740.0, '/tmp/sync/1740.0 (123.023434233).png')]

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.setGeometry(300, 300, 1280, 800)
        self.setWindowTitle("VSync")
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        self._build_window_content()

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

    def click_load_slides(self):
        dirname = QtGui.QFileDialog().getExistingDirectory(self, "Open slide directory", QDir.homePath())
        if dirname == "":
            return

        dirname = unicode(dirname)  # Convert from QString to unicode string
        self.status_label.setText("Loading %s..." % (dirname))

        image_slides = []
        num = 0
        try:
            for file in sorted(os.listdir(dirname)):
                filename, extension = os.path.splitext(file)
                if extension == ".png":
                    logger.debug("Found slide %s" % file)
                    image_slides.append((num, os.path.join(dirname, file)))
                    num += 1
        except IOError as e:
            msgBox = QMessageBox(QMessageBox.Critical, "Error :(", "Video file could not be opened.")
            msgBox.setDetailedText(unicode(e))
            msgBox.exec_()
            return

        self.image_slides = image_slides
        self._show_slides(self.slide_scroll, self.image_slides)
        self.status_ready()

    def update_progress(self, value, frame=None):
        self.progress_bar.setValue(value)
        self.app.processEvents()

    def extract_slides(self):
        self.status_label.setText("Extracting slides...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(self.video_file.get_info().duration)
        self.progress_bar.setMinimum(0.0)

        start = datetime.datetime.now()
        extractor = SlideExtractor(self.video_file, cropbox=(220, 50, 820, 560), grayscale=False, callback=self.update_progress)
        self.video_slides = extractor.extract_slides()    # TODO: fix
        logger.debug("Slides: %s" % (self.video_slides,))
        end = datetime.datetime.now()

        self._show_slides(self.video_scroll, self.video_slides)
        self.status_ready()

        processing_time = end - start
        msgBox = QMessageBox(QMessageBox.Information, "Woot", "Extracting took %s " % (processing_time,))
        msgBox.exec_()

    def match_slides(self):
        if self.video_slides is None:
            return

        self.status_label.setText("Matching slides...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)

        start = datetime.datetime.now()

        matcher = SlideMatcher(self.video_slides, self.image_slides)
        matches = matcher.match_slides()
        self._show_slides(self.video_scroll, self.video_slides)

        match_list = [(time, self.image_slides[matches[time]][1]) for time in sorted(matches.iterkeys())]
        self._show_slides(self.matched_scroll, match_list)
        end = datetime.datetime.now()
        self.status_ready()

        processing_time = end - start
        msgBox = QMessageBox(QMessageBox.Information, "Woot", "Matching took %s " % (processing_time,))
        msgBox.exec_()

    def status_ready(self):
        self.status_label.setText("Ready.")
        self.progress_bar.setVisible(False)
        self.status_label.update()

    def _show_slides(self, container, slides, click_cb=None):
        widget = QtGui.QWidget()
        widget.setMaximumHeight(self.slide_scroll.height())
        layout = QtGui.QHBoxLayout(widget)
        layout.setSpacing(25)

        for id, img_path in slides:
            img = SlideButton(image_file=img_path, time=id, selected_callback=click_cb, selectable=True)
            img.setMaximumHeight(self.slide_scroll.height())
            layout.addWidget(img)
        widget.setLayout(layout)
        container.setWidget(widget)
        widget.show()

    def _build_window_content(self):
        # Prepare toolbar
        self.toolbar = self.addToolBar("Main")

        loadFileAction = QtGui.QAction("Load video...", self)
        loadFileAction.triggered.connect(self.click_load_video)
        self.toolbar.addAction(loadFileAction)

        loadSlidesAction = QtGui.QAction("Load slides...", self)
        loadSlidesAction.triggered.connect(self.click_load_slides)
        self.toolbar.addAction(loadSlidesAction)

        extractAction = QtGui.QAction("Extract slides", self)
        extractAction.triggered.connect(self.extract_slides)
        self.toolbar.addAction(extractAction)

        matchAction = QtGui.QAction("Match slides", self)
        matchAction.triggered.connect(self.match_slides)
        self.toolbar.addAction(matchAction)

        # Prepare main content area
        central_widget = QtGui.QWidget()
        self.setCentralWidget(central_widget)
        main_box = QtGui.QVBoxLayout()
        central_widget.setLayout(main_box)
        label_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed) # Expand horizontally only
        # Slide list
        slides_label = QtGui.QLabel("Available slides")
        slides_label.setSizePolicy(label_size_policy)
        main_box.addWidget(slides_label)

        self.slide_scroll = QtGui.QScrollArea(self)
        self.slide_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.slide_scroll.setWidgetResizable(True)
        main_box.addWidget(self.slide_scroll)

        # Video frames
        frames_label= QtGui.QLabel("Video frames")
        frames_label.setSizePolicy(label_size_policy)
        main_box.addWidget(frames_label)
        self.video_scroll = QtGui.QScrollArea(self)
        self.video_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.video_scroll.setWidgetResizable(True)
        self.video_scroll.horizontalScrollBar().valueChanged.connect(self._video_scrolled)

        main_box.addWidget(self.video_scroll)
        # Matched slides
        matched_label = QtGui.QLabel("Matched slides")
        matched_label.setSizePolicy(label_size_policy)
        main_box.addWidget(matched_label)

        self.matched_scroll = QtGui.QScrollArea(self)
        self.matched_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.matched_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.matched_scroll.setWidgetResizable(True)
        main_box.addWidget(self.matched_scroll)

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
        self.show()

    def _video_scrolled(self, position):
        self.matched_scroll.horizontalScrollBar().setValue(position)

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