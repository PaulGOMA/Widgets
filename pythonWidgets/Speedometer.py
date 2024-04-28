import math
import sys

from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen
from PySide6.QtCore import QPoint, Qt, QPointF, Slot
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QHBoxLayout, QSlider, QVBoxLayout, QCheckBox

MAX_SPEED = 320


class SpeedWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.__speed = 0
        self.__maxSpeed = 130
        self.__limiter = False

    @Slot(int)
    def setSpeed(self, speed: int):
        self.__speed = speed
        if self.__limiter and self.__speed > self.__maxSpeed:
            self.__speed = self.__maxSpeed
        self.repaint()

    @Slot(int)
    def setMaxSpeed(self, speed: int):
        self.__maxSpeed = speed
        if self.__speed > self.__maxSpeed:
            self.__speed = self.__maxSpeed
        self.repaint()

    @Slot(bool)
    def setLimiter(self, value: bool):
        self.__limiter = value
        if value and self.__speed > self.__maxSpeed:
            self.__speed = self.__maxSpeed
        self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        radius = 0.95 * (min(self.width(), self.height()) / 2)

        centerX = int(self.width() / 2)
        centerY = int(self.height() / 2)
        # print("Center", centerX, centerY)

        linearGradient = QLinearGradient(QPointF(0, 0), QPointF(0, radius*2))
        linearGradient.setColorAt(0, QColor(0xE0, 0xE0, 0xE0))
        linearGradient.setColorAt(0.5, QColor(0x6E, 0x77, 0x74))
        linearGradient.setColorAt(0.51, QColor(0x0a, 0x0e, 0x0a))
        linearGradient.setColorAt(1, QColor(0x0a, 0x08, 0x09))

        linearGradient2 = QLinearGradient(QPointF(0, 0), QPointF(0, radius*2))
        linearGradient2.setColorAt(0, QColor(0x21, 0x21, 0x21))
        linearGradient2.setColorAt(1, QColor(0x0a, 0x08, 0x09))

        painter.setPen(QPen(linearGradient, 8))
        painter.setBrush(QColor(0x21, 0x21, 0x21))
        painter.drawEllipse(QPoint(centerX, centerY), radius, radius)

        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)

        # On trace les graduations externes
        angleStart = -5 * math.pi / 4
        for speed in range(0, MAX_SPEED + 1, 2):
            angle = angleStart + math.radians(speed / MAX_SPEED * 240)

            painter.setPen(Qt.white)
            painter.setBrush(Qt.white)

            if speed % 20 == 0:
                painter.setPen(QPen(Qt.white, 3))
                painter.drawLine(
                    QPointF(centerX + math.cos(angle) * radius * 0.92,
                            centerY + math.sin(angle) * radius * 0.92),
                    QPointF(centerX + math.cos(angle) * radius * 0.95,
                            centerY + math.sin(angle) * radius * 0.95)
                )

                delta = radius * 0.03
                painter.drawText(int(centerX + math.cos(angle) * radius * 0.8) - 24,
                                 int(centerY + math.sin(angle) * radius * 0.8 + delta),
                                 str(speed))
            elif speed % 10 == 0:
                painter.setPen(QPen(Qt.white, 2))
                painter.drawLine(
                    QPointF(centerX + math.cos(angle) * radius * 0.92,
                            centerY + math.sin(angle) * radius * 0.92),
                    QPointF(centerX + math.cos(angle) * radius * 0.95,
                            centerY + math.sin(angle) * radius * 0.95)
                )

            else:
                painter.setPen(QPen(Qt.gray, 1))
                painter.drawLine(
                    QPointF(centerX + math.cos(angle) * radius * 0.92,
                            centerY + math.sin(angle) * radius * 0.92),
                    QPointF(centerX + math.cos(angle) * radius * 0.95,
                            centerY + math.sin(angle) * radius * 0.95)
                )

        # On dessine le disque interne et ses graduation
        painter.setPen(QPen(linearGradient2, 8))
        painter.setBrush(QColor(0x21, 0x21, 0x21))
        painter.drawEllipse(QPoint(centerX, centerY), radius * 0.64, radius * 0.64)

        for speed in range(0, MAX_SPEED + 1, 2):
            angle = angleStart + math.radians(speed / MAX_SPEED * 240)

            painter.setPen(Qt.white)
            painter.setBrush(Qt.white)

            if speed % 20 == 0:
                painter.setPen(QPen(Qt.white, 3))
                painter.drawLine(
                    QPointF(centerX + math.cos(angle) * radius * 0.62,
                            centerY + math.sin(angle) * radius * 0.62),
                    QPointF(centerX + math.cos(angle) * radius * 0.66,
                            centerY + math.sin(angle) * radius * 0.66)
                )

            elif speed % 10 == 0:
                painter.setPen(QPen(Qt.white, 2))
                painter.drawLine(
                    QPointF(centerX + math.cos(angle) * radius * 0.62,
                            centerY + math.sin(angle) * radius * 0.62),
                    QPointF(centerX + math.cos(angle) * radius * 0.66,
                            centerY + math.sin(angle) * radius * 0.66)
                )

            else:
                painter.setPen(QPen(Qt.gray, 1))
                painter.drawLine(
                    QPointF(centerX + math.cos(angle) * radius * 0.62,
                            centerY + math.sin(angle) * radius * 0.62),
                    QPointF(centerX + math.cos(angle) * radius * 0.66,
                            centerY + math.sin(angle) * radius * 0.66)
                )

        # On dessine l'aiguille de vitesse
        painter.setPen(QColor(255, 0, 0))
        painter.setBrush(QColor(255, 0, 0, 150))

        angle = angleStart + math.radians(self.__speed / MAX_SPEED * 240)

        painter.drawPolygon([
            QPointF(centerX + math.cos(angle) * radius * 0.93, centerY + math.sin(angle) * radius * 0.93),
            QPointF(centerX + math.cos(angle - 0.4) * radius * 0.1, centerY + math.sin(angle - 0.4) * radius * 0.1),
            QPointF(centerX + math.cos(angle + 0.4) * radius * 0.1, centerY + math.sin(angle + 0.4) * radius * 0.1)
        ])

        # Doit-on afficher le marqueur pour le limiteur de vitesse
        if self.__limiter:
            angle = angleStart + math.radians(self.__maxSpeed / MAX_SPEED * 240)

            painter.setPen(QColor(0xfd, 0x56, 0x02))
            painter.setBrush(QColor(0xfd, 0x56, 0x02, 200))

            painter.drawPolygon([
                QPointF(centerX + math.cos(angle) * radius * 0.95, centerY + math.sin(angle) * radius * 0.95),
                QPointF(centerX + math.cos(angle - 0.03) * radius, centerY + math.sin(angle - 0.03) * radius),
                QPointF(centerX + math.cos(angle + 0.03) * radius, centerY + math.sin(angle + 0.03) * radius)
            ])

        painter.setPen(Qt.white)
        painter.drawText(centerX - 20, int(self.height() * 0.65), "Km/h")

        # On dessine le disque le plus interne
        painter.setPen(QPen(linearGradient, 8))
        painter.setBrush(QColor(0x21, 0x21, 0x21))
        painter.drawEllipse(QPoint(centerX, centerY), radius * 0.18, radius * 0.18)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Example of a speedometer design")
        self.resize(640, 600)

        widget = QWidget()
        hBox = QHBoxLayout()
        speedWidget = SpeedWidget()

        hBox.addWidget(speedWidget)
        global slider
        slider = QSlider(Qt.Vertical)
        slider.setMinimum(0)
        slider.setMaximum(MAX_SPEED)
        hBox.addWidget(slider)

        chkLimiter = QCheckBox("Activate limiter")
        slider2 = QSlider(Qt.Horizontal)
        slider2.setMinimum(0)
        slider2.setValue(130)
        slider2.setMaximum(MAX_SPEED)

        hBox2 = QHBoxLayout()
        hBox2.addWidget(chkLimiter)
        hBox2.addWidget(slider2)

        vBox = QVBoxLayout()
        vBox.addLayout(hBox)
        vBox.addLayout(hBox2)

        widget.setLayout(vBox)
        self.setCentralWidget(widget)

        slider.valueChanged.connect(speedWidget.setSpeed)
        chkLimiter.stateChanged.connect(speedWidget.setLimiter)
        slider2.valueChanged.connect(speedWidget.setMaxSpeed)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())