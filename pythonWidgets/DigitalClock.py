import sys

from PySide6.QtCore import QDateTime, QLocale, QTimer
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPen, Qt, QFont
from PySide6.QtWidgets import QMainWindow, QApplication


class DigitalClockWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark = "#3B3A44"
        self.light = "#4a4953"
        self.green = "#75ECB5"

        self.timer = QTimer()
        self.timer.setInterval(1000)

        self.timer.timeout.connect(self.update)
        self.timer.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        datetime = QDateTime().currentDateTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Drawing the base circle
        baseRect = self.rect().adjusted(20, 20, -20, -20)
        painter.setPen(QColor(self.dark))
        painter.setBrush(QColor(self.dark))
        painter.drawEllipse(baseRect)

        # Draw the arc path
        pen = QPen(QColor(self.light))
        pen.setWidth(25)
        painter.setPen(pen)
        arcRect = self.rect().adjusted(50, 50, -50, -50)
        painter.drawEllipse(arcRect)

        # Draw active arc
        pen.setColor(QColor(self.green))
        pen.setCapStyle(Qt.RoundCap)
        startAngle = 90
        spanAngle = self.secondToAngle(datetime.time().second())
        painter.setPen(pen)
        painter.drawArc(arcRect, startAngle * 16, spanAngle * 16)

        # Instantiate date
        time = datetime.toString("hh:mm")
        day = datetime.toString("dddd")
        date = datetime.toString("dd/MM/yyyy")
        second = datetime.toString("ss")

        painter.setPen(Qt.white)
        font = QFont()

        # Draw hour
        font.setPixelSize(90)
        painter.setFont(font)
        painter.drawText(arcRect, Qt.AlignCenter, time)

        # Draw day
        font.setPointSize(20)
        painter.setFont(font)
        arcRect.moveTop(-80)
        painter.drawText(arcRect, Qt.AlignCenter | Qt.AlignBottom, day)

        # Draw date
        arcRect.moveTop(-20)
        painter.drawText(arcRect, Qt.AlignCenter | Qt.AlignBottom, date)

        # Draw second
        painter.setPen(QPen(self.green))
        arcRect.moveTop(-120)
        painter.drawText(arcRect, Qt.AlignCenter | Qt.AlignTop, second)

    def secondToAngle(self, second):
        return -second * 360 / 60


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(600, 600)

        # We instantiate the new widget and add it to the window
        clock = DigitalClockWidget()
        self.setCentralWidget(clock)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
