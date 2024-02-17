from adafruit_circuitplayground import cp
import digitalio
import board
import time

def cal_distance(origin_point, current_point):
    return ((current_point[0] - origin_point[0]) + (current_point[1] - origin_point[1]) + (current_point[2] - origin_point[2])) ** 0.5

def light_change(change_mode):
    if change_mode == 1:
        for i in range(10):
            cp.pixels[i] = (0, 10, 0)
    else:
        for i in range(10):
            cp.pixels[i] = (0, 0, 0)

count = 0

while True:
    x, y, z = cp.acceleration
    # if cp.button_a:
    time.sleep(0.1)
    x2, y2, z2 = cp.acceleration
    try:
        if cal_distance((x, y, z), (x2, y2, z2)) > 5:
            light_change(1)
            count += 1
        else:
            light_change(0)
    except:
        continue

    if cp.button_a: # click to see jump count
        print(count)

