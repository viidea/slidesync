import logging
import os
from PyQt4 import QtGui
from PyQt4.QtCore import QDir
from audiosync import utils, sync


logger = logging.getLogger(__name__)
class SyncWindow(QtGui.QMainWindow):

    original_file = None
    camera_file = None

    def __init__(self, camera_file, slide_data, **kwargs):
        super(SyncWindow, self).__init__(**kwargs)
        self.camera_file = camera_file
        self.slide_data = slide_data

        self.setWindowTitle("Synchronize with main track")
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

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
        self.original_file = unicode(QtGui.QFileDialog().getOpenFileName(self, "Open original video", QDir.homePath()))
        filename = os.path.basename(self.original_file)
        self.original_filename.setText(filename)
        self._check_enable_sync()

    def _browse_camera(self):
        self.camera_file = unicode(QtGui.QFileDialog().getOpenFileName(self, "Open camera video", QDir.homePath()))
        filename = os.path.basename(self.camera_file)
        self.camera_filename.setText(filename)
        self._check_enable_sync()

    def _check_enable_sync(self):
        if self.original_file is not None and self.camera_file is not None:
            self.btn_sync.setEnabled(True)

    def _sync(self):
        logger.debug("Loading files %s and %s" % (self.original_file, self.camera_file))
        # Load audio files first
        original_audio, original_sr = utils.get_audio_from_file(self.original_file)
        slide_audio, slide_sr = utils.get_audio_from_file(self.camera_file)

        logger.debug("Preprocessing info...")
        # Preprocess audio files
        original_audio, original_sr = sync.preprocess_audio(original_audio, original_sr)
        slide_audio, slide_sr = sync.preprocess_audio(slide_audio, slide_sr)

        logger.debug("Starting offset calculations...")
        updated_slides = []
        count = 0
        for slide_time, slide_name in self.slide_data.items():
            updated_time = sync.find_offset((original_audio, original_sr), (slide_audio, slide_sr), slide_time)
            updated_slides.append((updated_time, slide_name))
            count += 1
            logger.debug("%s/%s" % (count, len(self.slide_data)))

        print updated_slides