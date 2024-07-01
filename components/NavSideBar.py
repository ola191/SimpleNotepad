from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsBlurEffect, QVBoxLayout
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap, QCursor, QBrush, QLinearGradient
from PySide6.QtCore import Qt, QSize, QRect, QTimer

class ComponentNavSideBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
            ("New file", "assets/icons/New.png"),
            ("Open file", "assets/icons/Open.png"),
            ("Save file", "assets/icons/Save.png"),
        ]

        for text, icon_path in buttons:
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

    def setNavBackground(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 200, 225, 100))
        gradient.setColorAt(1, QColor(255, 200, 225, 100))

        blurEffect = QGraphicsBlurEffect()
        blurEffect.setBlurRadius(200)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setGraphicsEffect(blurEffect)
