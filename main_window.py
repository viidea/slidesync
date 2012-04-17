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
    video_slides = [(2.16, '/tmp/sync/2.16 (1073741824).png'), (200.16, '/tmp/sync/200.16 (4.7381206446).png'), (206.16, '/tmp/sync/206.16 (133.417068815).png'), (222.16, '/tmp/sync/222.16 (5.90510307782).png'), (260.16, '/tmp/sync/260.16 (6.28900261324).png'), (362.16, '/tmp/sync/362.16 (7.35271341463).png'), (436.16, '/tmp/sync/436.16 (6.94161803136).png'), (618.16, '/tmp/sync/618.16 (9.36480037747).png'), (676.16, '/tmp/sync/676.16 (8.7093612079).png'), (798.16, '/tmp/sync/798.16 (8.23363530778).png'), (896.16, '/tmp/sync/896.16 (11.1702656794).png'), (898.16, '/tmp/sync/898.16 (35.2613632404).png')]

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