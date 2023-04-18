# libraries for base functionality
from sense_hat import SenseHat
import time
from datetime import datetime
import pandas as pd
import numpy as np
# our own scripts
import Settings
import LogHandler
import UploadHandler 
# libraries for TESTING/TIMING
#import random
from functools import wraps

# settings
LINES_PER_LOG = int(Settings.get_setting("READSPERLOG"))
DELAYTIME = float(Settings.get_setting("DELAYTIME"))
DECIMALS = int(Settings.get_setting("DECIMALROUNDING"))
LOGPATH = Settings.get_setting("LOGPATH")

# TEST FUNCTIONS

def timeit(func):       # vejledning fundet her https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
  @wraps(func)          # fungerer ved at skrive "@timeit" over en "def function..."
  def timeit_wrapper(*args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    #print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
    print(f"Function {func.__name__} Took {total_time:.4f} seconds")
    return result
  return timeit_wrapper

"""
def fake_sensor_reading():                      # test data - random float values between 0 and 360
    test_x = round(random.uniform(0, 360), DECIMALS)
    test_y = round(random.uniform(0, 360), DECIMALS)
    test_z = round(random.uniform(0, 360), DECIMALS)
    return test_x, test_y, test_z
"""

# FUNCTIONS
#@timeit
def get_accelerometer_geforce(sense):           # acceleration intensity (gravitational pull) on each axis measured in G
    acc = sense.get_accelerometer_raw()
    ax_g = round(acc['x'], DECIMALS)
    ay_g = round(acc['y'], DECIMALS)
    az_g = round(acc['z'], DECIMALS)
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

@timeit
def get_sensor_readings(sense):
    df = setup_dataframe()
    count = 0
    last_reading = 0    # "last epoch" timestamp til (mere) præcise delay mellem loop cycles
    
    while (count < LINES_PER_LOG):
        if (time.time() - last_reading >= DELAYTIME):
            last_reading = time.time() # set "last epoch" timestamp
            
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
        
    df = set_dtypes(df)
    return df


@timeit
def save_data_to_file(df_to_file):
    filepath = LOGPATH
    filename = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    filefull = filepath + filename + ".parquet"
    
    df_to_file.to_parquet(filefull, compression=None, index=False)

@timeit
def read_data_from_file(filefull):
    df_from_file = pd.read_parquet(filefull)
    return df_from_file

@timeit
def send_file_to_db():
    for log in LogHandler.get_all_filenames():
        log_df = LogHandler.read_data_from_file(log)
        succededBackLog = UploadHandler.post_http_single(log_df)
        print(succededBackLog)

# MAIN
sense = SenseHat()
while True:
   readings = get_sensor_readings(sense)
   readings = set_dtypes(readings)
   print(readings.info())
   #print(fromfile.head(10))
   save_data_to_file(readings) # "latestfile" er sti+filnavn... skal ændres til Marcus' løsning :)
   #fromfile = read_data_from_file(latestfile)
   #fromfile = set_dtypes(fromfile)
   #print("###########################")
   send_file_to_db()
   print("###########################")
   
