from adafruit_circuitplayground import cp
cp.pixels.brightness = 0.05
while True:
    if cp.touch_A1:
        cp.pixels[6] = (0,50,0)
    if cp.touch_A2:
        cp.pixels[8] = (50,0,0)
    if cp.touch_A3:
        cp.pixels[9] = (0,0,50)
    if cp.touch_A4:
        cp.pixels[1] = (50,50,0)
    if cp.touch_A5:
        cp.pixels[2] = (0,50,50)
    if cp.touch_A6:
        cp.pixels[3] = (50,0,50)
