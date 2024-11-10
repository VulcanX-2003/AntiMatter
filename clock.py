import sys
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QColorDialog
from PyQt5.QtGui import QFont, QColor, QPalette

class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()

        # clock display
        self.clock_label = QLabel(self)
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setFont(QFont("TimesNewRoman", 40, QFont.Bold))
        
        # date and day display
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setFont(QFont("TimesNewRoman", 20, QFont.Normal))
        self.date_label.move(0, 80)  

        # Transparent theme
        palette = QPalette()
        self.setAttribute(Qt.WA_TranslucentBackground)
        palette.setColor(QPalette.WindowText, QColor("#1e1e1e")) 
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Make window borderless and always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.resize(500, 400)

        # Clock Update
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        # Update Date & Time
        self.update_time()

    def update_time(self):
        # Update the current time
        current_time = QTime.currentTime().toString("hh:mm")
        self.clock_label.setText(current_time)
        
        # Update the current date and day
        current_date = QDate.currentDate().toString("dddd, MMMM d, yyyy")
        self.date_label.setText(current_date)

    def mousePressEvent(self, event):
        # Enable dragging the window by holding down the mouse button
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def contextMenuEvent(self, event):
        # Open color picker dialog on right-click
        color = QColorDialog.getColor()
        if color.isValid():
            # Set the color on the clock and date label's palette
            label_palette = self.clock_label.palette()
            label_palette.setColor(QPalette.WindowText, color)
            self.clock_label.setPalette(label_palette)
            self.date_label.setPalette(label_palette)

    def mouseMoveEvent(self, event):
        # Move the window when dragging
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = ClockWidget()
    clock.show()
    sys.exit(app.exec_())
