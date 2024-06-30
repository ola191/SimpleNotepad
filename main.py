import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGraphicsBlurEffect
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QCursor, QBrush, QLinearGradient
from PySide6.QtCore import Qt, QSize, QRect, QTimer

from BlurWindow.blurWindow import blur

from components.CustomTitleBar import CustomTitleBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WindowTitle")
        self.setMinimumSize(1200, 750)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        hWnd = self.winId()
        print(hWnd)
        blur(hWnd)

        self.buildUI()
        
        self.setMouseTracking(True)
        self.resizing = False
        self.resizeDir = None

    def buildUI(self):
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.titleBar = CustomTitleBar(self)
        mainLayout.addWidget(self.titleBar)
        self.setCustomTitleBarBackground()

        whiteBar = QWidget()
        whiteBar.setFixedHeight(64)
        whiteBar.setAutoFillBackground(True)
        palette = whiteBar.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        whiteBar.setPalette(palette)
        mainLayout.addWidget(whiteBar)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)

        self.navWidget = QWidget()
        self.navWidget.setAutoFillBackground(True)
        navWidgetPallette = self.navWidget.palette()
        navWidgetPallette.setColor(QPalette.Window, QColor(244, 249, 254, 60))
        self.navWidget.setPalette(navWidgetPallette)
        self.setNavBackground()

        navLayout = QVBoxLayout(self.navWidget)
        navLayout.setContentsMargins(10,10,10,10)
        navLayout.setSpacing(10)

        # username = os.getlogin()
        # titleLabel = QLabel(f"{username}")
        # titleLabel.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        # navLayout.addWidget(titleLabel)

        buttons = ["New File", "Open File", "Save File", "Close File", "Settings"]
        for button in buttons:
            btn = QPushButton(button)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    font-size: 12pt;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            navLayout.addWidget(btn)
        navLayout.addStretch()

        self.bodyWidget = QWidget()
        self.bodyWidget.setAutoFillBackground(True)
        bodyWidgetPallette = self.bodyWidget.palette()
        bodyWidgetPallette.setColor(QPalette.Window, QColor(255, 255, 255, 255))
        self.bodyWidget.setPalette(bodyWidgetPallette)

        contentLayout.addWidget(self.navWidget, 1)
        contentLayout.addWidget(self.bodyWidget, 3)

        mainLayout.addLayout(contentLayout)

    def setNavBackground(self):
        gradient = QLinearGradient(0, 0, 0, self.navWidget.height())
        # gradient.setColorAt(0, QColor(214, 183, 222, 250))
        # gradient.setColorAt(1, QColor(198, 210, 234, 250))

        gradient.setColorAt(0, QColor(255, 255, 255, 150))
        gradient.setColorAt(1, QColor(255, 255, 255, 150))

        blurEffect = QGraphicsBlurEffect()
        blurEffect.setBlurRadius(200)

        palette = self.navWidget.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.navWidget.setPalette(palette)
        self.navWidget.setGraphicsEffect(blurEffect)

    def setCustomTitleBarBackground(self):
        gradient = QLinearGradient(0, 0, 0, self.titleBar.height())
        # gradient.setColorAt(0, QColor(214, 183, 222, 0))
        # gradient.setColorAt(1, QColor(198, 210, 234, 0))

        gradient.setColorAt(0, QColor(255, 255, 255, 150))
        gradient.setColorAt(1, QColor(255, 255, 255, 150))

        blurEffect = QGraphicsBlurEffect()
        blurEffect.setBlurRadius(1000)

        palette = self.titleBar.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.titleBar.setPalette(palette)
        self.titleBar.setGraphicsEffect(blurEffect)

    def resizeEvent(self, event):
        size = event.size()
        width = self.width()
        height = self.height()

        if width > 1500:
            self.navWidget.setFixedWidth(350)
            self.bodyWidget.setFixedWidth(width - 350)
        elif width > 1200:
            self.navWidget.setFixedWidth(300)
            self.bodyWidget.setFixedWidth(width - 300)
        else:
            self.navWidget.setFixedWidth(250)
            self.bodyWidget.setFixedWidth(width - 250)

        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.resizeDir:
                self.resizing = True
            else:
                self.moving = True

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.moving = False
        self.setCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
