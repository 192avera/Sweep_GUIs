import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QWidget, QProgressBar
from PyQt5.QtCore import Qt
from time import sleep
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Sweep Plot')

        # Create labels and line edits for the input fields
        max_label = QLabel('Max:')
        self.max_edit = QLineEdit()
        self.max_edit.setPlaceholderText("Max: ")
        self.max_edit.setFixedWidth(200)
        min_label = QLabel('Min:')
        self.min_edit = QLineEdit()
        self.min_edit.setPlaceholderText("Min: ")
        self.min_edit.setFixedWidth(200)
        steps_label = QLabel('Steps:')
        self.steps_edit = QLineEdit()
        self.steps_edit.setPlaceholderText("Steps: ")
        self.steps_edit.setFixedWidth(200)
        wait_label = QLabel('Wait between plots (ms): ')
        self.wait_edit = QLineEdit()
        self.wait_edit.setPlaceholderText("Wait between plots: ")
        self.wait_edit.setFixedWidth(200)

        # Create a line edit for calibration constant 1
        self.calib_label = QLabel('Calibration Constant 1:')
        self.calib_edit = QLineEdit()
        self.calib_edit.setReadOnly(True)
        self.calib_edit.setFixedWidth(200)
        #self.calib_edit.setFixedHeight(30)
        self.calib_edit.setPlaceholderText("Calibration constant 1: ")

        # Create a line edit for calibration constant 2
        self.calib2_label = QLabel('Calibration Constant 2:')
        self.calib2_edit = QLineEdit()
        self.calib2_edit.setReadOnly(True)
        self.calib2_edit.setFixedWidth(200)
        #self.calib2_edit.setFixedHeight(30)
        self.calib2_edit.setPlaceholderText("Calibration constant 2: ")

        # Create a canvas for the plot
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)  # This is the widget
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Sweep Values')
        self.ax.set_ylabel('Proportional Values')
        self.ax.set_title('Sweep Plot')

        # Create buttons to run the script and abort
        self.button_run = QPushButton('Run Script')
        self.button_run.clicked.connect(self.run_script)
        self.button_abort = QPushButton('Abort')
        self.button_abort.setCheckable(True)
        self.button_abort.clicked.connect(self.toggle_bool)

        # Create progress bar
        self.progress_bar = QProgressBar()

        # Create a layout for the input fields and calibration constants (Left layout)
        left_layout = QVBoxLayout()
        left_layout.addWidget(max_label)
        left_layout.addWidget(self.max_edit)
        left_layout.addWidget(min_label)
        left_layout.addWidget(self.min_edit)
        left_layout.addWidget(steps_label)
        left_layout.addWidget(self.steps_edit)
        left_layout.addWidget(wait_label)
        left_layout.addWidget(self.wait_edit)
        left_layout.addStretch()
        left_layout.addWidget(self.calib_label)
        left_layout.addWidget(self.calib_edit)
        left_layout.addWidget(self.calib2_label)
        left_layout.addWidget(self.calib2_edit)

        # Create a layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_run)
        button_layout.addWidget(self.button_abort)

        # Create a layout for the canvas, buttons and progress bar (Right layout)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.canvas)
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.progress_bar)

        # Create a layout for the input fields and the button/canvas layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Set the central widget of the main window
        self.setCentralWidget(central_widget)

        # Create a counter to keep track of the current point index
        self.index = 0

        # Set button boolean value to False
        self.button_bool = False

        # Set the default values of the input line edits
        self.max_edit.setText("1000")
        self.min_edit.setText("0")
        self.steps_edit.setText("100")
        self.wait_edit.setText("100")

    # Define a function to change the boolean value to abort script
    def toggle_bool(self):
        self.button_bool = not self.button_bool

    # Define a function that reads the inputs
    def read_inputs(self):

        # Read input values
        max_val = float(self.max_edit.text())
        min_val = float(self.min_edit.text())
        steps_val = float(self.steps_edit.text())
        wait = float(self.wait_edit.text())
        return max_val, min_val, steps_val, wait

    def run_script(self):
        # Create a list to store the x and y data points
        self.x_data = []
        self.y_data = []

        # Get the input values from the line edits
        max_val, min_val, steps_val, wait = self.read_inputs()

        # Reset progress bar
        self.progress_bar.setValue(0)

        # Reset calibration constants line edits
        self.calib_edit.setText("")
        self.calib2_edit.setText("")

        # Create an array of sweep values
        sweep_vals = np.arange(min_val, max_val + steps_val, steps_val)

        # Create a list to store the proportional values
        prop_vals = []

        # Clear the previous plot
        self.canvas.figure.clear()

        # Create a new set of subplots
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xlabel('Sweep Values')
        self.ax.set_ylabel('Proportional Values')
        self.ax.set_title('Sweep Plot')

        # Loop through the sweep values and calculate proportional values
        for val in sweep_vals:

            # If clause to check for abort button press
            if self.button_bool == False:

                # Calculate the proportional value
                prop_val = val * 1.45

                # Calculate the total number of data points to be plotted
                data_points = ((max_val - min_val) / steps_val) + 1

                # Add the data points to the x and y data lists
                self.x_data.append(val)
                self.y_data.append(prop_val)
                print(f"x: {val}", f"y: {prop_val}")

                # Add the proportional value to the list
                prop_vals.append(prop_val)

                # Update the progress bar
                current_index = len(prop_vals)
                progress = round(current_index / data_points * 100)
                self.progress_bar.setValue(progress)

                # Plot the current data point
                self.ax.plot(self.x_data, self.y_data, linestyle='-', marker='o', color='r')

                # Draw the plot on the canvas
                self.canvas.draw()

                # Wait between plots
                QApplication.processEvents()
                sleep(wait/1000)

            # Else clause to end the program
            else:
                self.calib_edit.setText("aborted")
                self.calib2_edit.setText("aborted")
                break

        # Add the constants to the line edit if abort button was not clicked
        if self.button_bool == False:
            constant1 = 0.5
            constant2 = 1.5
            self.calib_edit.setText(f"constant1: {constant1}")
            self.calib2_edit.setText(f"constant2: {constant2}")
            print("Calibration constants:")
            print(f"constant1: {constant1}")
            print(f"constant2: {constant2}")
        else:
            print("Measurement aborted")

        # Update boolean value to run again
        self.button_bool = False

        # Print an empty line
        print("")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()