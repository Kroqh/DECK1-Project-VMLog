# libraries for base functionality
from sense_hat import SenseHat
import time
from datetime import datetime
import pandas as pd
import numpy as np
# libraries for TESTING
import random
from functools import wraps
# our own scripts
import Settings

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
    print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
    return result
  return timeit_wrapper

def fake_sensor_reading():                      # test data - random float values between 0 and 360
    test_x = round(random.uniform(0, 360), DECIMALS)
    test_y = round(random.uniform(0, 360), DECIMALS)
    test_z = round(random.uniform(0, 360), DECIMALS)
    return test_x, test_y, test_z

# FUNCTIONS

def get_accelerometer_geforce(sense):           # acceleration intensity (gravitational pull) on each axis measured in G
    acc = sense.get_accelerometer_raw()
    ax_g = round(acc['x'], DECIMALS)
    ay_g = round(acc['y'], DECIMALS)
    az_g = round(acc['z'], DECIMALS)
    return ax_g, ay_g, az_g

def get_orientation_degrees(sense):             # angle of each axis in degrees
    ori = sense.get_orientation_degrees()
    roll_d  = round(ori['roll'], DECIMALS)
    pitch_d = round(ori['pitch'], DECIMALS)
    yaw_d   = round(ori['yaw'], DECIMALS)
    return roll_d, pitch_d, yaw_d

def get_gyroscope_radians(sense):               # rotational intensity of each axis in radians/second
    gyr = sense.get_gyroscope_raw()
    gx_r = round(gyr['x'], DECIMALS)
    gy_r = round(gyr['y'], DECIMALS)
    gz_r = round(gyr['z'], DECIMALS)
    return gx_r, gy_r, gz_r

@timeit
def setup_dataframe():
    df = pd.DataFrame(          # predefining columns and data types for memory efficiency
        # column name : data type (configurable via NumPy e.g. np.float32)
        columns={
            
            "timestamp": np.datetime64,
            
            "roll": np.float16,
            "pitch": np.float16,
            "yaw": np.float16,

            "acc_x": np.float16,
            "acc_y": np.float16,
            "acc_z": np.float16,

            "gyr_x": np.float16,
            "gyr_y": np.float16,
            "gyr_z": np.float16
        }
    )
    return df

@timeit
def set_dtypes(df):
  df["timestamp"] = df["timestamp"].astype(np.datetime64)

  df["roll"] = df["roll"].astype(np.float16)
  df["pitch"] = df["pitch"].astype(np.float16)
  df["yaw"] = df["yaw"].astype(np.float16)

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
    for line in range(LINES_PER_LOG):
        timestamp = datetime.datetime.now()
        # roll, pitch, yaw = get_orientation_degrees(sense)
        # acc_x, acc_y, acc_z = get_accelerometer_geforce(sense)
        # gyr_x, gyr_y, gyr_z = get_gyroscope_radians(sense)
        roll, pitch, yaw = fake_sensor_reading()
        acc_x, acc_y, acc_z = fake_sensor_reading()
        gyr_x, gyr_y, gyr_z = fake_sensor_reading()

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
        time.sleep(DELAYTIME)

    return df

# def save_data_to_file(df_to_file):
#    df = setup_dataframe()
#    df = pd.concat([df, df_to_file], ignore_index=True)
#    df.to

# MAIN
while True:
   sense = SenseHat()
   readings = get_sensor_readings(sense)
   readings = set_dtypes(readings)
   print("###########################")
   print(readings.info())
   print("###########################")
   print(readings.head(5))
   print("###########################")