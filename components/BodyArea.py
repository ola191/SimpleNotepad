from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QObject, Signal, Slot, QThread, QTimer, QCoreApplication

class Worker(QObject):
    htmlChanged = Signal(str)

    def execute(self, html):
        self.htmlChanged.emit(html)

class ComponentBodyArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.webView = QWebEngineView()
        self.webView.setHtml("")
        self.layout.addWidget(self.webView)

        self.worker = Worker()
        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()

        self.worker.htmlChanged.connect(self.updateHtml)

    @Slot(str)
    def updateHtml(self, content):
        print("Updating content:", content)
        self.webView.setHtml(content)

    def loadNtpContent(self, content):
        try:
            print("Loading content...", content)
            self.worker.execute(content)
        except Exception as e:
            print(e)
