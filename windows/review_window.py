from PyQt4 import QtGui
import itertools
import time
from ui import review_window
from widgets.slide_button import SlideButton

class ReviewWindow(QtGui.QMainWindow, review_window.Ui_mwReview):
    _selected_slide = None
    done = False    # Used to signal back end of use


    def __init__(self, owner, slides, video_slides, matches):
        super(QtGui.QMainWindow, self).__init__(owner)

        self._slides = slides
        self._video_slides = video_slides
        self._matches = matches
        self.setupUi(self)
        #self.scrVideoFrames.horizontalScrollBar().valueChanged.connect(self._video_scrolled)
        self.btnDone.clicked.connect(self._done)
        self._slide_widgets = self._show_slides(self.scrSlides, self._slides, horizontal=False, click_cb=self._slide_clicked)
        match_list = [(self._matches[time], self._slides[self._matches[time]][1]) for time in sorted(self._matches.iterkeys())]
        self._video_widgets, self._match_widgets = self._populate_matches(self._video_slides, match_list)
        self._disable_matched_duplicates()

        #self._video_widgets = self._show_slides(self.scrVideoFrames, self._video_slides, selectable=False)
        #self._match_widgets = self._show_slides(self.scrMatches, match_list, selectable=False, click_cb=self._match_clicked)


    def _show_slides(self, container, slides, horizontal=True, click_cb=None, selectable=True):
        widgets = []

        widget = QtGui.QWidget()
        if horizontal:
            layout = QtGui.QHBoxLayout(widget)
        else:
            layout = QtGui.QVBoxLayout(widget)
        layout.setSpacing(25)

        for id, img_path in slides:
            img = SlideButton(image_file=img_path, time=id, selected_callback=click_cb, selectable=selectable, num=(id + 1))
            layout.addWidget(img)
            widgets.append(img)
        widget.setLayout(layout)
        container.setWidget(widget)
        widget.show()
        return widgets

    def _populate_matches(self, video_slides, matched_slides):
        video_widgets = []
        match_widgets = []

        widget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(widget)
        layout.setSpacing(30)

        for video_slide, matched_slide in itertools.izip(video_slides, matched_slides):
            h_layout = QtGui.QHBoxLayout()

            info_box_layout = QtGui.QVBoxLayout()
            time_label = QtGui.QLabel()
            time_label.setText(self._format_time(video_slide[0]))
            info_box_layout.addWidget(time_label)
            h_layout.addLayout(info_box_layout)

            video_slide = SlideButton(image_file=video_slide[1], time=video_slide[0], selectable=False)
            video_slide.setMaximumHeight(300)
            video_widgets.append(video_slide)
            h_layout.addWidget(video_slide)
            matched_slide = SlideButton(image_file=matched_slide[1], time=matched_slide[0], selected_callback=self._match_clicked, selectable=False, num=(matched_slide[0] + 1))
            video_slide.setMaximumHeight(300)
            match_widgets.append(matched_slide)
            h_layout.addWidget(matched_slide)

            layout.addLayout(h_layout)

            line = QtGui.QFrame()
            line.setFrameShape(QtGui.QFrame.HLine)
            line.setFrameShadow(QtGui.QFrame.Sunken)
            layout.addWidget(line)


        widget.setLayout(layout)
        self.scrMatches.setWidget(widget)
        widget.show()

        return video_widgets, match_widgets

    def _disable_matched_duplicates(self):
        for i in range(0, len(self._match_widgets)):
            if i > 0 and self._match_widgets[i - 1].image_path == self._match_widgets[i].image_path:
                self._match_widgets[i].disable()

    def _slide_clicked(self, widget):
        if self._selected_slide is not None:
            self._selected_slide.deselect()

        if widget.selected:
            self._selected_slide = widget
        else:
            self._selected_slide = None

    def _format_time(self, seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def _match_clicked(self, widget):
        if self._selected_slide is None:
            if widget.disabled:
                widget.enable()
            else:
                widget.disable()
        else:
            widget.setImage(self._selected_slide.image_path)
            widget.num = self._selected_slide.num
            widget.enable()
            self._selected_slide.deselect()
            self._selected_slide = None

    def _video_scrolled(self, position):
        self.scrMatches.horizontalScrollBar().setValue(position)

    def closeEvent(self, QCloseEvent):
        matches = {}

        for i in range(0, len(self._match_widgets)):
            match_slide = self._match_widgets[i]
            if not match_slide.disabled:
                time = self._video_slides[i][0]
                matches[time] = match_slide.image_path

        self.matches = matches
        self.done = True

    def _done(self):
        self.close()
