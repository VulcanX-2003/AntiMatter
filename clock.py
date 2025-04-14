import sys
import json
import os
import shutil
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_user_config_path():
    """Get the path for the user's config file in a writable location"""
    app_name = "AntimatterClock"
    if sys.platform.startswith('win'):
        app_data = os.path.join(os.environ['APPDATA'], app_name)
    elif sys.platform.startswith('darwin'):  # macOS
        app_data = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', app_name)
    else:  # Linux and others
        app_data = os.path.join(os.path.expanduser('~'), '.config', app_name)
    
    # Ensure directory exists
    os.makedirs(app_data, exist_ok=True)
    return os.path.join(app_data, 'config.json')


class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Get the path to the user's config file
        self.config_file = get_user_config_path()
        
        # Initialize config file if it doesn't exist
        self.initialize_config()
        
        # Load the config
        self.load_config()

        # Clock display
        self.clock_label = QLabel(self)
        self.clock_label.setAlignment(Qt.AlignCenter)
        
        # Date and day display
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignCenter)
        
        # Apply initial styling
        self.apply_styling()

        # Transparent theme
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        # Make window borderless and set as a tool window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint)
        self.resize(500, 400)

        # Clock Update
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        # Watch for config file changes
        self.file_watch_timer = QTimer(self)
        self.file_watch_timer.timeout.connect(self.check_config_changes)
        self.file_watch_timer.start(1000)  # Check every second

        # Update Date & Time
        self.update_time()
    
    def initialize_config(self):
        """Initialize the config file if it doesn't exist"""
        if not os.path.exists(self.config_file):
            # Try to copy the bundled config if it exists
            bundled_config = resource_path("config.json")
            try:
                if os.path.exists(bundled_config):
                    shutil.copy(bundled_config, self.config_file)
                else:
                    # Create default config
                    default_config = {
                        "clock_text": {
                            "color": "#fefefe",
                            "position": {"x": 0, "y": 0},
                            "font_size": 120,
                            "format": "hh:mm:ss",
                            "font": "Technology"
                        },
                        "date_text": {
                            "color": "#fefefe",
                            "position": {"x": 0, "y": 130},
                            "font_size": 35,
                            "format": "dddd, MMMM d,yyyy",
                            "font": "Technology"
                        }
                    }
                    with open(self.config_file, 'w') as f:
                        json.dump(default_config, f, indent=4)
            except Exception as e:
                print(f"Error initializing config: {e}")
        
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            # Use default values if config file cannot be loaded
            self.config = {
                "clock_text": {
                    "color": "#fefefe",
                    "position": {"x": 0, "y": 0},
                    "font_size": 120,
                    "format": "hh:mm:ss",
                    "font": "Technology"
                },
                "date_text": {
                    "color": "#fefefe",
                    "position": {"x": 0, "y": 130},
                    "font_size": 35,
                    "format": "dddd, MMMM d,yyyy",
                    "font": "Technology"
                }
            }
            # Write default config
            try:
                with open(self.config_file, 'w') as f:
                    json.dump(self.config, f, indent=4)
            except Exception as write_error:
                print(f"Error writing default config: {write_error}")

    def apply_styling(self):
        # Apply clock styling
        clock_config = self.config["clock_text"]
        self.clock_label.setFont(QFont(clock_config["font"], clock_config["font_size"], QFont.Bold))
        self.clock_label.move(clock_config["position"]["x"], clock_config["position"]["y"])
        clock_palette = self.clock_label.palette()
        clock_palette.setColor(QPalette.WindowText, QColor(clock_config["color"]))
        self.clock_label.setPalette(clock_palette)

        # Apply date styling
        date_config = self.config["date_text"]
        self.date_label.setFont(QFont(date_config["font"], date_config["font_size"], QFont.Normal))
        self.date_label.move(date_config["position"]["x"], date_config["position"]["y"])
        date_palette = self.date_label.palette()
        date_palette.setColor(QPalette.WindowText, QColor(date_config["color"]))
        self.date_label.setPalette(date_palette)

    def check_config_changes(self):
        # Only reload if the file has been modified
        try:
            self.load_config()
            self.apply_styling()
        except Exception as e:
            print(f"Error checking config changes: {e}")

    def update_time(self):
        # Update the current time using format from config
        clock_format = self.config["clock_text"]["format"]
        current_time = QTime.currentTime().toString(clock_format)
        self.clock_label.setText(current_time)

        # Update the current date and day using format from config
        date_format = self.config["date_text"]["format"]
        current_date = QDate.currentDate().toString(date_format)
        self.date_label.setText(current_date)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()


def main():
    app = QApplication(sys.argv)
    
    clock = ClockWidget()
    clock.show()

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "System Tray", "System tray not available on this system")
        sys.exit(1)

    # Use resource_path to find the icon
    icon_path = resource_path("resources/icon.png")
    tray_icon = QSystemTrayIcon(QIcon(icon_path))
    tray_icon.setToolTip("Antimatter Clock")

    menu = QMenu()

    # Add Edit Config option with improved error handling
    edit_config_action = QAction("Edit Config")
    def open_config():
        try:
            config_path = clock.config_file
            # Show a message indicating where the config file is located
            QMessageBox.information(None, "Config Location", 
                                   f"The config file is located at:\n{config_path}")
            
            # Use the appropriate text editor based on platform
            if sys.platform.startswith('win'):
                os.startfile(config_path)  # Use Windows default editor
            elif sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['open', config_path])
            else:  # Linux and others
                # Try some common text editors
                editors = ['xdg-open', 'gedit', 'kate', 'nano', 'vim', 'vi']
                for editor in editors:
                    try:
                        subprocess.run([editor, config_path], check=False)
                        break
                    except FileNotFoundError:
                        continue
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Could not open config file: {e}")
    
    edit_config_action.triggered.connect(open_config)
    menu.addAction(edit_config_action)

    menu.addSeparator()  # Add separator line

    open_action = QAction("Show Clock")
    open_action.triggered.connect(clock.show)
    menu.addAction(open_action)

    hide_action = QAction("Hide Clock")
    hide_action.triggered.connect(clock.hide)
    menu.addAction(hide_action)

    menu.addSeparator()  # Add separator line

    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)

    tray_icon.setContextMenu(menu)
    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()