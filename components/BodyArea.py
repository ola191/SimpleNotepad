from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QObject, Signal, Slot, QThread, QTimer
from PySide6.QtWebChannel import QWebChannel

class Worker(QObject):
    htmlChanged = Signal(str)

    def execute(self, html):
        self.htmlChanged.emit(html)

class ComponentBodyArea(QWidget):
    contentChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.currentFilePath = None
        self.currentContent = "<p>Click here and start typing...</p>"

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.webView = QWebEngineView()
        self.webView.setHtml("""
            <html>
            <head>
                <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        new QWebChannel(qt.webChannelTransport, function(channel) {
                            window.qtbridge = channel.objects.qtbridge;
                            document.body.addEventListener('input', function() {
                                window.qtbridge.contentChanged(document.body.innerHTML);
                            });
                        });
                    });
                </script>
            </head>
            <body contenteditable="true">
                <p>Start - Click here and start typing...</p>
            </body>
            </html>
        """)
        
        self.layout.addWidget(self.webView)

        self.worker = Worker()
        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()

        self.worker.htmlChanged.connect(self.updateHtml)

        self.webChannel = QWebChannel()
        self.webChannel.registerObject("qtbridge", self)
        self.webView.page().setWebChannel(self.webChannel)

    @Slot(str)
    def updateHtml(self, content):
        print("Updating content:", content)
        self.webView.setHtml(content)
    
    def saveFile(self):
        if self.currentFilePath is not None:
            self.webView.page().toHtml(self._saveHtmlContent)
        else:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Notepad Plus Files (*.ntp);;Notepad default Files (*.txt);;All Files (*)", options=options)
            if fileName:
                if not fileName.endswith(".ntp"):
                    fileName += ".ntp"
                try:
                    with open(fileName, "w") as file:
                        file.write(self.currentContent)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"An error ocurred while trying to create the file {fileName}")

    @Slot(str)
    def contentChanged(self, content):
        print("Content changed:", content)
        self.currentContent = content

    def loadNtpContent(self, content, filePath = None):
        try:
            print("Loading content...", content, filePath)
            self.worker.execute(content)
        except Exception as e:
            print(e)
