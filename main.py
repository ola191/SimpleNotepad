import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QCursor
from PySide6.QtCore import Qt, QSize, QRect, QTimer

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.setPalette(palette)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

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

        self.resizing = False
        self.moving = False
        self.resizeDir = None
        self.click_count = 0
        self.timer = QTimer()
        self.timer.setInterval(500)  # Interval for double/triple click detection
        self.timer.timeout.connect(self.reset_click_count)

    def reset_click_count(self):
        self.click_count = 0
        self.timer.stop()

    def closeWindow(self):
        self.window().close()

    def minimizeWindow(self):
        self.window().showMinimized()

    def maximizeWindow(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPos()
            self.startGeometry = self.window().geometry()
            margins = 5
            pos = event.pos()

            if pos.x() < margins:
                self.resizing = True
                self.resizeDir = "left"
            elif pos.x() > self.width() - margins:
                self.resizing = True
                self.resizeDir = "right"
            elif pos.y() < margins:
                self.resizing = True
                self.resizeDir = "top"
            elif pos.y() > self.height() - margins:
                self.resizing = True
                self.resizeDir = "bottom"
            else:
                self.moving = True
                self.resizeDir = None

            self.click_count += 1
            if self.click_count == 1:
                self.timer.start()
            elif self.click_count == 2:
                self.maximizeWindow()
                self.click_count = 0
                self.timer.stop()
            elif self.click_count == 3:
                self.minimizeWindow()
                self.click_count = 0
                self.timer.stop()

    def mouseMoveEvent(self, event):
        if self.moving:
            delta = event.globalPos() - self.startPos
            new_pos = self.startGeometry.topLeft() + delta
            self.window().move(new_pos)

        if self.resizing:
            delta = event.globalPos() - self.startPos
            rect = QRect(self.startGeometry)

            if self.resizeDir == "left":
                rect.setLeft(rect.left() + delta.x())
            elif self.resizeDir == "right":
                rect.setRight(rect.right() + delta.x())
            elif self.resizeDir == "top":
                rect.setTop(rect.top() + delta.y())
            elif self.resizeDir == "bottom":
                rect.setBottom(rect.bottom() + delta.y())

            self.window().setGeometry(rect)

        else:
            margins = 5
            pos = event.pos()

            if pos.x() < margins:
                self.setCursor(QCursor(Qt.SizeHorCursor))
            elif pos.x() > self.width() - margins:
                self.setCursor(QCursor(Qt.SizeHorCursor))
            elif pos.y() < margins:
                self.setCursor(QCursor(Qt.SizeVerCursor))
            elif pos.y() > self.height() - margins:
                self.setCursor(QCursor(Qt.SizeVerCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = False
            self.resizing = False
            self.setCursor(Qt.ArrowCursor)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WindowTitle")
        self.setMinimumSize(1200, 750)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowIcon(QIcon("icon.png"))
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

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)

        self.navWidget = QWidget()
        self.navWidget.setAutoFillBackground(True)
        navWidgetPallette = self.navWidget.palette()
        navWidgetPallette.setColor(QPalette.Window, QColor(244, 249, 254))
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
            # self.oldPos = event.globalPos()
            # self.oldSize = self.size()
            if self.resizeDir:
                self.resizing = True
            else:
                self.moving = True

    def mouseMoveEvent(self, event):
        # if self.resizing:
        #     delta = event.globalPos() - self.oldPos
        #     if self.resizeDir == "top":
        #         self.setGeometry(self.x(), self.y() + delta.y(), self.width(), self.oldSize.height() - delta.y())
        #     elif self.resizeDir == "bottom":
        #         self.setGeometry(self.x(), self.y(), self.width(), self.oldSize.height() + delta.y())
        #     elif self.resizeDir == "left":
        #         self.setGeometry(self.x() + delta.x(), self.y(), self.oldSize.width() - delta.x(), self.height())
        #     elif self.resizeDir == "right":
        #         self.setGeometry(self.x(), self.y(), self.oldSize.width() + delta.x(), self.height())
        #     elif self.resizeDir == "top_left":
        #         self.setGeometry(self.x() + delta.x(), self.y() + delta.y(), self.oldSize.width() - delta.x(), self.oldSize.height() - delta.y())
        #     elif self.resizeDir == "top_right":
        #         self.setGeometry(self.x(), self.y() + delta.y(), self.oldSize.width() + delta.x(), self.oldSize.height() - delta.y())
        #     elif self.resizeDir == "bottom_left":
        #         self.setGeometry(self.x() + delta.x(), self.y(), self.oldSize.width() - delta.x(), self.oldSize.height() + delta.y())
        #     elif self.resizeDir == "bottom_right":
        #         self.setGeometry(self.x(), self.y(), self.oldSize.width() + delta.x(), self.oldSize.height() + delta.y())
        # else:
        #     pos = event.pos()
        #     margins = 10
        #     if pos.x() < margins and pos.y() < margins:
        #         self.setCursor(Qt.SizeFDiagCursor)
        #         self.resizeDir = "top_left"
        #     elif pos.x() > self.width() - margins and pos.y() < margins:
        #         self.setCursor(Qt.SizeBDiagCursor)
        #         self.resizeDir = "top_right"
        #     elif pos.x() < margins and pos.y() > self.height() - margins:
        #         self.setCursor(Qt.SizeBDiagCursor)
        #         self.resizeDir = "bottom_left"
        #     elif pos.x() > self.width() - margins and pos.y() > self.height() - margins:
        #         self.setCursor(Qt.SizeFDiagCursor)
        #         self.resizeDir = "bottom_right"
        #     elif pos.x() < margins:
        #         self.setCursor(Qt.SizeHorCursor)
        #         self.resizeDir = "left"
        #     elif pos.x() > self.width() - margins:
        #         self.setCursor(Qt.SizeHorCursor)
        #         self.resizeDir = "right"
        #     elif pos.y() < margins:
        #         self.setCursor(Qt.SizeVerCursor)
        #         self.resizeDir = "top"
        #     elif pos.y() > self.height() - margins:
        #         self.setCursor(Qt.SizeVerCursor)
        #         self.resizeDir = "bottom"
        #     else:
        #         self.setCursor(Qt.ArrowCursor)
        #         self.resizeDir = None
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
