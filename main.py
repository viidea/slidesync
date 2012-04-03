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
    video_slides = [(2.2, '/tmp/sync/2.2 (1073741824).png'), (200.2, '/tmp/sync/200.2 (4.74319468641).png'), (206.2, '/tmp/sync/206.2 (133.433372532).png'), (222.2, '/tmp/sync/222.2 (5.924389518).png'), (260.2, '/tmp/sync/260.2 (6.29094584785).png'), (362.2, '/tmp/sync/362.2 (7.35102932636).png'), (436.2, '/tmp/sync/436.2 (6.95023954704).png'), (618.2, '/tmp/sync/618.2 (9.37152656794).png'), (676.2, '/tmp/sync/676.2 (8.71631387921).png'), (798.2, '/tmp/sync/798.2 (8.23237369338).png'), (896.2, '/tmp/sync/896.2 (10.9022742451).png'), (898.2, '/tmp/sync/898.2 (34.614716899).png')]

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
        self.video_view.show_frame(self.video_file.get_next_frame()[1])

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
        self.slide_list = QtGui.QHBoxLayout()
        main_box.addLayout(self.slide_list)
        # Video frames
        frames_label= QtGui.QLabel("Video frames")
        frames_label.setSizePolicy(label_size_policy)
        main_box.addWidget(frames_label)
        self.frame_list = QtGui.QHBoxLayout()
        main_box.addLayout(self.frame_list)
        # Matched slides
        matched_label = QtGui.QLabel("Matched slides")
        matched_label.setSizePolicy(label_size_policy)
        main_box.addWidget(matched_label)
        self.matched_list = QtGui.QHBoxLayout()
        main_box.addLayout(self.matched_list)

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