import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QIcon, QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WindowTitle")
        self.setMinimumSize(1200,750)
        # self.setWindowIcon(QIcon("icon.png"))
        self.buildUI()

    def buildUI(self):
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        
        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)

        self.navWidget = QWidget()
        self.navWidget.setAutoFillBackground(True)
        navWidgetPallette = self.navWidget.palette()
        navWidgetPallette.setColor(QPalette.Window, QColor(215, 215, 215))
        self.navWidget.setPalette(navWidgetPallette)

        self.bodyWidget = QWidget()
        self.bodyWidget.setAutoFillBackground(True)
        bodyWidgetPallette = self.bodyWidget.palette()
        bodyWidgetPallette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.bodyWidget.setPalette(bodyWidgetPallette)

        mainLayout.addWidget(self.navWidget, 1)
        mainLayout.addWidget(self.bodyWidget, 3)

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