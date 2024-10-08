from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsBlurEffect, QDialog, QGridLayout
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QCursor, QBrush, QLinearGradient
from PySide6.QtCore import Qt, QSize, QRect, QTimer, QPoint

class ComponentCustomTitleBar(QWidget):
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.setFixedHeight(32)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.setPalette(palette)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)

        self.windowIcon = QLabel(self)
        self.windowIcon.setPixmap(QPixmap("assets/icons/logo.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.windowIcon)

        self.titleLabel = QLabel("Notepad :", self)
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setStyleSheet("font-size: 14px; font-weight: semibold; color: #000000;")
        self.layout.addWidget(self.titleLabel)

        self.fileNameTitle = QLabel("empty", self)
        self.fileNameTitle.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.fileNameTitle.setStyleSheet("font-size: 14px; font-weight: semibold; color: #000000;")
        self.layout.addWidget(self.fileNameTitle)

        self.layout.addStretch()

        self.minimizeButton = QPushButton(self)
        self.minimizeButton.setIcon(QIcon("assets/icons/minimize.png"))
        self.minimizeButton.setFixedSize(QSize(32, 32))
        self.minimizeButton.setIconSize(QSize(12, 12))
        self.minimizeButton.setStyleSheet("background: none; border: none;")
        self.layout.addWidget(self.minimizeButton)

        self.layout.addSpacing(15)

        self.maximizeButton = QPushButton(self)
        self.maximizeButton.setIcon(QIcon("assets/icons/maximize.png"))
        self.maximizeButton.setFixedSize(QSize(32, 32))
        self.maximizeButton.setIconSize(QSize(12, 12))
        self.maximizeButton.setStyleSheet("background: none; border: none;")
        self.layout.addWidget(self.maximizeButton)

        self.layout.addSpacing(15)

        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon("assets/icons/close.png"))
        self.closeButton.setFixedSize(QSize(32, 32))
        self.closeButton.setIconSize(QSize(12, 12))
        self.closeButton.setStyleSheet("""
                QPushButton {
                    background-color: none;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #D9759B;
                    border: 1px solid #C2567F;
                }
            """)
        self.layout.addWidget(self.closeButton)

        self.layout.addSpacing(5)

        self.closeButton.clicked.connect(self.closeWindow)
        self.minimizeButton.clicked.connect(self.minimizeWindow)
        self.maximizeButton.clicked.connect(self.maximizeWindow)

        self.resizing = False
        self.moving = False
        self.resizeDir = None
        self.click_count = 0
        self.timer = QTimer()
        self.timer.setInterval(500) 
        self.timer.timeout.connect(self.resetClickCount)

    def resetClickCount(self):
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

    def setCustomTitleBarBackground(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 200, 225, 100))
        gradient.setColorAt(1, QColor(255, 200, 225, 100))

        blurEffect = QGraphicsBlurEffect()
        blurEffect.setBlurRadius(200)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setGraphicsEffect(blurEffect)

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
        elif event.button() == Qt.RightButton:
            if self.childAt(event.pos()) == self.maximizeButton:

                self.gridWidget = QWidget(self)
                self.gridWidget.setStyleSheet("background-color: rgba(255, 255, 255, 0.9);")
                self.gridWidget.setFixedSize(170, 170)

                self.gridLayout = QGridLayout(self.gridWidget)
                self.gridLayout.setSpacing(10)

                for i in range(3):
                    for j in range(3):
                        btn = QPushButton(self.gridWidget)
                        btn.setFixedSize(50, 50)
                        btn.setStyleSheet("""
                            QPushButton {
                                background-color: #A9A9A9;
                                border-radius: 10px;
                                border: 1px solid #000000;
                            }
                        """)
                        self.gridLayout.addWidget(btn, i, j)

                cursorPos = self.mapFromGlobal(event.globalPos())
                self.gridWidget.move(QPoint(self.childAt(event.pos()).pos().x() - 150, 20))
                self.gridWidget.show()

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