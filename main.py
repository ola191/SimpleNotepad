import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap
from PySide6.QtCore import Qt, QSize

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(239, 244, 249))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        # layout.setSpacing(20)
    
        self.windowIcon = QLabel(self)
        self.windowIcon.setPixmap(QPixmap("assets/icons/logo.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.windowIcon)

        self.titleLabel = QLabel("Notepad", self)
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setStyleSheet("font-size: 14px; font-weight: semibold; color: #000000;")
        layout.addWidget(self.titleLabel)

        layout.addStretch()

        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setIcon(QIcon("assets/icons/minimize.png"))
        self.minimizeButton.setFixedSize(QSize(20, 20))
        self.minimizeButton.setIconSize(QSize(12, 12))
        self.minimizeButton.setStyleSheet("background: none; border: none;")
        layout.addWidget(self.minimizeButton)

        layout.addSpacing(20)

        self.maximizeButton = QPushButton(self)
        self.maximizeButton.setIcon(QIcon("assets/icons/maximize.png"))
        self.maximizeButton.setFixedSize(QSize(20, 20))
        self.maximizeButton.setIconSize(QSize(12, 12))
        self.maximizeButton.setStyleSheet("background: none; border: none;")
        layout.addWidget(self.maximizeButton)

        layout.addSpacing(20)

        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon("assets/icons/close.png"))
        self.closeButton.setFixedSize(QSize(20, 20))
        self.closeButton.setIconSize(QSize(12, 12))
        self.closeButton.setStyleSheet("background: none; border: none;")
        layout.addWidget(self.closeButton)

        layout.addSpacing(5)

        self.closeButton.clicked.connect(self.closeWindow)
        self.minimizeButton.clicked.connect(self.minimizeWindow)
        self.maximizeButton.clicked.connect(self.maximizeWindow)

    def closeWindow(self):
        self.window().close()

    def minimizeWindow(self):
        self.window().showMinimized()

    def maximizeWindow(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WindowTitle")
        self.setMinimumSize(1200, 750)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowIcon(QIcon("icon.png"))
        self.buildUI()

    def buildUI(self):
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.titleBar = CustomTitleBar(self)
        mainLayout.addWidget(self.titleBar)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)

        self.navWidget = QWidget()
        self.navWidget.setAutoFillBackground(True)
        navWidgetPallette = self.navWidget.palette()
        navWidgetPallette.setColor(QPalette.Window, QColor(225, 225, 225))
        self.navWidget.setPalette(navWidgetPallette)

        navLayout = QVBoxLayout(self.navWidget)
        navLayout.setContentsMargins(10,10,10,10)
        navLayout.setSpacing(10)

        username = os.getlogin()
        titleLabel = QLabel(f"{username}")
        titleLabel.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        navLayout.addWidget(titleLabel)

        buttons = ["New File", "Open File", "Save File", "Close File", "Settings"]
        for button in buttons:
            btn = QPushButton(button)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(235, 235, 235);
                    border-radius: 5px;
                    padding: 10px;
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
        bodyWidgetPallette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.bodyWidget.setPalette(bodyWidgetPallette)

        contentLayout.addWidget(self.navWidget, 1)
        contentLayout.addWidget(self.bodyWidget, 3)

        mainLayout.addLayout(contentLayout)

    def resizeEvent(self, event):
        size = event.size()
        width = self.width()
        height = self.height()

        if width > 1500:
            self.navWidget.setFixedWidth(400)
            self.bodyWidget.setFixedWidth(width - 400)
        elif width > 1200:
            self.navWidget.setFixedWidth(350)
            self.bodyWidget.setFixedWidth(width - 350)
        else:
            self.navWidget.setFixedWidth(width / 4)
            self.bodyWidget.setFixedWidth(width /4 *3)

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
