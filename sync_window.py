import logging
import os
from PyQt4 import QtGui
from PyQt4.QtCore import QDir, Qt
from processing.slide_syncer import SlideSyncer
from processing.utils import package_slides

logger = logging.getLogger(__name__)
class SyncWindow(QtGui.QMainWindow):

    original_file = None
    camera_file = None

    def __init__(self,app, camera_file, slide_data, **kwargs):
        super(SyncWindow, self).__init__(**kwargs)
        self.app = app
        self.camera_file = camera_file
        self.slide_data = slide_data

        self.setWindowTitle("Synchronize")
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)
        self.setGeometry(2400, 300, 400, 200)

        self.status_label = QtGui.QLabel("Status")
        self.status_label.setAlignment(Qt.AlignLeft)
        self.status_label.setText("Ready.")
        self.statusBar().addWidget(self.status_label, stretch=1)

        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setMinimumWidth(100)
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setAlignment(Qt.AlignRight)
        self.statusBar().addWidget(self.progress_bar)

        central_widget = QtGui.QWidget(self)
        self.setCentralWidget(central_widget)

        main_grid = QtGui.QGridLayout()
        central_widget.setLayout(main_grid)
        main_grid.addWidget(QtGui.QLabel("Original video:"), 0, 0)
        main_grid.addWidget(QtGui.QLabel("Slide camera video:"), 1, 0)

        self.original_filename = QtGui.QLineEdit()
        self.original_filename.setEnabled(False)
        main_grid.addWidget(self.original_filename, 0, 1)

        self.camera_filename = QtGui.QLineEdit()
        if self.camera_file is not None:
            self.camera_filename.setText(os.path.basename(self.camera_file))
        self.camera_filename.setEnabled(False)
        main_grid.addWidget(self.camera_filename, 1, 1)

        btn_browse_original = QtGui.QPushButton("Browse...")
        btn_browse_original.clicked.connect(self._browse_original)
        main_grid.addWidget(btn_browse_original, 0, 2)

        btn_browse_camera = QtGui.QPushButton("Browse...")
        btn_browse_camera.clicked.connect(self._browse_camera)
        main_grid.addWidget(btn_browse_camera, 1, 2)

        self.btn_sync = QtGui.QPushButton("Sync")
        self.btn_sync.setEnabled(False)
        self.btn_sync.clicked.connect(self._sync)
        main_grid.addWidget(self.btn_sync, 2, 2)

    def _browse_original(self):
        self.original_file = unicode(QtGui.QFileDialog().getOpenFileName(self, "Open original video", "/storage/djangomeet/"))
        filename = os.path.basename(self.original_file)
        self.original_filename.setText(filename)
        self._check_enable_sync()

    def _browse_camera(self):
        self.camera_file = unicode(QtGui.QFileDialog().getOpenFileName(self, "Open camera video", "/storage/djangomeet/"))
        filename = os.path.basename(self.camera_file)
        self.camera_filename.setText(filename)
        self._check_enable_sync()

    def _check_enable_sync(self):
        if self.original_file is not None and self.camera_file is not None:
            self.btn_sync.setEnabled(True)

    def _progress_cb(self):
        self.app.processEvents()

    def _sync(self):
        self.status_label.setText("Syncing slides to main video...")
        self.progress_bar.setVisible(True)
        syncer = SlideSyncer(self.original_file, self.camera_file)
        slides = syncer.get_synced_timings(self.slide_data, progress_cb = self._progress_cb)
        package_slides("/tmp/slides.zip", slides)
        self.close()
        self.status_label.setText("Ready.")