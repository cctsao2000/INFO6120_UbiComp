from adafruit_circuitplayground import cp
import analogio
import time
import board

pin = analogio.AnalogIn(board.A5)
while True:
    val = pin.value
    print(f"{val}")
    for i  in range(10):
        if pin.value > i * 3200:
            cp.pixels[i] = (5, 5, 5)
        else:
            cp.pixels[i] = (0, 0, 0)
    time.sleep(0.01)
