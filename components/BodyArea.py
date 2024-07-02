from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QObject, Signal, Slot, QThread

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
        self.webView.setHtml("""
            <html contenteditable="true">
            <body>
                <p>Click here and start typing...</p>
            </body>
            </html>
        """)
        self.layout.addWidget(self.webView)

        self.worker = Worker()
        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()

        self.worker.htmlChanged.connect(self.updateHtml)

        self.webView.page().runJavaScript("""
            document.body.addEventListener('input', function() {
                window.qtbridge.contentChanged(document.body.innerHTML);
            });
        """)

        self.webView.page().setWebChannel(self.createWebChannel())

    def createWebChannel(self):
        from PySide6.QtWebChannel import QWebChannel
        channel = QWebChannel()
        channel.registerObject("qtbridge", self)
        return channel

    @Slot(str)
    def updateHtml(self, content):
        print("Updating content:", content)
        self.webView.setHtml(content)

    @Slot(str)
    def contentChanged(self, content):
        print("Content changed:", content)

    def loadNtpContent(self, content):
        try:
            print("Loading content...", content)
            self.worker.execute(content)
        except Exception as e:
            print(e)
