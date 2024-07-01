from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsBlurEffect
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QCursor, QBrush, QLinearGradient
from PySide6.QtCore import Qt, QSize, QRect, QTimer

class ComponentBodyArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        bodyWidgetPallette = self.palette()
        bodyWidgetPallette.setColor(QPalette.Window, QColor(255, 255, 255, 255))
        self.setPalette(bodyWidgetPallette)