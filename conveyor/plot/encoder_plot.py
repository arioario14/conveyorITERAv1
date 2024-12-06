import sys
import os
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from conveyor.sensor_actuator.ac_encoder import Encoder

class RPMPlot(FigureCanvas):
    def __init__(self, parent=None):
        dpi = 80
        self.fig = Figure(figsize=(451 / dpi, 250 / dpi), dpi=dpi)
        self.ax = self.fig.add_subplot(111)

        ENCODER_A = 20  # Pin A
        ENCODER_B = 21  # Pin B
        RESOLUTION = 2000

        # Initialize encoder (assumes encoder has calculate_rpm method)
        self.encoder = Encoder(pin_a=ENCODER_A, pin_b=ENCODER_B, resolution=RESOLUTION)

        # Set plot area position
        self.ax.set_position([0.1, 0.3, 0.8, 0.65])

        # Plot settings for speed
        self.min_speed, self.max_speed = 0, 100  # Define speed range for plot

        super(RPMPlot, self).__init__(self.fig)
        self.setParent(parent)

        self.speeds = []  # List to store speed data
        self.max_len = 50  # Maximum points to display on the plot

        # Timer for updating the plot
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(10)  # Update every 500 ms

    def resizeEvent(self, event):
        """Resize the plot when the widget is resized."""
        self.fig.set_size_inches(self.width() / self.fig.get_dpi(), self.height() / self.fig.get_dpi())
        super(RPMPlot, self).resizeEvent(event)

    def update_plot(self):
        # Get RPM value from encoder
        try:
            speed = self.encoder.calculate_rpm()  # Get RPM value
            self.current_rpm = speed
        except Exception as e:
            print(f"Error reading RPM: {e}")
            speed = 0  # Default to 0 if encoder fails

        # Update speed data
        self.speeds.append(speed)
        if len(self.speeds) > self.max_len:
            self.speeds.pop(0)

        # Clear and update the plot with encoder data
        self.ax.clear()
        self.ax.plot(range(len(self.speeds)), self.speeds, color="red", lw=2)  # Line plot for encoder data

        # Set axis limits
        self.ax.set_xlim(0, self.max_len - 1)
        self.ax.set_ylim(self.min_speed - 10, self.max_speed + 10)

        # Update the plot title
#         self.ax.set_title(f'RPM: {int(speed)}', fontsize=10)

        # Redraw the figure
        self.fig.tight_layout()
        self.draw()
        
    def get_current_rpm(self):
        """
        Returns the most recent RPM value.
        """
        return self.current_rpm
