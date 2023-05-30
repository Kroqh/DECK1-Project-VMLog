# libraries for base functionality
from sense_hat import SenseHat
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
import json
import requests
import shutil
# our own scripts
import settings
# libraries for TESTING/TIMING
#import random
from functools import wraps

# settings
LINES_PER_LOG = int(settings.get_setting("READSPERLOG"))
DELAYTIME = float(settings.get_setting("DELAYTIME"))
DECIMALS = int(settings.get_setting("DECIMALROUNDING"))
LOGPATH = settings.get_setting("LOGPATH")
api_key = settings.get_setting("KEY")
logger_id = settings.get_setting("LOGGERID")


# TEST FUNCTIONS (timeit NEEDS to be at the top)

def timeit(func):       # vejledning fundet her https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
  @wraps(func)          # fungerer ved at skrive "@timeit" over en "def function..."
  def timeit_wrapper(*args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    #print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
    write_to_system_log(f"Function {func.__name__} Took {total_time:.4f} seconds")
    return result
  return timeit_wrapper


# MAIN FUNCTION

def main():
    sense = SenseHat()
    write_to_system_log("VMLogger initiated at " + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + " with the following parameters: " + str(LINES_PER_LOG ) + " readings per log " + " with a " + str(DELAYTIME) + "s delay\n") 
    while True:
        readings = get_sensor_readings(sense)
        readings = set_dtypes(readings)
        print(readings.info())
        save_data_to_file(readings)
        send_file_to_db()
        write_to_system_log("\n")


# FUNCTIONS

#@timeit
def get_accelerometer_geforce(sense):           # acceleration intensity (gravitational pull) on each axis measured in G
    acc = sense.get_accelerometer_raw()
    ax_g = round(acc['x'], DECIMALS) * 10       # *10 to get gravitational pull as e.g. 9.813 m/s²
    ay_g = round(acc['y'], DECIMALS) * 10
    az_g = round(acc['z'], DECIMALS) * 10
    return ax_g, ay_g, az_g

#@timeit
def get_orientation_degrees(sense):             # angle of each axis in degrees
    ori = sense.get_orientation_degrees()
    roll_d  = round(ori['roll'], DECIMALS)
    pitch_d = round(ori['pitch'], DECIMALS)
    yaw_d   = round(ori['yaw'], DECIMALS)
    return roll_d, pitch_d, yaw_d

#@timeit
def get_gyroscope_radians(sense):               # rotational intensity of each axis in radians/second
    gyr = sense.get_gyroscope_raw()
    gx_r = round(gyr['x'], DECIMALS)
    gy_r = round(gyr['y'], DECIMALS)
    gz_r = round(gyr['z'], DECIMALS)
    return gx_r, gy_r, gz_r

def setup_dataframe():
    df = pd.DataFrame(          # predefining columns and data types for memory efficiency
        # column name : data type (via NumPy's data types e.g. np.float16)
        columns={
            "timestamp": datetime,
            
            "roll": np.int16,
            "pitch": np.int16,
            "yaw": np.int16,

            "acc_x": np.float16,
            "acc_y": np.float16,
            "acc_z": np.float16,

            "gyr_x": np.float16,
            "gyr_y": np.float16,
            "gyr_z": np.float16
        }
    )
    return df

#@timeit
def set_dtypes(df):
    
  df["timestamp"] = df["timestamp"].astype(str)
  df["roll"] = df["roll"].astype(np.int16)
  df["pitch"] = df["pitch"].astype(np.int16)
  df["yaw"] = df["yaw"].astype(np.int16)

  df["acc_x"] = df["acc_x"].astype(np.float16)
  df["acc_y"] = df["acc_y"].astype(np.float16)
  df["acc_z"] = df["acc_z"].astype(np.float16)

  df["gyr_x"] = df["gyr_x"].astype(np.float16)
  df["gyr_y"] = df["gyr_y"].astype(np.float16)
  df["gyr_z"] = df["gyr_z"].astype(np.float16)
  
  return df
  
def set_dtypes_db(df):
    
  df["timestamp"] = df["timestamp"].astype(str)
  df["roll"] = df["roll"].astype(np.int16)
  df["pitch"] = df["pitch"].astype(np.int16)
  df["yaw"] = df["yaw"].astype(np.int16)
  
  return df

#@timeit
def round_column_values(df):    # rounds down / sets number of decimals for specific (df) columns
    df = df.round(
        {
            "acc_x": DECIMALS, 
            "acc_y": DECIMALS, 
            "acc_z": DECIMALS, 
            "gyr_x": DECIMALS, 
            "gyr_y": DECIMALS, 
            "gyr_z": DECIMALS
        }
    )
    return df
    

@timeit
def get_sensor_readings(sense):
    df = setup_dataframe()
    count = 0
    last_reading = 0    # "last epoch" timestamp til (mere) præcise delay mellem loop cycles
    
    while (count < LINES_PER_LOG):
        if (time.time() - last_reading >= DELAYTIME):
            last_reading = time.time()
            
            timestamp = datetime.now()
            roll, pitch, yaw = get_orientation_degrees(sense)
            acc_x, acc_y, acc_z = get_accelerometer_geforce(sense)
            gyr_x, gyr_y, gyr_z = get_gyroscope_radians(sense)
            
            reading = pd.DataFrame(
              {
              "timestamp": [timestamp],
               
              "roll": [roll],
              "pitch": [pitch],
              "yaw": [yaw],
               
              "acc_x": [acc_x],
              "acc_y": [acc_y],
              "acc_z": [acc_z],
               
              "gyr_x": [gyr_x],
              "gyr_y": [gyr_y],
              "gyr_z": [gyr_z]
              }
            )
            df = pd.concat([df, reading], ignore_index=True)
            count = count + 1
        
    # df = set_dtypes(df)
    return df

def get_all_filenames_in_new():  # returnerer alle filnavne i folder
    return os.listdir(LOGPATH + "new/")
"""
def save_data_to_file(df_to_file):
    filepath = LOGPATH + "new/"
    filename = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    filetype = ".parquet"
    filefull = filepath + filename + filetype
    
    df_to_file.to_parquet(filefull, compression=None, index=False)
"""
@timeit
def save_data_to_file(df_to_file):
    filepath = LOGPATH + "new/"
    filename = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    filetype = ".csv"
    filefull = filepath + filename + filetype
    
    df_to_file.to_csv(filefull, compression=None, index=False)

"""    
def read_data_from_file(file_to_df): # fra (parquet) fil til dataframe
    df_from_file = pd.read_parquet(file_to_df)
    return df_from_file
"""
def read_data_from_file(file_to_df): 
    df_from_file = pd.read_csv(file_to_df)
    return df_from_file
    
def write_to_system_log(text):              # logger driftsinformationer fra scripts
    print(text)
    sysfile = open(LOGPATH + "syslog/syslog.txt", "a")
    sysfile.write(text + "\n")
    sysfile.close()

"""
def move_file(path, new_name):     # flytter filer fra én mappe til en anden
    shutil.move(LOGPATH + "new/" + path, LOGPATH + "old/")
    os.rename(LOGPATH + "old/" + path, LOGPATH + "old/" + new_name + ".parquet")
"""
def move_file(old_name, new_name):     # flytter filer fra én mappe til en anden
    shutil.move(LOGPATH + "new/" + old_name, LOGPATH + "old/")
    os.rename(LOGPATH + "old/" + old_name, LOGPATH + "old/" + new_name + ".csv")    

@timeit
def post_http_single(log_df): #Returns response
    log_df = set_dtypes_db(log_df)
    log_df = round_column_values(log_df)
    print(log_df.head(10))
    dictionary = log_df.to_dict()
    try:
        url = "https://westeurope.azure.data.mongodb-api.com/app/data-mgxzs/endpoint/data/v1/action/insertOne"
        payload = json.dumps(
            {
            "collection": "motion_data",
            "database": "VMLog",
            "dataSource": "VMLog",

            "document": {
                "logger_id": logger_id,
                "local_time_for_upload": datetime.now().strftime('%Y-%m-%d_%H_%M_%S'),
                "timestamp": dictionary.get("timestamp"),
                "roll": dictionary.get("roll"),
                "pitch": dictionary.get("pitch"),
                "yaw": dictionary.get("yaw"),
                "acc_x": dictionary.get("acc_x"),
                "acc_y": dictionary.get("acc_y"),
                "acc_z": dictionary.get("acc_z"),
                "gyr_x": dictionary.get("gyr_x"),
                "gyr_y": dictionary.get("gyr_y"),
                "gyr_z": dictionary.get("gyr_z")
            
            }
            }
        )
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': api_key,
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        """
        LogHandler.write_to_system_log
        if response.ok:
            LogHandler.write_to_system_log("Log succesfully uploaded with id: " + response.text)
            return True
        else:
            LogHandler.write_to_system_log("Log upload failed, error message: " + response.text)
            return False
        """
        if response.ok:
            write_to_system_log("Log succesfully uploaded with id: " + response.text)
            return response
        else:
            write_to_system_log("Log upload failed, error message: " + response.text)
            return response
        
    except Exception as err:
        #LogHandler.write_to_system_log("Upload failed, exception: " + str(err))
        write_to_system_log("Upload failed, exception: " + str(err))
        return None



@timeit
def send_file_to_db():
    for log in get_all_filenames_in_new():
        log_df = read_data_from_file(LOGPATH + "new/" + log)
        succeded = post_http_single(log_df)
        if ((succeded is None) or (not succeded.ok)):
            write_to_system_log("Upload failed")
            break
        else:
            move_file(log, json.loads(succeded.text)["insertedId"])
            write_to_system_log("Upload succesful")

# run MAIN
if __name__ == "__main__":
    main()
