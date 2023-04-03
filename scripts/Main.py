
from sense_hat import SenseHat
# import time
from datetime import datetime
import asyncio
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

#functions
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

def data_to_database():                   # dict = dictionary (from sensor_readings)
    #succeded = UploadHandler.post_http_single(dict)
    # return succeded
    # ????????
    # if succeded:
    #     for log in LogHandler.get_all_logs_in_new():
    #         # print(log)
    #         succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log, "new"))
    #         if succededBackLog:
    #             LogHandler.move_log(log)
    
    for log_file in LogHandler.get_path_new_logs():
        succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log_file, "new"))
        if succededBackLog:
            LogHandler.move_log(log_file)
    # return succededBackLog

def data_to_file(dict):                       # dict = dictionary (from sensor_readings)
    LogHandler.write_log(dict)
    
"""    
# v1
def sensor_readings(sense):
    line_counter = 0
    dictionary = {}

    while line_counter < LINES_PER_LOG:
        roll, pitch, yaw = get_orientation_degrees(sense)
        acc_x, acc_y, acc_z = get_accelerometer_geforce(sense)
        gyr_rads_x, gyr_rads_y, gyr_rads_z = get_gyroscope_radians(sense)

        dictionary[line_counter] = {
            "timestamp": datetime.now().strftime("%Y-%B-%d_%H_%M_%S"),    # datetime converted to text (string)
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,
            "acc_x": acc_x,
            "acc_y": acc_y,
            "acc_z": acc_z,
            "gyr_rads_x": gyr_rads_x,
            "gyr_rads_y": gyr_rads_y,
            "gyr_rads_z": gyr_rads_z
        }
        line_counter += 1
        time.sleep(DELAYTIME)
        
    return dictionary
"""
# v2
def sensor_readings(sense):
    for line in range(LINES_PER_LOG):

        timestamp = datetime.now().strftime("%Y-%B-%d_%H_%M_%S")
        roll, pitch, yaw    = get_orientation_degrees(sense)
        acc_x, acc_y, acc_z = get_accelerometer_geforce(sense)
        gyr_x, gyr_y, gyr_z = get_gyroscope_radians(sense)

        readings = {
            "timestamp": [].append(timestamp),

            "roll":  [].append(roll),
            "pitch": [].append(pitch),
            "yaw":   [].append(yaw),

            "acc_x": [].append(acc_x),
            "acc_y": [].append(acc_y),
            "acc_z": [].append(acc_z),

            "gyr_x": [].append(gyr_x),
            "gyr_y": [].append(gyr_y),
            "gyr_z": [].append(gyr_z)
        }
        asyncio.sleep(DELAYTIME)    # for async usage
    return readings

# MAIN

while True:
        #loop = asyncio.get_event_loop()
        #asyncio.ensure_future(data_readout = sensor_readings())
        readings = sensor_readings(sense)
        if readings != null:
            data_to_file(readings)

        data_to_database(readings)
    
        #asyncio.ensure_future(data_to_file(data_readout))

        # data_to_database(timestamp, pitch, roll, g_force_x, g_force_y, g_force_z)
