# Version 1
from adafruit_circuitplayground import cp
import digitalio
import board
import time

# Setup the motor on pin A4
motor = digitalio.DigitalInOut(board.A4)
motor.switch_to_output()

def vibrate_motor(times, on_time=0.2, off_time=0.2):
    """
    Vibrates the motor a specified number of times.
    :param times: Number of times to vibrate.    :param on_time: Duration of each vibration in seconds.
    :param off_time: Pause between vibrations in seconds.
    """
    for _ in range(times):
        motor.value = True
        time.sleep(on_time)
        motor.value = False
        time.sleep(off_time)

while True:
    light_value = cp.light  # Read the ambient light sensor value (0-255)
    
    if light_value < 50:  # Check if the ambient light is low
        cp.pixels.fill((255, 0, 0))  # Set NeoPixels to red
        vibrate_motor(3)  # Vibrate the motor 3 times
        cp.pixels.fill((0, 0, 0))  # Turn off NeoPixels after vibrating
    else:
        cp.pixels.fill((0, 0, 0))  # Ensure NeoPixels are off if light is not low
    
    time.sleep(1)  # Wait for 1 second before checking the light value again
