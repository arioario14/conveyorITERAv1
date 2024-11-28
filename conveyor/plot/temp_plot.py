from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time
from PyQt5.QtCore import QThread


class TemperaturePlot(FigureCanvas):
    """
    A Matplotlib Canvas to display real-time temperature plots.
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)
        self.setParent(parent)
        self.axes = self.figure.add_subplot(111)
        self.time_data = []
        self.temp_data = []

    def update_plot(self, temp, timestamp):
        """Updates the plot with new temperature and timestamp data."""
        self.time_data.append(timestamp)
        self.temp_data.append(temp)

        if len(self.time_data) > 20:  # Limit the data to the last 20 points
            self.time_data.pop(0)
            self.temp_data.pop(0)

        self.axes.clear()
        self.axes.plot(self.time_data, self.temp_data, label="Temperature (°C)", color='b')
        self.axes.set_title("Real-Time Temperature")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Temperature (°C)")
        self.axes.legend()
        self.draw()


class TemperatureMonitorThread(QThread):
    """
    A QThread to read temperature data and update the plot in real time.
    """

    def __init__(self, sensor, plot_canvas):
        super().__init__()
        self.sensor = sensor
        self.plot_canvas = plot_canvas
        self.running = True

    def run(self):
        start_time = time.time()
        while self.running:
            try:
                temp = self.sensor.read_temp()
                if temp is not None:
                    current_time = time.time() - start_time
                    self.plot_canvas.update_plot(temp, current_time)
                time.sleep(1)  # Update every second
            except Exception as e:
                print(f"Error reading temperature: {e}")
                self.running = False

    def stop(self):
        self.running = False
