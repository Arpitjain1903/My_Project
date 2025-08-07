import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton, QWidget, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QIcon("Python_program/python_simple project/icon.png")) # Place your icon in the same folder

        # When the result is an error, this flag is set. The next digit press will clear the display.
        self.is_error_state = False

        # --- Main Layout and Widget ---
        # All widgets go into a central widget, which is then set for the main window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # The main layout is a vertical box layout to hold the display and the button grid
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- UI Elements ---
        self._create_display()
        self._create_buttons()
        self._apply_styles()

    def _create_display(self):
        """Creates the calculator's display (QLineEdit)."""
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True) # Make it read-only for user input
        self.main_layout.addWidget(self.display)

    def _create_buttons(self):
        """Creates all buttons and adds them to a grid layout."""
        self.buttons = {}
        buttons_layout = QGridLayout()

        # A map of button text to its grid position (row, column, row span, column span)
        # This makes the layout extremely easy to read and modify
        buttons_map = {
            'AC': (0, 0, 1, 1), 'C': (0, 1, 1, 1), '%': (0, 2, 1, 1), '/': (0, 3, 1, 1),
            '7': (1, 0, 1, 1), '8': (1, 1, 1, 1), '9': (1, 2, 1, 1), '×': (1, 3, 1, 1),
            '4': (2, 0, 1, 1), '5': (2, 1, 1, 1), '6': (2, 2, 1, 1), '-': (2, 3, 1, 1),
            '1': (3, 0, 1, 1), '2': (3, 1, 1, 1), '3': (3, 2, 1, 1), '+': (3, 3, 1, 1),
            '0': (4, 0, 1, 2), '00': (4, 2, 1, 1), '=': (4, 3, 1, 1),
        }

        for text, pos in buttons_map.items():
            button = QPushButton(text)
            self.buttons[text] = button
            buttons_layout.addWidget(button, pos[0], pos[1], pos[2], pos[3])
            button.clicked.connect(self._on_button_click)
        
        self.main_layout.addLayout(buttons_layout)

    def _on_button_click(self):
        """General handler for all button clicks."""
        button_text = self.sender().text()

        # Clear display on new input if the last result was an error
        if self.is_error_state:
            self.display.clear()
            self.is_error_state = False

        if button_text == '=':
            self._calculate_result()
        elif button_text == 'AC':
            self.display.clear()
        elif button_text == 'C':
            self.display.setText(self.display.text()[:-1])
        elif button_text == '%':
            self._calculate_percentage()
        else:
            self.display.setText(self.display.text() + button_text)
            
    def _calculate_result(self):
        """Evaluates the expression in the display."""
        try:
            expression = self.display.text().replace('×', '*')
            result = str(eval(expression))
            self.display.setText(result)
        except Exception:
            self.display.setText("Error")
            self.is_error_state = True
            
    def _calculate_percentage(self):
        """Calculates percentage based on the expression."""
        try:
            expression = self.display.text()
            # A simple implementation: treat the last number as a percentage of the first
            # For example: "100+10%" becomes 100+10
            # For a more robust solution, a proper math expression parser would be needed
            if expression:
                # Replace 'x' with '*' to make it valid for eval
                parts = expression.replace('×', '*').split('*')
                if len(parts) > 1:
                    base_value = eval(''.join(parts[:-1]))
                    percent_value = float(parts[-1])
                    result = base_value * (percent_value / 100)
                    self.display.setText(str(result))
                else:
                    self.display.setText(str(float(expression)/100))
        except Exception:
            self.display.setText("Error")
            self.is_error_state = True

    def _apply_styles(self):
        """Applies fonts and stylesheets to the widgets."""
        self.setMinimumSize(400, 500)
        display_font = QFont('Arial', 32, QFont.Bold)
        self.display.setFont(display_font)
        self.display.setStyleSheet("color: #fff; background-color: #9575cd; border-radius: 10px; border: 2px solid #b39ddb; padding: 5px;")
        
        self.setStyleSheet("background-color: #7e57c2;")
        
        button_style = """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ede7f6, stop:1 #b39ddb);
                border-radius: 15px;
                border: 2px solid #9575cd;
                color: #311b4f;
                padding: 10px;
                font: bold 20px 'Arial';
            }
            QPushButton:hover {
                background-color: #d1c4e9;
                color: #4a148c;
            }
            QPushButton:pressed {
                background-color: #b39ddb;
            }
        """
        for button in self.buttons.values():
            button.setStyleSheet(button_style)
            button.setMinimumHeight(60)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()