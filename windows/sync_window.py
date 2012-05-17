from PyQt4 import QtGui
import Queue
import threading
from processing.slide_syncer import SlideSyncer
from ui import progress_window

class SyncWindow(QtGui.QDialog, progress_window.Ui_Dialog):
    _is_done = False

    def __init__(self, owner, app, original_video, camera_file, slide_data):
        super(QtGui.QDialog, self).__init__(owner)
        self._camera_video = camera_file
        self._original_video = original_video
        self._slide_data = slide_data
        self._app = app
        self.setupUi(self)
        self.setWindowTitle("Syncing videos...")
        self.lblInfo.setText("Syncing videos...")
        self.prgProgress.setMaximum(0)
        self.prgProgress.setMinimum(0)

    def process(self):
        result_queue = Queue.Queue()
        thread = threading.Thread(target=_process_sync, args=((self._original_video, self._camera_video, self._slide_data), result_queue))
        thread.daemon = True
        thread.start()

        while result_queue.empty():
            self._app.processEvents()

        result = result_queue.get()
        self.close()
        return result

def _process_sync(params, q):
    try:
        original_video, slide_video, matches = params
        slide_syncer = SlideSyncer(original_video, slide_video)
        results = slide_syncer.get_synced_timings(matches)
        q.put(results)
    except:
        q.put([])