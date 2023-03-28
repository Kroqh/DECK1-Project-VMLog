import os
import shutil
from time import strptime

import Settings

LINES_PER_LOG = int(Settings.get_setting("READSPERLOG"))                    # number of lines of data per logfile
LOGPATH = Settings.get_setting("LOGPATH")
SEPARATOR = Settings.get_setting("SEPARATOR")                               # separator sign for values in file

def write_log(dict):                                                        # dict = dictionary (from sensor_readings)

    file = open(LOGPATH + "new/" + dict[0]["timestamp"] + ".txt", "x")      # file name is the first timestamp in the dataset

    counter = 0

    while counter < LINES_PER_LOG:
        dict[counter]
        file.write(
            dict["timestamp"]  + SEPARATOR + 
            str(dict["roll"])  + SEPARATOR +
            str(dict["pitch"]) + SEPARATOR + 
            str(dict["yaw"])   + SEPARATOR + 
            str(dict["acc_x"]) + SEPARATOR + 
            str(dict["acc_y"]) + SEPARATOR + 
            str(dict["acc_z"]) + "\n")
        counter += 1
    file.close()


def get_all_logs_in_new():
    return os.listdir(LOGPATH + "new/")


def move_log(path):
    shutil.move(LOGPATH + "new/" + path, LOGPATH + "old/")

def read_log(file_name, directory):
    """
        Returns the log for a logfile
        :param file: The name of the file
        :param directory: The name of the the folder
        :return: A dictionary of arrays, use time, pitch or roll, g_force_x, g_force_y, g_force_z to access the right array.
    """
    
    file = open(LOGPATH + directory + "/" +  file_name, "r")
    lines = file.read().split("\n")

    time_of_reading = []
    pitch = []
    roll = []
    g_force_x = []
    g_force_y = []
    g_force_z = []

    for line in lines:
        if line != "":
            stripped_line = line.split("&")
            time_of_reading.append(strptime(stripped_line[0], "%Y-%B-%d_%H_%M_%S"))
            pitch.append(float(stripped_line[1]))
            roll.append(float(stripped_line[2]))
            g_force_x.append(float(stripped_line[3]))
            g_force_y.append(float(stripped_line[4]))
            g_force_z.append(float(stripped_line[5]))

    return {"time": time_of_reading, "pitch": pitch, "roll": roll, "g_force_x": g_force_x,
            "g_force_y": g_force_y, "g_force_z": g_force_z}
