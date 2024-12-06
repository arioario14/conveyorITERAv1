import smbus
import time

# Constants
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Class for MPU6050 sensor
class MPU6050:
    def __init__(self, bus_num=1, address=MPU6050_ADDR):
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 0)  # Wake up the MPU6050
        self.accel_offsets = [0, 0, 0]
        self.gyro_offsets = [0, 0, 0]

    def read_word(self, reg):
        high = self.bus.read_byte_data(self.address, reg)
        low = self.bus.read_byte_data(self.address, reg + 1)
        value = (high << 8) + low
        if value >= 0x8000:
            value -= 0x10000
        return value

    def read_accel(self):
        ax = self.read_word(ACCEL_XOUT_H) - self.accel_offsets[0]
        ay = self.read_word(ACCEL_XOUT_H + 2) - self.accel_offsets[1]
        az = self.read_word(ACCEL_XOUT_H + 4) - self.accel_offsets[2]
        return ax, ay, az

    def read_gyro(self):
        gx = self.read_word(GYRO_XOUT_H) - self.gyro_offsets[0]
        gy = self.read_word(GYRO_XOUT_H + 2) - self.gyro_offsets[1]
        gz = self.read_word(GYRO_XOUT_H + 4) - self.gyro_offsets[2]
        return gx, gy, gz

    def calibrate(self, samples=100):
        accel_sum = [0, 0, 0]
        gyro_sum = [0, 0, 0]

        for _ in range(samples):
            ax, ay, az = self.read_accel()
            gx, gy, gz = self.read_gyro()

            accel_sum[0] += ax
            accel_sum[1] += ay
            accel_sum[2] += az
            gyro_sum[0] += gx
            gyro_sum[1] += gy
            gyro_sum[2] += gz
            time.sleep(0.01)

        self.accel_offsets = [x // samples for x in accel_sum]
        self.gyro_offsets = [x // samples for x in gyro_sum]
        print(f"Calibration complete. Offsets: Accel={self.accel_offsets}, Gyro={self.gyro_offsets}")
