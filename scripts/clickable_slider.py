from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider
from PyQt6.QtGui import QMouseEvent

class ClickableSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            x = event.position().x()
            new_value = (self.maximum() - self.minimum()) * x / self.width()
            self.setValue(int(new_value))
            self.sliderMoved.emit(int(new_value))
