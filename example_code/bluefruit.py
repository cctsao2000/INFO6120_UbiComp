import time
from adafruit_circuitplayground import cp
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
ble = BLERadio()
ble.name = "Amber"
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
while True:
# Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()
    print("Connected!")
    while ble.connected:
        x, y, z = cp.acceleration
        try:
            uart_server.write(f"{x},{y},{z}\n")
        except ConnectionError:
            print("Disconnected!")
            break
        time.sleep(0.1)
