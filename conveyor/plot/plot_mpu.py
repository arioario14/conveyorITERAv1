import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from conveyor.sensor_actuator.sensor_mpu import MPU6050
from mpu6050 import mpu6050

class MPU6050Plotter(FigureCanvas):
    def __init__(self, parent, max_points=100):
        self.fig = Figure()
        self.max_points = max_points
        self.x_data = [0] * self.max_points
        self.y_data = [0] * self.max_points
        self.z_data = [0] * self.max_points
        
        self.sensor = mpu6050(0x68)
        dpi = 80
        self.fig = Figure(figsize=(451 / dpi, 200 / dpi), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim([-5, 5])

        self.fig.tight_layout()
        self.fig.subplots_adjust(bottom=0.2, top=0.9)
        
#         self.fig.subplots_adjust(bottom=0.2)
#         self.fig.subplots_adjust(top=0.1)

        self.line_x, = self.ax.plot(self.x_data, label='X Axis')
        self.line_y, = self.ax.plot(self.y_data, label='Y Axis')
        self.line_z, = self.ax.plot(self.z_data, label='Z Axis')

        self.ax.legend(prop={'size': 8})

        # Create a canvas to embed the matplotlib figure in Qt
        self.canvas = FigureCanvas(self.fig)
        super(MPU6050Plotter, self).__init__(self.fig)
        self.canvas.setParent(parent)

        # Layout for the canvas
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        parent.setLayout(layout)

        self.update_plot()

    def read_accel_data(self):
        accel_data = self.sensor.get_accel_data()
        return accel_data['x'], accel_data['y'], accel_data['z']

    def update_plot(self):
        x_acc, y_acc, z_acc = self.read_accel_data()

        self.x_data.append(x_acc)
        self.y_data.append(y_acc)
        self.z_data.append(z_acc)

        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.y_data.pop(0)
            self.z_data.pop(0)

        self.line_x.set_ydata(self.x_data)
        self.line_y.set_ydata(self.y_data)
        self.line_z.set_ydata(self.z_data)

        self.canvas.draw()

        QtCore.QTimer.singleShot(10, self.update_plot)