import time
import board
import digitalio
from adafruit_circuitplayground import cp
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# BLE Setup
ble = BLERadio()
ble.name = "Peggy's Circuit Playground"
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

# Setup for motor vibration
motor = digitalio.DigitalInOut(board.A4)  # Adjust to your motor's pin
motor.switch_to_output()

def vibrate_motor(times, on_time=0.2, off_time=0.2):
    for _ in range(times):
        motor.value = True
        time.sleep(on_time)
        motor.value = False
        time.sleep(off_time)

mode = "start"
cp.pixels.brightness = 0.1

# Function to establish BLE connection
def ensure_ble_connection():
    if not ble.connected:
        print("Trying to connect...")
        ble.start_advertising(advertisement)
        while not ble.connected:
            pass  # Wait for a connection
        ble.stop_advertising()
        print("Connected!")

while True:
    ensure_ble_connection()  # Ensure BLE connection first

    if mode == "start":
        # Blinking white LED
        cp.pixels.fill((255, 255, 255))
        time.sleep(0.5)
        cp.pixels.fill((0, 0, 0))
        time.sleep(0.5)

        if cp.button_a:
            mode = "ambient_light"
            while cp.button_a: pass  # Debounce
        elif cp.button_b:
            mode = "sleep_mode"
            while cp.button_b: pass  # Debounce

    elif mode == "ambient_light":
        light_value = cp.light
        if light_value < 50:
            cp.pixels.fill((255, 0, 0))
            vibrate_motor(3)

        else:
            cp.pixels.fill((0, 0, 0))
        time.sleep(1)

        if cp.button_a and cp.button_b:
            mode = "start"
            while cp.button_a and cp.button_b: pass  # Debounce

    elif mode == "sleep_mode":
        # Initialize variables at the start of sleep mode
        last_x, last_y, last_z = cp.acceleration
        turn_count = 0

        while mode == "sleep_mode":
            x, y, z = cp.acceleration
            temp = cp.temperature
            light_value = cp.light

            # Detect turning
            if abs(x - last_x) > 1 or abs(y - last_y) > 1 or abs(z - last_z) > 1:
                turn_count += 1

            # Check temperature range
            if not 19 <= temp <= 30:
                vibrate_motor(1)
                cp.pixels[0] = (0, 0, 255)  # Set a single pixel to blue
                time.sleep(1)

            # Check light condition
            if light_value > 10:
                cp.pixels.fill((255, 0, 0))  # Red light

            # For the Mu plotter, print the values in a comma-separated format
            print(time.monotonic(), x, y, z, temp, light_value, turn_count)

            # Update last accelerometer values for the next iteration
            last_x, last_y, last_z = x, y, z
            cp.pixels.fill((0, 0, 0))  # Turn off LEDs for next loop iteration

            # Optional: Transmit data over BLE
            if ble.connected:
                try:
                    uart_server.write(f"{x},{y},{z},{temp},{light_value},{turn_count}\n".encode())
                except ConnectionError:
                    print("Disconnected!")
                    break

            if cp.button_a and cp.button_b:
                mode = "start"
                while cp.button_a and cp.button_b: pass  # Debounce
            time.sleep(0.1)  # Adjust sleep time as needed for responsiveness vs. power consumption
