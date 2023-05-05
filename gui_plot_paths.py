import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel,\
    QPlainTextEdit, QSplitter, QSpinBox, QRadioButton, QTableWidget, QPushButton, QProgressBar, QFrame, QTableWidgetItem
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from time import sleep

# -------------- EXTERNAL FUNCTIONS -------------- #

# Function to build array of sweep values depending on path selection
def build_array(num_paths, points_arr, steps_arr):
    sweep_values = []

    for i in range(num_paths):
        start_index = i
        end_index = i + 1

        start_point = points_arr[start_index]
        end_point = points_arr[end_index]
        step_size = steps_arr[start_index]

        # Generate sweep values from start_point to end_point with step_size
        sweep_values.extend(list(range(int(start_point), int(end_point), int(step_size))))

    # Add final point to sweep values
    sweep_values.append(points_arr[num_paths])

    return sweep_values

# -------------- CLASS DEFINITION -------------- #

# Definition of the MainWindow class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Plot with Paths')

        # -------------- WIDGETS -------------- #

        # Create a tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setFixedWidth(420)

        # Create radio buttons
        radio1 = QRadioButton('A-B')
        radio2 = QRadioButton('A-B-C')
        radio3 = QRadioButton('A-B-C-D')
        radio4 = QRadioButton('A-B-C-D-E')
        radio5 = QRadioButton('A-B-C-D-E-F')
        radio6 = QRadioButton('A-B-C-D-E-F-G')

        # Initialize the variable to store the radio button value
        self.radio_value = None

        # Connect the radio buttons to the callback function
        radio1.clicked.connect(lambda: self.update_radio_value(1))
        radio2.clicked.connect(lambda: self.update_radio_value(2))
        radio3.clicked.connect(lambda: self.update_radio_value(3))
        radio4.clicked.connect(lambda: self.update_radio_value(4))
        radio5.clicked.connect(lambda: self.update_radio_value(5))
        radio6.clicked.connect(lambda: self.update_radio_value(6))

        # Create spin boxes and labels for the first tab
        # Point A
        pointA_label = QLabel('Point A')
        self.pointA_edit = QSpinBox()
        self.pointA_edit.setMinimum(-20000)
        self.pointA_edit.setMaximum(20000)
        self.pointA_edit.setFixedWidth(100)

        # Point B
        pointB_label = QLabel('Point B')
        self.pointB_edit = QSpinBox()
        self.pointB_edit.setMinimum(-20000)
        self.pointB_edit.setMaximum(20000)
        self.pointB_edit.setFixedWidth(100)

        # Point C
        pointC_label = QLabel('Point C')
        self.pointC_edit = QSpinBox()
        self.pointC_edit.setMinimum(-20000)
        self.pointC_edit.setMaximum(20000)
        self.pointC_edit.setFixedWidth(100)

        # Point D
        pointD_label = QLabel('Point D')
        self.pointD_edit = QSpinBox()
        self.pointD_edit.setMinimum(-20000)
        self.pointD_edit.setMaximum(20000)
        self.pointD_edit.setFixedWidth(100)

        # Point E
        pointE_label = QLabel('Point E')
        self.pointE_edit = QSpinBox()
        self.pointE_edit.setMinimum(-20000)
        self.pointE_edit.setMaximum(20000)
        self.pointE_edit.setFixedWidth(100)

        # Point F
        pointF_label = QLabel('Point F')
        self.pointF_edit = QSpinBox()
        self.pointF_edit.setMinimum(-20000)
        self.pointF_edit.setMaximum(20000)
        self.pointF_edit.setFixedWidth(100)

        # Point G
        pointG_label = QLabel('Point G')
        self.pointG_edit = QSpinBox()
        self.pointG_edit.setMinimum(-20000)
        self.pointG_edit.setMaximum(20000)
        self.pointG_edit.setFixedWidth(100)

        # Create labels and spin boxes for steps
        # Step A-B
        step1_label = QLabel('Step A-B')
        self.step1_edit = QSpinBox()
        self.step1_edit.setMinimum(-20000)
        self.step1_edit.setMaximum(20000)
        self.step1_edit.setFixedWidth(100)

        # Step B-C
        step2_label = QLabel('Step B-C')
        self.step2_edit = QSpinBox()
        self.step2_edit.setMinimum(-20000)
        self.step2_edit.setMaximum(20000)
        self.step2_edit.setFixedWidth(100)

        # Step C-D
        step3_label = QLabel('Step C-D')
        self.step3_edit = QSpinBox()
        self.step3_edit.setMinimum(-20000)
        self.step3_edit.setMaximum(20000)
        self.step3_edit.setFixedWidth(100)

        # Step D-E
        step4_label = QLabel('Step D-E')
        self.step4_edit = QSpinBox()
        self.step4_edit.setMinimum(-20000)
        self.step4_edit.setMaximum(20000)
        self.step4_edit.setFixedWidth(100)

        # Step E-F
        step5_label = QLabel('Step E-F')
        self.step5_edit = QSpinBox()
        self.step5_edit.setMinimum(-20000)
        self.step5_edit.setMaximum(20000)
        self.step5_edit.setFixedWidth(100)

        # Step F-G
        step6_label = QLabel('Step F-G')
        self.step6_edit = QSpinBox()
        self.step6_edit.setMinimum(-20000)
        self.step6_edit.setMaximum(20000)
        self.step6_edit.setFixedWidth(100)

        # Create setup values labels and spin boxes
        freq_label = QLabel('Frequency')
        self.freq_edit = QSpinBox()
        self.freq_edit.setMinimum(-20000)
        self.freq_edit.setMaximum(20000)
        self.freq_edit.setFixedWidth(100)
        pow_label = QLabel('Power')
        self.pow_edit = QSpinBox()
        self.pow_edit.setMinimum(-20000)
        self.pow_edit.setMaximum(20000)
        self.pow_edit.setFixedWidth(100)
        measurements_label = QLabel('# of measurements')
        self.measurements_edit = QSpinBox()
        self.measurements_edit.setMinimum(-20000)
        self.measurements_edit.setMaximum(20000)
        self.measurements_edit.setFixedWidth(100)
        time_label = QLabel('Time between')
        self.time_edit = QSpinBox()
        self.time_edit.setMinimum(-20000)
        self.time_edit.setMaximum(20000)
        self.time_edit.setFixedWidth(100)

        # Create a table widget for the data
        self.table = QTableWidget(1, 2)
        self.table.setHorizontalHeaderLabels(['Sweep Values', 'Values of interest'])

        # Create canvas for the plot
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)  # This is the widget
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Sweep Values')
        self.ax.set_ylabel('Variable of interest')
        self.ax.set_title('Sweep Plot')

        # Create button to run script and abort
        self.button_run = QPushButton('Run Script')
        self.button_run.clicked.connect(self.run_script)
        self.button_abort = QPushButton('Abort')
        self.button_abort.setCheckable(True)
        self.button_abort.clicked.connect(self.toggle_bool)

        # Create progress bar
        self.progress_bar = QProgressBar()

        # Create a QPlainTextEdit widget to display the console output
        self.console = QPlainTextEdit(self)
        self.console.setReadOnly(True)

        # -------------- LAYOUTS -------------- #

        # Create a layout for the radio buttons
        radio_layout1 = QHBoxLayout()
        radio_layout1.addWidget(radio1)
        radio_layout1.addWidget(radio2)
        radio_layout1.addWidget(radio3)
        radio_layout2 = QHBoxLayout()
        radio_layout2.addWidget(radio4)
        radio_layout2.addWidget(radio5)
        radio_layout2.addWidget(radio6)
        radio_layout = QVBoxLayout()  # Final layout for the radio buttons
        radio_layout.addLayout(radio_layout1)
        radio_layout.addLayout(radio_layout2)

        # Create a layout for the left spin boxes and labels
        left_spin_layout = QVBoxLayout()
        left_spin_layout.addWidget(pointA_label)
        left_spin_layout.addWidget(self.pointA_edit)
        left_spin_layout.addWidget(pointB_label)
        left_spin_layout.addWidget(self.pointB_edit)
        left_spin_layout.addWidget(pointC_label)
        left_spin_layout.addWidget(self.pointC_edit)
        left_spin_layout.addWidget(pointD_label)
        left_spin_layout.addWidget(self.pointD_edit)
        left_spin_layout.addWidget(pointE_label)
        left_spin_layout.addWidget(self.pointE_edit)
        left_spin_layout.addWidget(pointF_label)
        left_spin_layout.addWidget(self.pointF_edit)
        left_spin_layout.addWidget(pointG_label)
        left_spin_layout.addWidget(self.pointG_edit)

        # Create a layout for the right spin boxes and labels
        right_spin_layout = QVBoxLayout()
        right_spin_layout.addStretch()
        right_spin_layout.addWidget(step1_label)
        right_spin_layout.addWidget(self.step1_edit)
        right_spin_layout.addWidget(step2_label)
        right_spin_layout.addWidget(self.step2_edit)
        right_spin_layout.addWidget(step3_label)
        right_spin_layout.addWidget(self.step3_edit)
        right_spin_layout.addWidget(step4_label)
        right_spin_layout.addWidget(self.step4_edit)
        right_spin_layout.addWidget(step5_label)
        right_spin_layout.addWidget(self.step5_edit)
        right_spin_layout.addWidget(step6_label)
        right_spin_layout.addWidget(self.step6_edit)
        right_spin_layout.addStretch()

        # Create a layout with both right and left spin boxes
        spin_layout = QHBoxLayout()
        spin_layout.addLayout(left_spin_layout)
        spin_layout.addLayout(right_spin_layout)

        # Create a layout for the setup variables spin boxes and labels
        setup_layout1 = QVBoxLayout()
        setup_layout1.addWidget(freq_label)
        setup_layout1.addWidget(self.freq_edit)
        setup_layout1.addWidget(pow_label)
        setup_layout1.addWidget(self.pow_edit)
        setup_layout2 = QVBoxLayout()
        setup_layout2.addWidget(measurements_label)
        setup_layout2.addWidget(self.measurements_edit)
        setup_layout2.addWidget(time_label)
        setup_layout2.addWidget(self.time_edit)
        setup_layout = QHBoxLayout()  # Final layout for setup variables
        setup_layout.addLayout(setup_layout1)
        setup_layout.addLayout(setup_layout2)

        # Add a separator line between the layouts
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        # Create first tab and add the layouts
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel('Select Path'))
        tab1_layout.addLayout(radio_layout)
        tab1_layout.addWidget(line1)
        tab1_layout.addWidget(QLabel('Path Settings'))
        tab1_layout.addLayout(spin_layout)
        tab1_layout.addWidget(line2)
        tab1_layout.addWidget(QLabel('Measurement Settings'))
        tab1_layout.addLayout(setup_layout)
        tab1.setLayout(tab1_layout)
        self.tab_widget.addTab(tab1, "Settings")

        # Create the second tab and add the layouts
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(self.table)
        tab2.setLayout(tab2_layout)
        self.tab_widget.addTab(tab2, "Data")

        # Create a layout for the tabs
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.tab_widget)

        # Create a layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_run)
        button_layout.addWidget(self.button_abort)

        # Create a layout for the canvas, buttons and progress bar
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.canvas)
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.progress_bar)

        # Create a layout with the left and right layouts
        top_layout = QHBoxLayout()
        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)

        # Create a bottom layout for the Console Writer
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.console)

        # Create a main layout with the top and bottom
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Set the central widget of the main window
        self.setCentralWidget(central_widget)

        # -------------- SETTINGS -------------- #

        # Set button boolean value to False
        self.button_bool = False

        # Set default values of inputs
        radio1.setChecked(True)
        self.radio_value = 1

        self.pointA_edit.setValue(-1000)
        self.step1_edit.setValue(100)
        self.pointB_edit.setValue(-100)
        self.step2_edit.setValue(10)
        self.pointC_edit.setValue(100)
        self.step3_edit.setValue(100)
        self.pointD_edit.setValue(1000)
        self.step4_edit.setValue(-100)
        self.pointE_edit.setValue(100)
        self.step5_edit.setValue(-10)
        self.pointF_edit.setValue(-100)
        self.step6_edit.setValue(-100)
        self.pointG_edit.setValue(-1000)

        self.freq_edit.setValue(7000)
        self.pow_edit.setValue(12)
        self.measurements_edit.setValue(1)
        self.time_edit.setValue(500)

        # Redirect the stdout and stderr streams to the console widget
        sys.stdout = self.ConsoleWriter(self.console, sys.stdout)
        sys.stderr = self.ConsoleWriter(self.console, sys.stderr)

        # Show the GUI
        self.show()

    # -------------- CONSOLE WRITER CLASS -------------- #

    class ConsoleWriter:
        def __init__(self, console, stream):
            self.console = console
            self.stream = stream

        def write(self, text):
            self.console.insertPlainText(text)

        def flush(self):
            pass

    # -------------- METHODS -------------- #

    # Define function to update radio button value
    def update_radio_value(self, value):
        self.radio_value = value

    # Define a function to change the boolean value to abort script
    def toggle_bool(self):
        self.button_bool = not self.button_bool

    # Define a function that reads the inputs
    def read_inputs(self):
        # Read input values
        pointA = float(self.pointA_edit.text())
        pointB = float(self.pointB_edit.text())
        pointC = float(self.pointC_edit.text())
        pointD = float(self.pointD_edit.text())
        pointE = float(self.pointE_edit.text())
        pointF = float(self.pointF_edit.text())
        pointG = float(self.pointG_edit.text())
        points_arr = [pointA, pointB, pointC, pointD, pointE, pointF, pointG]

        stepAB = float(self.step1_edit.text())
        stepBC = float(self.step2_edit.text())
        stepCD = float(self.step3_edit.text())
        stepDE = float(self.step4_edit.text())
        stepEF = float(self.step5_edit.text())
        stepFG = float(self.step6_edit.text())
        steps_arr = [stepAB, stepBC, stepCD, stepDE, stepEF, stepFG]

        freq = float(self.freq_edit.text())
        pow = float(self.pow_edit.text())
        meas = float(self.measurements_edit.text())
        time_between = float(self.time_edit.text())
        setups_arr = [freq, pow, meas, time_between]

        return points_arr, steps_arr, setups_arr

    def run_script(self):

        print('Running script...')

        # Create a list to store the x and y data points
        self.x_data = []
        self.y_data = []

        # Reset progress bar
        self.progress_bar.setValue(0)

        # Get the input values and store them in variables
        points_array, steps_array, setups_array = self.read_inputs()
        wait = setups_array[3]

        # Build the array of current values
        num_paths = self.radio_value
        sweep_array = build_array(num_paths, points_array, steps_array)
        print(sweep_array)

        # Create a list to store the resulting values
        resulting_vals = []

        # Clear the previous table elements
        self.table.clearContents()
        self.table.setRowCount(1)
        self.table.setColumnCount(2)

        # Clear the previous plot
        self.canvas.figure.clear()

        # Create a new set of subplots
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xlabel('Sweep Values')
        self.ax.set_ylabel('Variable of interest')
        self.ax.set_title('Sweep Plot')

        # Loop through the sweep values and get variable of interest values
        for idx, val in enumerate(sweep_array):

            # If clause to check for abort button press
            if self.button_bool == False:

                # Get variable of interest value
                value_of_interest = np.random.normal(0, 1)

                # Get the total number of datapoints to be plotted
                data_points = len(sweep_array)

                # Add the data points to the x and y data lists
                self.x_data.append(val)
                self.y_data.append(value_of_interest)

                # Add the value of interest to the list
                resulting_vals.append(value_of_interest)

                # Update the progress bar
                current_index = len(resulting_vals)
                progress = round(current_index / data_points * 100)
                self.progress_bar.setValue(progress)

                # Plot the current data point
                self.ax.plot(self.x_data, self.y_data, linestyle='-', marker='o', color='r')

                # Draw the plot on the canvas
                self.canvas.draw()

                # Inject new data to the table widget in the second tab
                new_data = [val, value_of_interest]
                if idx == 0:
                    for i, value in enumerate(new_data):
                        item = QTableWidgetItem(str(value))
                        self.table.setItem(0, i, item)
                else:
                    self.table.insertRow(self.table.rowCount())
                    for i, value in enumerate(new_data):
                        item = QTableWidgetItem(str(value))
                        self.table.setItem(self.table.rowCount()-1, i, item)

                # Wait between plots
                QApplication.processEvents()
                sleep(wait / 1000)

            # Else clause to end the program
            else:
                print('Measurement Aborted')
                break

        # Update boolean value to run again
        self.button_bool = False

        # Print an empty line
        print("")

# -------------- BOILERPLATE CODE / MAIN ENTRY POINT OF GUI -------------- #


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(app.exec_())