
from sense_hat import SenseHat
import time
from datetime import datetime
# import asyncio
import LogHandler
import Settings
# import UploadHandler

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

# async def data_to_database(dict):                   # dict = dictionary (from sensor_readings)
#     succeded = UploadHandler.post_http_single({
#         "time": timestamp, 
#         "pitch": pitch, 
#         "roll": roll, 
#         "g_force_x": g_force_x,
#         "g_force_y": g_force_y, 
#         "g_force_z": g_force_z
#         })
#     return succeded

def data_to_file(dict):                       # dict = dictionary (from sensor_readings)
    LogHandler.write_log(dict)
    
    # ????????
    # if succeded:
    #     for log in LogHandler.get_all_logs_in_new():
    #         print(log)
    #         succededBackLog = UploadHandler.post_http_single(LogHandler.read_log(log, "new"))
    #         if succededBackLog:
    #             LogHandler.move_log(log)
    # return succeded

def sensor_readings():
    counter = 0
    dictionary = {}

    while counter < LINES_PER_LOG:
        roll, pitch, yaw = get_orientation_degrees()
        acc_x, acc_y, acc_z = get_accelerometer_geforce()

        dictionary[counter] = {
            "timestamp": datetime.now().strftime("%Y-%B-%d_%H_%M_%S"),    # datetime converted to text (string)
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw,
            "acc_x": acc_x,
            "acc_y": acc_y,
            "acc_z": acc_z
        }
        counter += 1
        time.sleep(DELAYTIME)
        
    return dictionary


while True:
        #loop = asyncio.get_event_loop()
        #asyncio.ensure_future(data_readout = sensor_readings())
        data_readout = sensor_readings()

        # data_to_database(data_readout)
    
        #asyncio.ensure_future(data_to_file(data_readout))

        # data_to_database(timestamp, pitch, roll, g_force_x, g_force_y, g_force_z)
    
        data_to_file(data_readout)
