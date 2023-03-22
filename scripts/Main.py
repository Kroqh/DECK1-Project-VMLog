
import sense_hat
import time
from datetime import datetime
import LogHandler
import Settings
import UploadHandler

timesToRead = int(Settings.get_setting("READSPERLOG"))
delayTime = float(Settings.get_setting("DELAYTIME"))
decimalsToRound = int(Settings.get_setting("DECIMALROUNDING"))
warning_degress = int(Settings.get_setting("WARNINGDEGRESS"))


def take_readings():
    count = 0
    time_of_reading = []
    pitch = []
    roll = []
    g_force_x = []
    g_force_y = []
    g_force_z = []



    senseHat = sense_hat.SenseHat()
    while count < timesToRead:
        orientation = senseHat.get_orientation_degrees()
        accel_raw = senseHat.get_accelerometer_raw()
        time_of_reading.append(datetime.now().strftime("%Y-%B-%d_%H_%M_%S"))

        pitch.append(round(orientation["pitch"], decimalsToRound))
        roll.append(round(orientation["roll"], decimalsToRound))
        g_force_x.append(round(accel_raw.get("x"), decimalsToRound))
        g_force_y.append(round(accel_raw.get("y"), decimalsToRound))
        g_force_z.append(round(accel_raw.get("z"), decimalsToRound))

        count = count + 1
        senseHat.set_pixels(get_panel(orientation["pitch"], orientation["roll"]))
        time.sleep(delayTime)

    succeded = UploadHandler.post_http_single({"time": time_of_reading, "pitch": pitch, "roll": roll, "g_force_x": g_force_x,
            "g_force_y": g_force_y, "g_force_z": g_force_z})
    LogHandler.write_log(time_of_reading, pitch, roll, g_force_x, g_force_y, g_force_y, succeded)
    if succeded:
        for log in LogHandler.get_all_logs_in_new():
            succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log))
            if succededBackLog:
                LogHandler.move_log(log)


    print("reading finished")





def get_panel(pitch, roll):
    # Add negative if pitch or roll sways to much

    O = []
    X = [0, 0, 0]  # Black
    
    panel = []

    if (warning_degress < roll < 360 - warning_degress) or (warning_degress < pitch < 360 - warning_degress):
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