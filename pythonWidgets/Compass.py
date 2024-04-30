import math
import sys
import random

from PySide6.QtCore import QPointF, QPoint, Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication

cardinalPoint = {"N": 360, "S": 180, "E": 90, "O": 270}


class CompassWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.angleRandom = 0
        print(self.angleRandom)
        self.timer = QTimer()

        self.timer.timeout.connect(self.updateCompass())
        self.timer.start(1000)

    def updateCompass(self):
        self.angleRandom = math.radians(random.randint(0, 360))
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # We draw the compass with a gradient around it
        radius = 0.8 * (min(self.width(), self.height()) / 2)

        centerX = int(self.width() / 2)
        centerY = int(self.height() / 2)

        linearGradient = QLinearGradient(QPointF(0, 0), QPointF(0, radius * 2))
        linearGradient.setColorAt(0, QColor(0xE0, 0xE0, 0xE0))
        linearGradient.setColorAt(0.5, QColor(0x6E, 0x77, 0x74))
        linearGradient.setColorAt(0.51, QColor(0x0a, 0x0e, 0x0a))
        linearGradient.setColorAt(1, QColor(0x0a, 0x08, 0x09))

        painter.setPen(QPen(linearGradient, 8))
        painter.setBrush(QColor(0x21, 0x21, 0x21))
        painter.drawEllipse(QPoint(centerX, centerY), radius, radius)

        # We're about to draw graduations on the compass
        font = painter.font()
        font.setPointSize(16)
        painter.setFont(font)

        angle = (-math.pi / 2) + self.angleRandom
        # randomAngle = random.randint(0, 360)
        declination = 0
        for step in range(12 * 3):
            angle += math.pi / 18
            declination += 10

            painter.setPen(Qt.white)
            painter.setBrush(Qt.white)

            if declination % 9 == 0:
                # drawing the graduations of four cardinal points
                painter.drawPolygon([
                    QPointF(centerX + math.cos(angle - 0.02) * radius * 0.9,
                            centerY + math.sin(angle - 0.02) * radius * 0.9),
                    QPointF(centerX + math.cos(angle - 0.01) * radius * 0.8,
                            centerY + math.sin(angle - 0.01) * radius * 0.8),
                    QPointF(centerX + math.cos(angle + 0.01) * radius * 0.8,
                            centerY + math.sin(angle + 0.01) * radius * 0.8),
                    QPointF(centerX + math.cos(angle + 0.02) * radius * 0.9,
                            centerY + math.sin(angle + 0.02) * radius * 0.9)
                ])
            else:
                # drawing classic compass graduations
                painter.drawLine(
                    QPointF(centerX + math.cos(angle) * radius * 0.85,
                            centerY + math.sin(angle) * radius * 0.85),
                    QPointF(centerX + math.cos(angle) * radius * 0.9,
                            centerY + math.sin(angle) * radius * 0.9)
                )

            if declination % 3 == 0:
                # marking of graduations numbers
                delta = radius * 0.04
                painter.drawText(int(centerX + math.cos(angle) * radius * 1.2) - 10,
                                 int(centerY + math.sin(angle) * radius * 1.2 + delta),
                                 str(0 if declination == 360 else declination)
                                 )

            if declination % 9 == 0:
                # marking of the four cardinal points graduations
                delta = radius * 0.04
                painter.drawText(int(centerX + math.cos(angle) * radius * 0.7) - 8,
                                 int(centerY + math.sin(angle) * radius * 0.7 + delta),
                                 str([key for key, value in cardinalPoint.items() if declination == value][0])
                                 )

            if declination == 360:
                # Drawing of the north arrow
                painter.setPen(QColor(255, 0, 0))
                painter.setBrush(QColor(255, 0, 0, 150))

                painter.drawPolygon([
                    QPointF(centerX + math.cos(angle) * radius * 0.6, centerY + math.sin(angle) * radius * 0.6),
                    QPointF(centerX + math.cos(angle - 1) * radius * 0.1,
                            centerY + math.sin(angle - 1) * radius * 0.1),
                    QPointF(centerX + math.cos(angle + 1) * radius * 0.1,
                            centerY + math.sin(angle + 1) * radius * 0.1)
                ])

            if declination == 180:
                # Drawing of the south arrow
                painter.setPen(QColor(0, 0, 255))
                painter.setBrush(QColor(0, 0, 255, 150))

                painter.drawPolygon([
                    QPointF(centerX + math.cos(angle) * radius * 0.6, centerY + math.sin(angle) * radius * 0.6),
                    QPointF(centerX + math.cos(angle - 1) * radius * 0.1,
                            centerY + math.sin(angle - 1) * radius * 0.1),
                    QPointF(centerX + math.cos(angle + 1) * radius * 0.1,
                            centerY + math.sin(angle + 1) * radius * 0.1)
                ])

        # we draw the internal disk
        painter.setPen(QPen(linearGradient, 8))
        painter.setBrush(QColor(0x21, 0x21, 0x21))
        painter.drawEllipse(QPoint(centerX, centerY), radius * 0.1, radius * 0.1)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Example of a compass design")
        self.resize(600, 600)

        # we instantiate our new compass and add it to the window
        compass = CompassWidget()
        self.setCentralWidget(compass)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
