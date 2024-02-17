from adafruit_circuitplayground import cp
import digitalio
import board
import time
import adafruit_hcsr04
from adafruit_datetime import datetime, date
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.magnetometer_packet import MagnetometerPacket # ios app UI issue
from adafruit_bluefruit_connect.location_packet import LocationPacket

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A2, echo_pin=board.A1)
ble = BLERadio()
ble.name = "Amber"
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

start_sec = 0
end_sec = 0
started = False
speed_list = []
distance = 0

def cal_acceleration(origin_point, current_point): # ignore y axis, which refers to jumping action
    return (abs(current_point[0] - origin_point[0]) + abs(current_point[2] - origin_point[2])) ** 0.5

def cal_distance(origin_point, current_point):
    return (abs(current_point[0] - origin_point[0]) + abs(current_point[1] - origin_point[1])) ** 0.5

def overspeed_alert(speed, speed_limit=1.5):
    if speed > speed_limit:
        for i in range(10):
            cp.pixels[i] = (10, 0, 0)
        cp.play_file("assets/overspeed.wav")
        for i in range(10):
            cp.pixels[i] = (0, 0, 0)

def obstacle_detecter(distance):
    if distance < 100:
        cp.play_file("assets/obstacle.wav")

def generate_report():
    current_time = time.localtime(761275844+time.time()) # rebooting will cause the time to be inaccurate
    with open(f'{current_time[0]}_{current_time[1]}_{current_time[2]}_{current_time[3]}{current_time[4]}.txt', 'w') as f:
        f.write(f'Date: {current_time[0]}/{current_time[1]}/{current_time[2]}\n')
        f.write(f'Average Speed: {(distance_location) / (end_sec-start_sec) * 3.6:.2f} kph\n')
        f.write(f'Skating Distance: {distance_location:.2f} meters\n')
        f.write(f'Skating Time: {(end_sec-start_sec) // 60:02d}:{(end_sec-start_sec) % 60:02d}\n')
    print(current_time)
    print(f'{(distance_location) / (end_sec-start_sec) * 3.6:.2f}')
    print(f'Skating Distance: {distance_location:.2f} meters')
    print(f'Skating Time: {(end_sec-start_sec) // 60:02d}:{(end_sec-start_sec) % 60:02d}')


def start_record():
    global start_sec
    global started
    global speed_list
    global distance_location
    distance_location = 0
    speed_list = []
    start_sec = time.time()
    started = True
    print('start recording')

def end_record():
    global end_sec
    global started
    end_sec = time.time()
    started = False
    print('end recording')

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()
    while ble.connected:
        try:
            if uart.in_waiting:
                packet = Packet.from_stream(uart)
                if isinstance(packet, ButtonPacket):
                    if packet.pressed:
                        if packet.button == ButtonPacket.BUTTON_1:
                            start_record()
                        elif packet.button == ButtonPacket.BUTTON_2:
                            end_record()
                            generate_report()
                if started == True:
                    if isinstance(packet, LocationPacket):
                        try:
                            initial_location
                        except NameError:
                            initial_location = (float(f'{packet.latitude:6f}'[2:]), float(f'{packet.longitude:6f}'[2:]))
                        current_location = (float(f'{packet.latitude:6f}'[2:]), float(f'{packet.longitude:6f}'[2:]))
                        distance_location += cal_distance(initial_location, current_location)
                        current_location = initial_location
                    speed_list.append(round(speed, 2))
        except ValueError:
            continue

        unit_time = 0.1
        x, y, z = cp.acceleration
        time.sleep(unit_time)
        x2, y2, z2 = cp.acceleration
        speed = (cal_acceleration((x, y, z), (x2, y2, z2)) * (unit_time ** 2)) / 2
        overspeed_alert(speed)
        obstacle_detecter(sonar.distance)

