import RPi.GPIO as GPIO
import time

class Encoder:
    def __init__(self, pin_a, pin_b, pulses_per_revolution=2000):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pulses_per_revolution = pulses_per_revolution
        self.encoder_value = 0
        
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self.encoder_callback)
        GPIO.add_event_detect(self.pin_b, GPIO.BOTH, callback=self.encoder_callback)
        
    def encoder_callback(self, channel):
        A = GPIO.input(self.pin_a)
        B = GPIO.input(self.pin_b)
        
        if (A == GPIO.HIGH) != (B == GPIO.LOW):
            self.encoder_value -= 1
        else:
            self.encoder_value += 1
    
    def calculate_rpm(self):
        rpm = (self.encoder_value * 60) / self.pulses_per_revolution
        self.encoder_value = 0
        return abs(rpm)
    
    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    PIN_A = 20  # Example GPIO pin for A
    PIN_B = 21  # Example GPIO pin for B
    PULSES_PER_REVOLUTION = 2000  # Example value, adjust based on your encoder

    # Initialize the encoder
    encoder = Encoder(PIN_A, PIN_B, PULSES_PER_REVOLUTION)

    try:
        while True:
            # Calculate and print RPM every 1 second
            rpm = encoder.calculate_rpm()
            print(f"RPM: {rpm}")
            time.sleep(1)

    except KeyboardInterrupt:
        # Graceful cleanup when the program is interrupted
        print("Program interrupted. Cleaning up...")
        encoder.cleanup()
