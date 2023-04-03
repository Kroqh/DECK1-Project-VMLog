import os
import shutil
from time import strptime
import Settings

# settings
LINES_PER_LOG = int(Settings.get_setting("READSPERLOG"))                    # number of lines of data per logfile
LOGPATH = Settings.get_setting("LOGPATH")
SEPARATOR = Settings.get_setting("SEPARATOR")                               # separator sign for values in file
NEWFOLDER = Settings.get_setting("FOLDER_NEW_LOGS")
OLDFOLDER = Settings.get_setting("FOLDER_OLD_LOGS")

# functions
def write_log(data_list):
    filename = data_list[0]
    file = open(LOGPATH + NEWFOLDER + filename["timestamp"] + ".txt", "x")   # file name is the first timestamp in the dataset
    for each_line in data_list:
        dict = each_line
        file.write(
            dict["timestamp"]  + SEPARATOR + 

            str(dict["roll"])  + SEPARATOR +
            str(dict["pitch"]) + SEPARATOR + 
            str(dict["yaw"])   + SEPARATOR + 

            str(dict["acc_x"]) + SEPARATOR + 
            str(dict["acc_y"]) + SEPARATOR + 
            str(dict["acc_z"]) + SEPARATOR +

            str(dict["gyr_x"]) + SEPARATOR + 
            str(dict["gyr_y"]) + SEPARATOR + 
            str(dict["gyr_z"]) + "\n"
        )
    file.close()


def get_path_new_logs():
    return os.listdir(LOGPATH + NEWFOLDER)


def move_log(file_name):
    shutil.move(LOGPATH + NEWFOLDER + file_name, LOGPATH + OLDFOLDER)

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
