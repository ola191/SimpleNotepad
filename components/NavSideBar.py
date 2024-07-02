from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsBlurEffect, QVBoxLayout, QFileDialog, QMessageBox 
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QCursor, QBrush, QLinearGradient
from PySide6.QtCore import Qt, QSize, QRect, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView

from components.BodyArea import ComponentBodyArea

class ComponentNavSideBar(QWidget):
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.bodyArea = mainWindow.bodyWidget

        self.setAutoFillBackground(True)
        navWidgetPallette = self.palette()
        navWidgetPallette.setColor(QPalette.Window, QColor(244, 249, 254, 60))
        self.setPalette(navWidgetPallette)
        self.setNavBackground()

        navMainLayout = QVBoxLayout(self)
        navMainLayout.setContentsMargins(0, 0, 0, 0)
        navMainLayout.setSpacing(0)

        navContentLayout = QVBoxLayout()
        navContentLayout.setContentsMargins(10, 10, 10, 10) 
        navContentLayout.setSpacing(10)

        filesLabel = QLabel("Files")
        filesLabel.setStyleSheet("font-size: 12pt; font-weight: semibold;")
        navContentLayout.addWidget(filesLabel)

        buttons = [
            ("New file", "assets/icons/New.png", self.newFile),
            ("Open file", "assets/icons/Open.png", self.openFile),
            ("Save file", "assets/icons/Save.png", self.saveFile),
        ]

        for text, icon_path, callback in buttons:
            btn = QPushButton(f" {text}")
            btn.setIcon(QIcon(icon_path))
            btn.setContentsMargins(15, 0, 0, 0)
            btn.setIconSize(QSize(20, 20))  
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
            btn.setLayoutDirection(Qt.LeftToRight)
            btn.clicked.connect(callback)
            navContentLayout.addWidget(btn)
        navContentLayout.addStretch()

        bottomWidget = QWidget()
        bottomWidget.setFixedHeight(64) 
        bottomWidget.setAutoFillBackground(True)
        bottomPalette = bottomWidget.palette()
        bottomPalette.setColor(QPalette.Window, QColor(244, 249, 254, 60))
        bottomWidget.setPalette(bottomPalette)
        bottomWidget.setGraphicsEffect(QGraphicsBlurEffect())

        shadow = QGraphicsBlurEffect()
        shadow.setBlurRadius(20)
        bottomWidget.setGraphicsEffect(shadow)

        navMainLayout.addLayout(navContentLayout)
        navMainLayout.addWidget(bottomWidget)

    def newFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Create new file", "", "Notepad Plus Files (*.ntp);;Notepad default Files (*.txt);;All Files (*)", options=options)
        if fileName:
            if not fileName.endswith(".ntp"):
                fileName += ".ntp"
            content = """

<h1>New World</h1>

            """
            try:
                with open(fileName, "w") as file:
                    file.write(content)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error ocurred while trying to create the file {fileName}")


    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Notepad Plus Files (*.ntp);;Notepad default Files (*.txt);;All Files (*)", options=options)
        if fileName:
            try:
                with open(fileName, "r") as file:
                    content = file.read()
                    QTimer.singleShot(0, lambda: self.bodyArea.loadNtpContent(content))
            except Exception as e:
                QMessageBox.information(self, "File opened", f"File {fileName} opened")

    def saveFile(self):
        self.bodyArea.loadNtpContent("ababbaba")


    def setNavBackground(self):
        startPosY = self.height() + 200
        gradient = QLinearGradient(0, startPosY, 0, 400)
        gradient.setColorAt(0, QColor(255, 200, 225, 100))
        gradient.setColorAt(1, QColor(255, 175, 200, 159))

        blurEffect = QGraphicsBlurEffect()
        blurEffect.setBlurRadius(200)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setGraphicsEffect(blurEffect)
