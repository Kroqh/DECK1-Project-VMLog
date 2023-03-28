
from sense_hat import SenseHat
import time
from datetime import datetime
# import asyncio
import LogHandler
import Settings
import UploadHandler

# settings
LINES_PER_LOG = int(Settings.get_setting("READSPERLOG"))
DELAYTIME = float(Settings.get_setting("DELAYTIME"))
DECIMALS_IMU = int(Settings.get_setting("DECIMALROUNDING")) # motion sensors (gyro, accelerometer, magnetometer)
# DECIMALS_ENV = int(Settings.get_setting("DECIMALROUNDING")) # enviromental sensor (humidity, temperature)
TILT_LIMIT_DEGREES = int(Settings.get_setting("WARNINGDEGRESS"))

sense = SenseHat()

def get_accelerometer_geforce(sense):           # acceleration intensity (gravitational pull) on each axis measured in G
    acc = sense.get_accelerometer_raw()
    ax_g = round(acc['x'], DECIMALS_IMU)
    ay_g = round(acc['y'], DECIMALS_IMU)
    az_g = round(acc['z'], DECIMALS_IMU)
    return ax_g, ay_g, az_g

def get_orientation_degrees(sense):             # angle of each axis in degrees
    ori = sense.get_orientation_degrees()
    roll_d  = round(ori['roll'], DECIMALS_IMU)
    pitch_d = round(ori['pitch'], DECIMALS_IMU)
    yaw_d   = round(ori['yaw'], DECIMALS_IMU)
    return roll_d, pitch_d, yaw_d

def get_gyroscope_radians(sense):               # rotational intensity of each axis in radians/second
    gyr = sense.get_gyroscope_raw()
    gx_r = round(gyr['x'], DECIMALS_IMU)
    gy_r = round(gyr['y'], DECIMALS_IMU)
    gz_r = round(gyr['z'], DECIMALS_IMU)
    return gx_r, gy_r, gz_r

def data_to_database(dict):                   # dict = dictionary (from sensor_readings)
    #succeded = UploadHandler.post_http_single(dict)
    # return succeded
    # ????????
    # if succeded:
    #     for log in LogHandler.get_all_logs_in_new():
    #         # print(log)
    #         succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log, "new"))
    #         if succededBackLog:
    #             LogHandler.move_log(log)
    
    for log in LogHandler.get_all_logs_in_new():
        succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log, "new"))
        if succededBackLog:
            LogHandler.move_log(log)
    # return succededBackLog

def data_to_file(dict):                       # dict = dictionary (from sensor_readings)
    LogHandler.write_log(dict)
    
    

def sensor_readings():
    counter = 0
    dictionary = {}

    while counter < LINES_PER_LOG:
        roll, pitch, yaw = get_orientation_degrees()
        acc_x, acc_y, acc_z = get_accelerometer_geforce()
        gyr_rads_x, gyr_rads_y, gyr_rads_z = get_gyroscope_radians(sense)

        dictionary[counter] = {
            "timestamp": datetime.now().strftime("%Y-%B-%d_%H_%M_%S"),    # datetime converted to text (string)
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,
            "acc_x": acc_x,
            "acc_y": acc_y,
            "acc_z": acc_z,
            "gyr_rads_x":gyr_rads_x,
            "gyr_rads_y":gyr_rads_y,
            "gyr_rads_z":gyr_rads_z
        }
        counter += 1
        time.sleep(DELAYTIME)
        
    return dictionary

while True:
        #loop = asyncio.get_event_loop()
        #asyncio.ensure_future(data_readout = sensor_readings())
        data_readout = sensor_readings()
        if data_readout != null:
            data_to_file(data_readout)

        data_to_database(data_readout)
    
        #asyncio.ensure_future(data_to_file(data_readout))

        # data_to_database(timestamp, pitch, roll, g_force_x, g_force_y, g_force_z)
