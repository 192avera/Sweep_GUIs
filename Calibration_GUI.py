import numpy as np
import pyvisa
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QWidget, QProgressBar
from time import sleep
import os


def supply_current2020(current, delay):
    """
    Sets the output current of the power supply and returns the actual current the supply is outputting.
    :param current: set the output current to the value input in Ampere units.
    :param delay: delay between write and query commands in time unit of seconds.
    :return: a float with the value of the actual current (Ampere) the instrument is outputting.
    """
    supply.clear()
    supply_string = f'func:mode curr;:curr {current};:volt 20;:OUTP ON'
    supply.write(supply_string)
    sleep(delay)
    supply.clear()
    sleep(delay)
    outp_str = supply.query("curr?").splitlines()
    supply.clear()
    return float(outp_str[0])


# Define function to query the teslameter
def gaussm_query():
    """
    Queries the instrument and returns the value of the reading.
    :return: float with magnetic field units of Gauss (G)
    """
    gm_string = gaussm.query("f")
    gm_float = float(gm_string.split('G')[0])
    return gm_float


# PyVisa Resource Manager
rm = pyvisa.ResourceManager()

# List all available resources with their respective aliases
print("Listing connected GPIB-VISA resources:")
resources_tuple = rm.list_resources()

names = []
aliases = []
for name in resources_tuple:
    names.append(name)
    aliases.append(rm.resource_info(name)[4])

# Create a pandas Dataframe with resources names and aliases
resources_dict = {'Name': names, 'alias': aliases}
resources_df = pd.DataFrame(resources_dict)
print(f'VISA Resources:\n {resources_df.to_string(index=False)}')

# Open Resources
supply = rm.open_resource('GPIB0::1::INSTR')  # KEPCO BOP20-20DL Power Supply
supply.clear()
gaussm = rm.open_resource('GPIB0::3::INSTR')  # Group3 DTM-133 Digital Teslameter


# Initiate the GUI
class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialization of the Main Window of the GUI.
        """
        super().__init__()

        # Set the window title
        self.setWindowTitle('Calibration: Current - Magnetic Field')

        # Create labels and line edits for the input fields
        max_label = QLabel('Max Current (mA):')
        self.max_edit = QLineEdit()
        self.max_edit.setFixedWidth(200)
        min_label = QLabel('Min Current (mA):')
        self.min_edit = QLineEdit()
        self.min_edit.setFixedWidth(200)
        steps_label = QLabel('Current Steps (mA):')
        self.steps_edit = QLineEdit()
        self.steps_edit.setFixedWidth(200)
        wait_label = QLabel('Wait between measurements (ms): ')
        self.wait_edit = QLineEdit()
        self.wait_edit.setFixedWidth(200)

        # Create a line edit for calibration constant 1
        self.calib_label = QLabel('Calibration Constant 1:')
        self.calib_edit = QLineEdit()
        self.calib_edit.setReadOnly(True)
        self.calib_edit.setFixedWidth(200)
        #self.calib_edit.setFixedHeight(30)

        # Create a line edit for calibration constant 2
        self.calib2_label = QLabel('Calibration Constant 2:')
        self.calib2_edit = QLineEdit()
        self.calib2_edit.setReadOnly(True)
        self.calib2_edit.setFixedWidth(200)
        #self.calib2_edit.setFixedHeight(30)
        self.calib_formula_label = QLabel('y = a1 * x + a0')

        # Create a canvas for the plot
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)  # This is the widget
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Current (mA)')
        self.ax.set_ylabel('Magnetic Field (Oe)')
        self.ax.set_title('Calibration Plot')

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
        left_layout.addWidget(self.calib_formula_label)

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
        """
        Changes the boolean value of button_bool so that the if clause in the
        run_script function aborts the loop.
        """
        self.button_bool = not self.button_bool

    # Define a function that reads the inputs
    def read_inputs(self):
        """
        Reads the input values of the input line edits widgets.
        """

        # Read input values
        max_val = float(self.max_edit.text())
        min_val = float(self.min_edit.text())
        steps_val = float(self.steps_edit.text())
        wait = float(self.wait_edit.text())
        return max_val, min_val, steps_val, wait

    def run_script(self):
        """
        This function runs when the run button widget is clicked.
        """
        # Open Resources
        supply = rm.open_resource('GPIB0::1::INSTR')  # KEPCO BOP20-20DL Power Supply
        supply.clear()
        gaussm = rm.open_resource('GPIB0::3::INSTR')  # Group3 DTM-133 Digital Teslameter

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

        # Clear the previous plot
        self.canvas.figure.clear()

        # Create a new set of subplots
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xlabel('Current (mA)')
        self.ax.set_ylabel('Magnetic Field (Oe)')
        self.ax.set_title('Calibration Plot')

        # Create an array of sweep values
        curr_vals = np.arange(min_val, max_val + steps_val, steps_val)

        # Create an array to store current values
        current_data = []

        # Create a list to store the magnetic field values
        mfield_vals = []

        # Loop through the sweep values and calculate proportional values
        for val in curr_vals:

            # If clause to check for abort button press
            if self.button_bool == False:

                # Set the current in ampere units
                curr = round(supply_current2020(val/1000, 0.2)*1000)

                # Store current data in current array
                current_data.append(curr)

                # Query the teslameter and store it in m_field variable
                mfield = gaussm_query()
                print(f"current: {curr}", f"mfield: {mfield}")

                # Calculate the total number of data points to be plotted
                data_points = ((max_val - min_val) / steps_val) + 1

                # Add the data points to the x and y data lists
                self.x_data.append(val)
                self.y_data.append(mfield)

                # Add the proportional value to the list
                mfield_vals.append(mfield)

                # Update the progress bar
                current_index = len(mfield_vals)
                progress = round(current_index / data_points * 100)
                self.progress_bar.setValue(progress)

                # Plot the current data point
                self.ax.plot(self.x_data, self.y_data, linestyle='-', marker='o', color='r')

                # Draw the plot on the canvas
                self.canvas.draw()

                # Wait between measurements
                QApplication.processEvents()
                sleep(wait/1000)

            # Else clause to end the program
            else:
                supply_current2020(0.0, 0.5)
                supply.close()
                gaussm.close()
                self.calib_edit.setText("aborted")
                self.calib2_edit.setText("aborted")
                break

        # Supply current set to 0
        print(f"Current set to {supply_current2020(0.0, 0.1)} A")

        # Close visa resources
        supply.close()
        gaussm.close()

        # Prepare the data to fit
        np_current_data = np.array(current_data)
        np_mfield_vals = np.array(mfield_vals)
        data = np.column_stack((np_current_data, np_mfield_vals))

        # Calculating calibration coefficients
        data_to_fit = data
        model = LinearRegression().fit(data_to_fit[:, 0].reshape((-1, 1)), data_to_fit[:, 1])  # linear regression
        intercept = model.intercept_  # intercept
        slope = model.coef_[0]  # slope

        # Add the constants to the line edit if abort button was not clicked
        if self.button_bool == False:
            self.calib_edit.setText(f"a0: {intercept}")
            self.calib2_edit.setText(f"a1: {slope}")
            print("Calibration constants:")
            print(f"a1: {slope}")
            print(f"a0: {intercept}")
        else:
            print("Measurement aborted")

        # Export the calibration file to the directory of this python file
        path1 = os.getcwd().replace("\\", "/") + "/calibration.txt"
        file1 = open(path1, "w+")
        file1.writelines(f"{slope}" + "," + f"{intercept}")
        file1.close()

        # Update boolean value to run again if abort button is pressed
        self.button_bool = False

        # Print an empty line
        print("")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
