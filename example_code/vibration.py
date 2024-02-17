from adafruit_circuitplayground import cp
import digitalio
import board
motor = digitalio.DigitalInOut(board.A4)
motor.switch_to_output()
while True:
    if cp.button_a:
        motor.value = True
    else:
        motor.value = False

