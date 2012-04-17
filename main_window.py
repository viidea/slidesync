from PyQt4 import QtGui
import logging
import os
from PyQt4.QtCore import QDir, Qt
from PyQt4.QtGui import QMessageBox
import datetime
from processing.slide_extractor import SlideExtractor
from processing.slide_matcher import SlideMatcher
from sync_window import SyncWindow
import video
from widgets.slide_button import SlideButton

logger = logging.getLogger(__name__)
class MainWindow(QtGui.QMainWindow):
    video_file = None
    selected_slide = None
    match_widgets = []

    # TODO: remove debug
    video_slides = [(2.16, '/tmp/sync/2.16 (1073741824).png'), (200.16, '/tmp/sync/200.16 (4.7381206446).png'), (206.16, '/tmp/sync/206.16 (133.417068815).png'), (222.16, '/tmp/sync/222.16 (5.90510307782).png'), (260.16, '/tmp/sync/260.16 (6.28900261324).png'), (362.16, '/tmp/sync/362.16 (7.35271341463).png'), (436.16, '/tmp/sync/436.16 (6.94161803136).png'), (618.16, '/tmp/sync/618.16 (9.36480037747).png'), (676.16, '/tmp/sync/676.16 (8.7093612079).png'), (798.16, '/tmp/sync/798.16 (8.23363530778).png'), (896.16, '/tmp/sync/896.16 (11.1702656794).png'), (898.16, '/tmp/sync/898.16 (35.2613632404).png'), (900.16, '/tmp/sync/900.16 (45.1867799071).png'), (902.16, '/tmp/sync/902.16 (29.9405255517).png'), (904.16, '/tmp/sync/904.16 (76.9001785714).png'), (906.16, '/tmp/sync/906.16 (17.940268583).png'), (908.16, '/tmp/sync/908.16 (148.350195993).png'), (910.16, '/tmp/sync/910.16 (81.15334277).png'), (940.16, '/tmp/sync/940.16 (73.753757259).png'), (942.16, '/tmp/sync/942.16 (14.8620920441).png'), (946.16, '/tmp/sync/946.16 (57.2611563589).png'), (948.16, '/tmp/sync/948.16 (190.888604094).png'), (950.16, '/tmp/sync/950.16 (26.6223744193).png'), (984.16, '/tmp/sync/984.16 (45.3339655923).png'), (1010.16, '/tmp/sync/1010.16 (38.7970107433).png'), (1034.16, '/tmp/sync/1034.16 (37.2762993612).png'), (1042.16, '/tmp/sync/1042.16 (5.39681837979).png'), (1046.16, '/tmp/sync/1046.16 (4.63113240418).png'), (1052.16, '/tmp/sync/1052.16 (4.98980691057).png'), (1058.16, '/tmp/sync/1058.16 (6.05390606852).png'), (1062.16, '/tmp/sync/1062.16 (5.52389227642).png'), (1076.16, '/tmp/sync/1076.16 (70.5215643148).png'), (1082.16, '/tmp/sync/1082.16 (41.5366819106).png'), (1086.16, '/tmp/sync/1086.16 (11.9621254355).png'), (1090.16, '/tmp/sync/1090.16 (9.45242450639).png'), (1092.16, '/tmp/sync/1092.16 (15.0839351045).png'), (1104.16, '/tmp/sync/1104.16 (20.1765585075).png'), (1122.16, '/tmp/sync/1122.16 (8.24537456446).png'), (1132.16, '/tmp/sync/1132.16 (56.4492203833).png'), (1134.16, '/tmp/sync/1134.16 (9.30322952962).png'), (1138.16, '/tmp/sync/1138.16 (8.34893800813).png'), (1140.16, '/tmp/sync/1140.16 (16.8280328107).png'), (1144.16, '/tmp/sync/1144.16 (57.9800500871).png'), (1152.16, '/tmp/sync/1152.16 (9.09116724739).png'), (1170.16, '/tmp/sync/1170.16 (28.5020339721).png'), (1172.16, '/tmp/sync/1172.16 (70.2634102787).png'), (1182.16, '/tmp/sync/1182.16 (141.098807346).png'), (1186.16, '/tmp/sync/1186.16 (76.9492973287).png'), (1192.16, '/tmp/sync/1192.16 (11.7791594077).png'), (1194.16, '/tmp/sync/1194.16 (6.40362587108).png'), (1196.16, '/tmp/sync/1196.16 (6.20081736353).png'), (1214.16, '/tmp/sync/1214.16 (79.6229188444).png'), (1222.16, '/tmp/sync/1222.16 (9.87044279907).png'), (1224.16, '/tmp/sync/1224.16 (29.2044410569).png'), (1226.16, '/tmp/sync/1226.16 (4.00559088269).png'), (1242.16, '/tmp/sync/1242.16 (4.54396849593).png'), (1260.16, '/tmp/sync/1260.16 (5.73917392567).png'), (1262.16, '/tmp/sync/1262.16 (6.62993321719).png'), (1276.16, '/tmp/sync/1276.16 (107.723228804).png'), (1292.16, '/tmp/sync/1292.16 (137.134844657).png'), (1310.16, '/tmp/sync/1310.16 (24.3197089141).png'), (1330.16, '/tmp/sync/1330.16 (15.7786636179).png'), (1332.16, '/tmp/sync/1332.16 (14.4140084204).png'), (1374.16, '/tmp/sync/1374.16 (140.465209785).png'), (1376.16, '/tmp/sync/1376.16 (13.5966332753).png'), (1380.16, '/tmp/sync/1380.16 (136.236588995).png'), (1414.16, '/tmp/sync/1414.16 (84.6471392276).png'), (1454.16, '/tmp/sync/1454.16 (37.5135460221).png'), (1462.16, '/tmp/sync/1462.16 (9.40198678862).png'), (1464.16, '/tmp/sync/1464.16 (6.71910060976).png'), (1468.16, '/tmp/sync/1468.16 (15.7115309233).png'), (1480.16, '/tmp/sync/1480.16 (29.9799745935).png'), (1482.16, '/tmp/sync/1482.16 (5.14528455285).png'), (1484.16, '/tmp/sync/1484.16 (7.62331083043).png'), (1490.16, '/tmp/sync/1490.16 (5.04878847271).png'), (1498.16, '/tmp/sync/1498.16 (8.54592987805).png'), (1526.16, '/tmp/sync/1526.16 (124.788774681).png'), (1606.16, '/tmp/sync/1606.16 (132.745868902).png'), (1630.16, '/tmp/sync/1630.16 (4.87637993612).png'), (1632.16, '/tmp/sync/1632.16 (5.01387993612).png'), (1648.16, '/tmp/sync/1648.16 (4.10456083043).png'), (1652.16, '/tmp/sync/1652.16 (6.88284262485).png'), (1662.16, '/tmp/sync/1662.16 (4.13255662021).png'), (1664.16, '/tmp/sync/1664.16 (4.92934088269).png'), (1700.16, '/tmp/sync/1700.16 (112.308745645).png'), (1720.16, '/tmp/sync/1720.16 (4.36554878049).png'), (1740.16, '/tmp/sync/1740.16 (123.023434233).png')]

    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        self.setGeometry(300, 300, 1280, 800)
        self.setWindowTitle("Viidea Slide Sync")
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        self._build_window_content()

    def load_video(self):
        filename = QtGui.QFileDialog().getOpenFileName(self, "Open video file", "/storage/djangomeet/")
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

        self._status_ready()
        self.video_label.setText(unicode(self.video_file.get_info()))

    def load_slides(self):
        dirname = QtGui.QFileDialog().getExistingDirectory(self, "Open slide directory", "/storage/djangomeet/")
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
        self._show_slides(self.slide_scroll, self.image_slides, click_cb=self._click_slide)
        self._status_ready()

    def _update_progress(self, value, min = 0.0, max = 1.0):
        if self.progress_bar.minimum() != min:
            self.progress_bar.setMinimum(min)
        if self.progress_bar.maximum() != max:
            self.progress_bar.setMaximum(max)

        self.progress_bar.setValue(value)
        self.app.processEvents()

    def extract_slides(self):
        self.status_label.setText("Extracting slides...")
        self.progress_bar.setVisible(True)

        start = datetime.datetime.now()
        extractor = SlideExtractor(self.video_file, cropbox=(220, 50, 820, 560), grayscale=False, callback=self._update_progress)
        self.video_slides = extractor.extract_slides()    # TODO: fix
        logger.debug("Slides: %s" % (self.video_slides,))
        end = datetime.datetime.now()

        self._show_slides(self.video_scroll, self.video_slides)
        self._status_ready()
        processing_time = end - start

    def match_slides(self):
        if self.video_slides is None:
            return

        self.status_label.setText("Matching slides...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        start = datetime.datetime.now()

        matcher = SlideMatcher(self.video_slides, self.image_slides, progress_cb=self._update_progress)
        matches = matcher.match_slides()
        match_list = [(None, self.image_slides[matches[time]][1]) for time in sorted(matches.iterkeys())]
        self.match_widgets = self._show_slides(self.matched_scroll, match_list, click_cb=self._click_matched_slide, selectable=False)
        self._show_slides(self.video_scroll, self.video_slides)
        end = datetime.datetime.now()
        self._status_ready()

        processing_time = end - start

    def sync(self):
        # Collect sync data first
        matches = {}

        for i in range(0, len(self.match_widgets)):
            match_slide = self.match_widgets[i]
            if not match_slide.disabled:
                time = self.video_slides[i][0]
                matches[time] = match_slide.image_path

        print matches

        if not self.video_file:
            sync_window = SyncWindow(self.app, None, matches, parent=self)
        else:
            sync_window = SyncWindow(self.app, self.video_file.filepath, matches, parent=self)
        sync_window.show()

    def _status_ready(self):
        self.status_label.setText("Ready.")
        self.progress_bar.setVisible(False)
        self.status_label.update()

    def _show_slides(self, container, slides, click_cb=None, selectable=True):
        widgets = []

        widget = QtGui.QWidget()
        widget.setMaximumHeight(self.slide_scroll.height())
        layout = QtGui.QHBoxLayout(widget)
        layout.setSpacing(25)

        for id, img_path in slides:
            img = SlideButton(image_file=img_path, time=id, selected_callback=click_cb, selectable=selectable)
            img.setMaximumHeight(self.slide_scroll.height())
            layout.addWidget(img)
            widgets.append(img)
        widget.setLayout(layout)
        container.setWidget(widget)
        widget.show()

        return widgets

    def _click_matched_slide(self, widget):
        if self.selected_slide is None:
            if widget.disabled:
                widget.enable()
            else:
                widget.disable()
        else:
            widget.time = self.selected_slide.time
            widget.setImage(self.selected_slide.image_path)
            self.selected_slide.deselect()
            self.selected_slide = None

    def _click_slide(self, widget):
        if self.selected_slide is not None:
            self.selected_slide.deselect()

        if widget.selected:
            self.selected_slide = widget
        else:
            self.selected_slide = None


    def _build_window_content(self):
        # Prepare toolbar
        self.toolbar = self.addToolBar("Main")

        loadFileAction = QtGui.QAction("Load video...", self)
        loadFileAction.triggered.connect(self.load_video)
        self.toolbar.addAction(loadFileAction)

        loadSlidesAction = QtGui.QAction("Load slides...", self)
        loadSlidesAction.triggered.connect(self.load_slides)
        self.toolbar.addAction(loadSlidesAction)

        extractAction = QtGui.QAction("Extract slides", self)
        extractAction.triggered.connect(self.extract_slides)
        self.toolbar.addAction(extractAction)

        matchAction = QtGui.QAction("Match slides", self)
        matchAction.triggered.connect(self.match_slides)
        self.toolbar.addAction(matchAction)

        syncAction = QtGui.QAction("Sync", self)
        syncAction.triggered.connect(self.sync)
        self.toolbar.addAction(syncAction)

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
        self._status_ready()
        self.show()

    def _video_scrolled(self, position):
        self.matched_scroll.horizontalScrollBar().setValue(position)