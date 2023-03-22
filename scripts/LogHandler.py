import os
import shutil
from time import strptime

import Settings

LOGPATH = Settings.get_setting("LOGPATH")

def write_log(time, pitch, roll, g_force_x, g_force_y, g_force_z, succesfullySavedAlready):
    """
            Writes a logfile, saves in logs/new by default, name is the first time reading
            :param time: a string array of the time of the readings, already converted to string prior
            :param pitch: an array of the pitch readings
            :param roll: an array of the roll readings
        """
    if succesfullySavedAlready:
        file = open(LOGPATH + "old/" + time[0] + ".txt", "x")
    else:
        file = open(LOGPATH + "new/" + time[0] + ".txt", "x")

    counter = 0
    for count in time:
        file.write(time[counter] + "&" + str(pitch[counter]) + "&" + str(roll[counter]) + "&" + str(g_force_x[counter])
                   + "&" + str(g_force_y[counter]) + "&" + str(g_force_z[counter]) + "\n")
        counter = counter + 1
    file.close()


def get_all_logs_in_new():
    return os.listdir(LOGPATH + "new/")


def move_log(path):
    shutil.move(path, LOGPATH + "old/")

def read_log(path):
    """
        Returns the log for a logfile
        :param path: uses full path for the log file
        :return: A dictionary of arrays, use time, pitch or roll, g_force_x, g_force_y, g_force_z to access the right array.
    """
    file = open(path, "r")
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
            time_of_reading.append(strptime(stripped_line[0]), "%Y-%B-%d_%H_%M_%S")
            pitch.append(float(stripped_line[1]))
            roll.append(float(stripped_line[2]))
            g_force_x.append(float(stripped_line[3]))
            g_force_y.append(float(stripped_line[4]))
            g_force_z.append(float(stripped_line[5]))

    return {"time": time_of_reading, "pitch": pitch, "roll": roll, "g_force_x": g_force_x,
            "g_force_y": g_force_y, "g_force_z": g_force_z}
