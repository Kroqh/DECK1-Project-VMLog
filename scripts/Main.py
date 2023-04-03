
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
visuals = Settings.get_setting("VISUALS").lower() == "true"

LogHandler.write_to_system_log("VMLogger initiated at " + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + " with the following parameters: " + str(timesToRead) + " readings per log " + " with a " + str(delayTime) + "s delay\n") 


def take_readings():
    LogHandler.write_to_system_log("Logfile creation initated at " + datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
    log_start_time = time.time()
    count = 0
    time_of_reading = []
    pitch = []
    roll = []
    g_force_x = []
    g_force_y = []
    g_force_z = []
    senseHat = sense_hat.SenseHat()
    
    last_reading = 0
    while count < timesToRead:
        if (time.time() - last_reading >= delayTime):
            last_reading = time.time()
            orientation = senseHat.get_orientation_degrees()
            accel_raw = senseHat.get_accelerometer_raw()
            time_of_reading.append(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))

            pitch.append(round(orientation["pitch"], decimalsToRound))
            roll.append(round(orientation["roll"], decimalsToRound))
            g_force_x.append(round(accel_raw.get("x"), decimalsToRound))
            g_force_y.append(round(accel_raw.get("y"), decimalsToRound))
            g_force_z.append(round(accel_raw.get("z"), decimalsToRound))

            count = count + 1
            if visuals:
                senseHat.set_pixels(get_panel(orientation["pitch"], orientation["roll"]))
            
            
            
    LogHandler.write_to_system_log("Theoretical time it should have taken: " + str(timesToRead*delayTime))
    diff = time.time() - log_start_time
    LogHandler.write_to_system_log("Actual time taken: " + str(diff))

    succeded = UploadHandler.post_http_single({"time": time_of_reading, "pitch": pitch, "roll": roll, "g_force_x": g_force_x,
            "g_force_y": g_force_y, "g_force_z": g_force_z})
    LogHandler.write_log(time_of_reading, pitch, roll, g_force_x, g_force_y, g_force_y, succeded)
    if succeded:
        for log in LogHandler.get_all_logs_in_new():
            LogHandler.write_to_system_log("Found "+ log + " in backlog, will attempt to uploaded")
            succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log, "new"))
            if succededBackLog:
                LogHandler.move_log(log)
        diff = time.time() - log_start_time
        LogHandler.write_to_system_log("Postupload time taken: " + str(diff))


    LogHandler.write_to_system_log("Logfile creation finished\n")

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
