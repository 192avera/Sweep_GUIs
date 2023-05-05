# Sweep_GUIs
A repository of PyQt GUIs I made time ago when I was working on a Material Physics Laboratory, more specifically in the area of Spintronics.

## Overview

### plot_gui.py
This script is just the template of a GUI using PyQt. It performs a sweep of values with user inputs as settings and plots them against proportional values. All you have to do is input the minimum and maximum values of the sweep and the magnitude of the steps between each point. Then, it plots the values against the same values multiplied by a constant and displays two calibration constants as outputs. It also comes with a progress bar, a button to run the sweep and an abort button. The code is developed in a way that each time the run button is pressed it clears the previous plot and constants, reads the inputs again and performs the sweep again with updated inputs without terminating the application. 

I developed this GUI because I needed to create a calibration program that determines the mathematical relationship between the applied magnetic field on a sample and the electric current beign supllied to the electromagnet generating the magnetic field.

### Calibration_GUI.py
As mentioned before, this is the python code for the GUI designed to find the relationship between the electrical current supplied to an electromagnet and the magnetic field generated between the magnetic poles. This is done because, in some cases, you wouldn't want to have a Teslameter measuring magetic field and using up space in the setup when you could know what value of electrical current generates what magnitude of magnetic field strength. It basically frees you of the need of using one more machine in the experiment.

This is also an example of how the previous template can be modified for a specific sweep application.

When the sweep is done a linear regression model finds the best coefficients to describe the linear relationship between these values. This calibration constants are to be used in other experiments.

The code is designed to work with a KEPCO BOP20-20DL Power Supply and a Group3 DTM-133 Digital Teslameter.

### gui_plot_paths.py
This is the template of a GUI that performs a sweep that is a little more complex than the plot_gui.py script. This time you can choose path settings of the sweep, this means that, in contrast with the other sweep template, you can chose more than two points to perform the sweep and between each of these points you can set different steps sizes between each point. It plots the sweep values against some other variable values (in the template they are produced randomly). It also comes with a console widget that displays what is printed in the console.
