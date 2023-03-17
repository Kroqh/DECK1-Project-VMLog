
import sense_hat
import time
from datetime import datetime
import LogHandler
import Settings

timesToRead = int(Settings.GetSetting("READSPERLOG"))
delayTime = float(Settings.GetSetting("DELAYTIME"))


def take_readings():
    count = 0
    time_of_reading = []
    pitch = []
    roll = []



    senseHat = sense_hat.SenseHat()
    while count < timesToRead:
        orientation = senseHat.get_orientation_degrees()
        time_of_reading.append(datetime.now().strftime("%Y-%B-%d_%H_%M_%S"))
        pitch.append(orientation["pitch"])
        roll.append(orientation["roll"])
        count = count + 1
        senseHat.set_pixels(get_panel(orientation["pitch"], orientation["roll"]))
        time.sleep(delayTime)

    LogHandler.WriteLog(time_of_reading, pitch, roll)
    print("reading finished")





def get_panel(pitch, roll):
    # Add negative if pitch or roll sways to much

    O = []
    X = [0, 0, 0]  # Black
    
    panel = []

    if (30 < roll < 330) or (30 < pitch < 330):
        O = [255, 0, 0] #red
        panel = [
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O,
        O, O, X, X, X, X, O, O,
        O, X, O, O, O, O, X, O,
        O, X, O, O, O, O, X, O,
        O, O, O, O, O, O, O, O
    ]
    else:
        O = [142, 252, 0] #green
        panel = [
        O, O, O, O, O, O, O, O,
        O, X, X, O, O, X, X, O,
        O, X, X, O, O, X, X, O,
        O, O, O, O, O, O, O, O,
        O, X, O, O, O, O, X, O,
        O, X, O, O, O, O, X, O,
        O, O, X, X, X, X, O, O,
        O, O, O, O, O, O, O, O
    ]
        
    return panel

while True:
        take_readings()