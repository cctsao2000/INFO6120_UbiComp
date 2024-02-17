from adafruit_circuitplayground import cp
import time

cp.pixels.brightness = 0.1
def modifylight():
    pixel_no = 0
    while True:
        if pixel_no > 9:
            pixel_no = 0
        if pixel_no < 0:
            pixel_no = -1
        if cp.button_a:
            pixel_no += 1
            time.sleep(0.5)
        if cp.button_b:
            pixel_no -= 1
            time.sleep(0.5)
        for i in range(10):
            if i <= pixel_no:
                cp.pixels[i] = (0, 50, 0)
            else:
                cp.pixels[i] = (0, 0, 0)
