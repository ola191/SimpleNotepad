import json
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog, QProgressBar
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtWebChannel import QWebChannel

CONFIG_FILE = "configs/files.json"

class Worker(QObject):
    htmlChanged = Signal(str)

    def execute(self, html):
        self.htmlChanged.emit(html)

class ComponentBodyArea(QWidget):
    contentChanged = Signal(str)
    fileSizeUpdated = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.currentFilePath = None
        self.currentContent = "<p>Click here and start typing...</p>"
        self.totalFileSizes = []

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

        self.loadFilePaths()

    @Slot(str)
    def updateHtml(self, content):
        self.currentContent = content
        if '<body contenteditable="true">' not in content:
            content = content.replace("<body", '<body contenteditable="true"')
        self.webView.setHtml(content)

    def saveFile(self):
        self.toHtml(save=True)

    def saveFileContent(self):
        if self.currentFilePath is not None:
            with open(self.currentFilePath, "w") as file:
                file.write(self.currentContent)
            self.saveFilePath(self.currentFilePath)
        else:
            options = QFileDialog.Options()
            documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
            fileName, _ = QFileDialog.getSaveFileName(self, "Save file", documents_dir, "Notepad Plus Files (*.ntp);;Notepad default Files (*.txt);;All Files (*)", options=options)
            if fileName:
                if not fileName.endswith(".ntp"):
                    fileName += ".ntp"
                try:
                    with open(fileName, "w") as file:
                        file.write(self.currentContent)
                    self.currentFilePath = fileName
                    self.saveFilePath(self.currentFilePath)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"An error occurred while trying to create the file {fileName}")

    @Slot(str)
    def contentChanged(self, content):
        self.currentContent = content
        self.calculateTotalSize(content)

    def calculateTotalSize(self, content):
        file_size_kb = len(content.encode('utf-8')) / 1024
        self.totalFileSizes.append(file_size_kb)
        # total_size_kb = sum(self.totalFileSizes)
        self.fileSizeUpdated.emit(file_size_kb)

    def callbackFunc(self, html):
        self.currentContent = html
        self.saveFileContent()

    def toHtml(self, save=False):
        if save:
            self.webView.page().runJavaScript(
                "document.getElementsByTagName('html')[0].innerHTML", 0, self.callbackFunc
            )
        else:
            self.webView.page().runJavaScript(
                "document.getElementsByTagName('html')[0].innerHTML", 0, self.updateHtml
            )

    def loadNtpContent(self, content, filePath=None):
        try:
            self.worker.execute(content)
            self.currentFilePath = filePath
        except Exception as e:
            print(e)

    def saveFilePath(self, filePath):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            file_size_kb = os.path.getsize(filePath) / 1024
            file_info = {"path": filePath, "size_kb": file_size_kb}

            for item in data:
                if item["path"] == filePath:
                    item["size_kb"] = file_size_kb
                    break
            else:
                data.append(file_info)

            with open(CONFIG_FILE, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving file path: {e}")

    def loadFilePaths(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as file:
                    try:
                        data = json.load(file)
                        for item in data:
                            print(f"Previously saved file: {item['path']} ({item['size_kb']} kB)")
                            self.totalFileSizes.append(item['size_kb'])
                    except json.JSONDecodeError:
                        print("Error loading file paths: JSONDecodeError - the file is empty or corrupted.")
        except Exception as e:
            print(f"Error loading file paths: {e}")
