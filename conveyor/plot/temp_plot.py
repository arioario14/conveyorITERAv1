import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import time
from conveyor.sensor_actuator.sensor_temp import TemperatureSensor
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer


class TemperaturePlot(FigureCanvas):
    def __init__(self, parent=None):
        dpi = 80
        self.fig = Figure(figsize=(451 / dpi, 200 / dpi), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        
        self.ax.set_position([0.1, 3, 0.8, 0.65])  # [left, bottom, width, height]
        
        self.sensor = TemperatureSensor()

        self.min_temp, self.max_temp = 0, 100
        self.norm = mcolors.Normalize(vmin=self.min_temp, vmax=self.max_temp)
        self.cmap = cm.get_cmap('plasma')

        self.sm = cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        self.sm.set_array([])
        self.cbar = self.fig.colorbar(self.sm, ax=self.ax, orientation='vertical')

        super(TemperaturePlot, self).__init__(self.fig)
        self.setParent(parent)

        self.temps = []
        self.max_len = 50
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(10)

    def resizeEvent(self, event):
        self.fig.set_size_inches(self.width() / self.fig.get_dpi(), self.height() / self.fig.get_dpi())
        super(TemperaturePlot, self).resizeEvent(event)

    def update_plot(self):
        temp = self.sensor.read_temp()
        self.current_temp = temp
        
        if temp is not None:
            self.temps.append(temp)
            if len(self.temps) > self.max_len:
                self.temps.pop(0)

            self.ax.clear()
            scatter = self.ax.scatter(range(len(self.temps)), self.temps, c=self.temps, cmap=self.cmap, norm=self.norm)
            
            if len(self.temps) > 1:
                self.ax.set_xlim(max(0, len(self.temps) - self.max_len), len(self.temps) - 1)
            else:
                self.ax.set_xlim(-1, 1)  

            self.ax.set_ylim(self.min_temp - 5, self.max_temp + 5)
#             self.ax.set_title(f'Temperature ({int(temp)}°C)', fontsize=7)
            
            self.fig.tight_layout()  # Automatically adjust layout

            self.draw()
            
    def get_current_temp(self):
        """
        Returns the most recent RPM value.
        """
        return self.current_temp
            
        
# 