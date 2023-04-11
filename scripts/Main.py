
from sense_hat import SenseHat
import time
from datetime import datetime
# import asyncio
import pandas as pd
import numpy as np
import LogHandler
import Settings
import UploadHandler

# settings
LINES_PER_LOG = int(Settings.get_setting("READSPERLOG"))
DELAYTIME = float(Settings.get_setting("DELAYTIME"))
DECIMALS_IMU = int(Settings.get_setting("DECIMALROUNDING")) # motion sensors (gyro, accelerometer, magnetometer)
# DECIMALS_ENV = int(Settings.get_setting("DECIMALROUNDING")) # enviromental sensor (humidity, temperature)
# TILT_LIMIT_DEGREES = int(Settings.get_setting("WARNINGDEGRESS"))

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

def data_to_database():
    for log_file in LogHandler.get_path_new_logs():
        succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log_file, "new"))
        if succededBackLog:
            LogHandler.move_log(log_file)
    # return succededBackLog

def data_to_file(readings_df):                       # dict = dictionary (from sensor_readings)
    LogHandler.write_log(readings_df)

def sensor_readings(sense):

    df = pd.DataFrame(          # predefining columns and data types for memory efficiency
        columns={
            # name : data type
            "timestamp": np.object,
            
            "roll": np.float32,
            "pitch": np.float32,
            "yaw": np.float32,

            "acc_x": np.float32,
            "acc_y": np.float32,
            "acc_z": np.float32,

            "gyr_x": np.float32,
            "gyr_y": np.float32,
            "gyr_z": np.float32,
        }
    )
    
    for line in range(LINES_PER_LOG):   # runs loop from 0 to {LINES_PER_LOG}

        timestamp = datetime.now().strftime("%Y-%B-%d_%H_%M_%S")
        roll, pitch, yaw = get_orientation_degrees(sense)
        acc_x, acc_y, acc_z = get_accelerometer_geforce(sense)
        gyr_x, gyr_y, gyr_z = get_gyroscope_radians(sense)

        reading={                     # dictionary with sensor data from this loop cycle
            "timestamp": timestamp,

            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,

            "acc_x": acc_x,
            "acc_y": acc_y,
            "acc_z": acc_z,

            "gyr_x": gyr_x,
            "gyr_y": gyr_y,
            "gyr_z": gyr_z
        }
        df = df.append(reading, ignore_index=True)  # add data from dictionary to dataframe 
        # asyncio.sleep(DELAYTIME)    # for async usage
        time.sleep(DELAYTIME)
    print(df.info())
    print(df.head())
    return df

# MAIN

sense = SenseHat()
while True:
        #loop = asyncio.get_event_loop()
        #asyncio.ensure_future(data_readout = sensor_readings())
        readings_df = sensor_readings(sense)
        if (readings_df.size != 0):
            data_to_file(readings_df)

        # data_to_database(readings_df)
    
        #asyncio.ensure_future(data_to_file(data_readout))

        # data_to_database(timestamp, pitch, roll, g_force_x, g_force_y, g_force_z)
