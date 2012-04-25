from PyQt4 import QtGui, uic
from widgets.slide_button import SlideButton

form_class, _ = uic.loadUiType("ui/review_window.ui")
class ReviewWindow(QtGui.QMainWindow, form_class):
    _selected_slide = None


    def __init__(self, owner, slides, video_slides, matches):
        super(QtGui.QMainWindow, self).__init__(owner)
        self._slides = slides
        self._video_slides = video_slides
        self._matches = matches
        self.setupUi(self)
        self.scrVideoFrames.horizontalScrollBar().valueChanged.connect(self._video_scrolled)

        self._slide_widgets = self._show_slides(self.scrSlides, self._slides, horizontal=False, click_cb=self._slide_clicked)
        self._video_widgets = self._show_slides(self.scrVideoFrames, self._video_slides, selectable=False)
        match_list = [(None, self._slides[self._matches[time]][1]) for time in sorted(self._matches.iterkeys())]
        self._match_widgets = self._show_slides(self.scrMatches, match_list, selectable=False, click_cb=self._match_clicked)
        self._disable_matched_duplicates()

    def _show_slides(self, container, slides, horizontal=True, click_cb=None, selectable=True):
        widgets = []

        widget = QtGui.QWidget()
        if horizontal:
            layout = QtGui.QHBoxLayout(widget)
        else:
            layout = QtGui.QVBoxLayout(widget)
        layout.setSpacing(25)

        for id, img_path in slides:
            img = SlideButton(image_file=img_path, time=id, selected_callback=click_cb, selectable=selectable)
            layout.addWidget(img)
            widgets.append(img)
        widget.setLayout(layout)
        container.setWidget(widget)
        widget.show()
        return widgets

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

    def _match_clicked(self, widget):
        if self._selected_slide is None:
            if widget.disabled:
                widget.enable()
            else:
                widget.disable()
        else:
            widget.setImage(self._selected_slide.image_path)
            self._selected_slide.deselect()
            self._selected_slide = None

    def _video_scrolled(self, position):
        self.scrMatches.horizontalScrollBar().setValue(position)

