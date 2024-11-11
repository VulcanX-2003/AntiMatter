![Banner](../resources/logo.png)



# AntiMatter

AntiMatter is an alternative to Rainmeter, designed for users who want customizable widgets on their desktop. Currently, AntiMatter includes a sleek clock widget that displays the date, day, and time, with options to change the font color.

## Features

- **Clock Widget**: Displays the current date, day, and time.
- **Customization**: Allows users to change the font color for a personalized look.

## Getting Started

To build and run the project, you need to set up an environment with the required dependencies.

### Prerequisites

- **PyQt5**: Used for the widget's graphical interface.
- **PyInstaller**: For building the project into an executable.

### Installation

1. **Set up the environment**  
   Create a Python virtual environment:
   ```bash
   python -m venv antimatter-env
   source antimatter-env/bin/activate  for LINUX
   use antimatter-env\Scripts\activate for Windows
   pip install PyQt5 

2. **Creating a executable for Windows**
    ```bash
    pyinstaller --onefile clock.py


