from sense_hat import SenseHat
import time

sense = SenseHat()

G = (0, 255, 0)

def blinky_blinky(sense):
    sense.set_pixel(7, 7, G)
    time.sleep(0.5)
    sense.clear()
    time.sleep(3)

for i in range(10):
    blinky_blinky(sense)