import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGraphicsBlurEffect
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QCursor, QBrush, QLinearGradient
from PySide6.QtCore import Qt, QSize, QRect, QTimer

from BlurWindow.blurWindow import blur

from components.BodyArea import ComponentBodyArea
from components.CustomTitleBar import ComponentCustomTitleBar
from components.FilesBar import ComponentFilesBar
from components.MenuBar import ComponentMenuBar
from components.NavSideBar import ComponentNavSideBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WindowTitle")
        self.setMinimumSize(1200, 750)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        hWnd = self.winId()
        blur(hWnd)

        self.buildUI()
        
        self.setMouseTracking(True)
        self.resizing = False
        self.resizeDir = None

    def buildUI(self):
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        #!Main layout
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        #*Title bar
        self.titleBar = ComponentCustomTitleBar(self)
        mainLayout.addWidget(self.titleBar)
        ComponentCustomTitleBar.setCustomTitleBarBackground(self.titleBar)
        
        #*Files bar
        self.filesBar = ComponentFilesBar(self)
        mainLayout.addWidget(self.filesBar)

        #*Menu bar
        self.menuBar = ComponentMenuBar(self)
        mainLayout.addWidget(self.menuBar)

        #!Content layout
        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)

        #*Nav side bar
        self.navWidget = ComponentNavSideBar(self)

        #*Body area
        self.bodyWidget = ComponentBodyArea(self)

        # webView = QWidget()

        #!Body layout
        bodyLayout = QVBoxLayout(self.bodyWidget)
        bodyLayout.setContentsMargins(0, 0, 0, 0)
        bodyLayout.setSpacing(0)
        # bodyLayout.addWidget(webView)

        contentLayout.addWidget(self.navWidget, 1)
        contentLayout.addWidget(self.bodyWidget, 3)

        mainLayout.addLayout(contentLayout)

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
