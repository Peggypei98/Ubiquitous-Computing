import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
ble.name = "Peggy's Circuit Playground"  # Set the name of the BLE device
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)

while True:
    ble.start_advertising(advertisement)
    print("Advertising...")
    while not ble.connected:
        pass
    ble.stop_advertising()
    print("Connected!")
    while ble.connected:
        # Perform BLE communication tasks
        time.sleep(1)
    print("Disconnected!")
