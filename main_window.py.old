from PyQt4 import QtGui
import logging
import os
from PyQt4.QtCore import QDir, Qt
from PyQt4.QtGui import QMessageBox
import datetime
from crop_window import CropWindow
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
    video_slides = [(2.16, '/tmp/sync/2.16 (1073741824).png'), (22.16, '/tmp/sync/22.16 (35.6361300392).png'), (24.16, '/tmp/sync/24.16 (35.9456742421).png'), (38.16, '/tmp/sync/38.16 (11.218083419).png'), (40.16, '/tmp/sync/40.16 (11.0006439783).png'), (68.16, '/tmp/sync/68.16 (92.9345933737).png'), (70.16, '/tmp/sync/70.16 (93.8840553504).png'), (88.16, '/tmp/sync/88.16 (52.4541823696).png'), (160.16, '/tmp/sync/160.16 (110.94294923).png'), (162.16, '/tmp/sync/162.16 (116.804611265).png'), (484.16, '/tmp/sync/484.16 (54.1802187623).png'), (522.16, '/tmp/sync/522.16 (35.3900827338).png'), (598.16, '/tmp/sync/598.16 (84.5447295291).png'), (760.16, '/tmp/sync/760.16 (83.5620598424).png'), (870.16, '/tmp/sync/870.16 (108.431528925).png'), (872.16, '/tmp/sync/872.16 (109.041043308).png'), (1026.16, '/tmp/sync/1026.16 (40.1712569949).png'), (1152.16, '/tmp/sync/1152.16 (18.2371013996).png'), (1158.16, '/tmp/sync/1158.16 (11.1790196302).png'), (1166.16, '/tmp/sync/1166.16 (12.13619983).png'), (1168.16, '/tmp/sync/1168.16 (13.2669115688).png'), (1176.16, '/tmp/sync/1176.16 (35.8350051391).png'), (1188.16, '/tmp/sync/1188.16 (12.2378024795).png'), (1190.16, '/tmp/sync/1190.16 (12.9114228431).png'), (1194.16, '/tmp/sync/1194.16 (13.2783191848).png'), (1204.16, '/tmp/sync/1204.16 (14.1342044488).png'), (1212.16, '/tmp/sync/1212.16 (12.4049957491).png'), (1214.16, '/tmp/sync/1214.16 (12.3057088837).png'), (1226.16, '/tmp/sync/1226.16 (15.1821824203).png'), (1234.16, '/tmp/sync/1234.16 (13.4200134506).png'), (1250.16, '/tmp/sync/1250.16 (13.5930025252).png'), (1252.16, '/tmp/sync/1252.16 (14.5809477584).png'), (1264.16, '/tmp/sync/1264.16 (11.1562678442).png'), (1266.16, '/tmp/sync/1266.16 (10.0532313119).png'), (1284.16, '/tmp/sync/1284.16 (37.2335420711).png'), (1290.16, '/tmp/sync/1290.16 (22.6405427183).png'), (1292.16, '/tmp/sync/1292.16 (23.6238056264).png'), (1294.16, '/tmp/sync/1294.16 (14.4397388557).png'), (1300.16, '/tmp/sync/1300.16 (22.1813956882).png'), (1318.16, '/tmp/sync/1318.16 (24.3311349246).png'), (1322.16, '/tmp/sync/1322.16 (23.1369707006).png'), (1326.16, '/tmp/sync/1326.16 (16.3523164186).png'), (1328.16, '/tmp/sync/1328.16 (15.9959013793).png'), (1330.16, '/tmp/sync/1330.16 (14.7880962351).png'), (1332.16, '/tmp/sync/1332.16 (16.0731946401).png'), (1340.16, '/tmp/sync/1340.16 (49.6316507417).png'), (1356.16, '/tmp/sync/1356.16 (11.6915851384).png'), (1358.16, '/tmp/sync/1358.16 (12.4914696664).png'), (1404.16, '/tmp/sync/1404.16 (44.0741685383).png'), (1412.16, '/tmp/sync/1412.16 (10.2465231515).png'), (1414.16, '/tmp/sync/1414.16 (10.9028734757).png'), (1456.16, '/tmp/sync/1456.16 (49.8049507023).png'), (1554.16, '/tmp/sync/1554.16 (11.8941337698).png'), (1562.16, '/tmp/sync/1562.16 (49.1451140127).png'), (1564.16, '/tmp/sync/1564.16 (10.4069308564).png'), (1566.16, '/tmp/sync/1566.16 (50.8491599731).png'), (1582.16, '/tmp/sync/1582.16 (46.7680567716).png'), (1584.16, '/tmp/sync/1584.16 (47.6750383849).png'), (1588.16, '/tmp/sync/1588.16 (49.2393347038).png'), (1594.16, '/tmp/sync/1594.16 (11.32348332).png'), (1606.16, '/tmp/sync/1606.16 (12.961967211).png'), (1616.16, '/tmp/sync/1616.16 (11.0717385511).png'), (1618.16, '/tmp/sync/1618.16 (12.6740137297).png'), (1628.16, '/tmp/sync/1628.16 (19.4469431649).png'), (1630.16, '/tmp/sync/1630.16 (16.1523881127).png'), (1666.16, '/tmp/sync/1666.16 (20.2087726979).png'), (1672.16, '/tmp/sync/1672.16 (13.8225792125).png'), (1676.16, '/tmp/sync/1676.16 (11.313874402).png'), (1686.16, '/tmp/sync/1686.16 (14.2820276118).png'), (1692.16, '/tmp/sync/1692.16 (13.9234427145).png'), (1702.16, '/tmp/sync/1702.16 (21.7818055503).png'), (1706.16, '/tmp/sync/1706.16 (17.9314908574).png'), (1716.16, '/tmp/sync/1716.16 (41.6984849062).png'), (1748.16, '/tmp/sync/1748.16 (11.2702012512).png'), (1752.16, '/tmp/sync/1752.16 (17.1129753702).png'), (1762.16, '/tmp/sync/1762.16 (19.5975198904).png'), (1764.16, '/tmp/sync/1764.16 (20.3408865964).png'), (1778.16, '/tmp/sync/1778.16 (27.0096850534).png'), (1780.16, '/tmp/sync/1780.16 (24.4364967579).png'), (1784.16, '/tmp/sync/1784.16 (16.0320942302).png'), (1786.16, '/tmp/sync/1786.16 (17.1025765478).png'), (1790.16, '/tmp/sync/1790.16 (17.2752166686).png'), (1792.16, '/tmp/sync/1792.16 (18.1345026457).png'), (1794.16, '/tmp/sync/1794.16 (18.7845654574).png'), (1806.16, '/tmp/sync/1806.16 (15.7670733564).png'), (1808.16, '/tmp/sync/1808.16 (16.2339798495).png'), (1810.16, '/tmp/sync/1810.16 (14.8180047458).png'), (1822.16, '/tmp/sync/1822.16 (17.3127799561).png'), (1826.16, '/tmp/sync/1826.16 (15.3901144568).png')]

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

        crop_window = CropWindow(self.video_file)
        crop_window.exec_()
        self.cropbox = crop_window.selected

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
        extractor = SlideExtractor(self.video_file, cropbox=self.cropbox, grayscale=False, callback=self._update_progress)
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
        self._disabled_matched_duplicates()
        end = datetime.datetime.now()
        self._status_ready()

        processing_time = end - start

    def _disabled_matched_duplicates(self):
        for i in range(0, len(self.match_widgets)):
            if i > 0 and self.match_widgets[i - 1].image_path == self.match_widgets[i].image_path:
                self.match_widgets[i].disable()

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