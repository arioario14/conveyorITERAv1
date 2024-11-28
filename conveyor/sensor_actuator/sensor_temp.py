import os
import time

class TemperatureSensor:
    """
    A class to manage temperature sensor readings using the 1-Wire interface.
    """

    def __init__(self, base_dir='/sys/bus/w1/devices/'):
        self.base_dir = base_dir
        self.device_folder = self._find_device()
        self.device_file = f'{self.base_dir}/{self.device_folder}/w1_slave'

    def _find_device(self):
        """Finds the temperature sensor device folder."""
        try:
            device_folder = [d for d in os.listdir(self.base_dir) if d.startswith('28-')][0]
            return device_folder
        except IndexError:
            raise FileNotFoundError("Temperature sensor not detected.")

    def _read_temp_raw(self):
        """Reads raw data from the sensor."""
        with open(self.device_file, 'r') as file:
            lines = file.readlines()
        return lines

    def read_temp(self):
        """Reads and converts raw sensor data to temperature in Celsius."""
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
        return None
