def WriteLog(time, pitch, roll):
    """
            Writes a logfile, saves in logs/new by default, name is the first time reading
            :param time: a string array of the time of the readings, already converted to string prior
            :param pitch: an array of the pitch readings
            :param roll: an array of the roll readings
        """
    file = open("logs/new/" + time[0] + ".txt", "x")

    counter = 0
    for count in time:
        file.write(time[counter] + "&" + str(pitch[counter]) + "&" + str(roll[counter]) + "\n")
        counter = counter + 1
    file.close()

def ReadLog(path):
    """
        Returns the log for a logfile
        :param path: full path to the file for now, fx logs/test/2023-March-12_16_33_56.txt
        :return: A dictionary of arrays, use time, pitch or roll to access the right array.
    """
    file = open(path, "r")
    lines = file.read().split("\n")

    time_of_reading = []
    pitch = []
    roll = []

    for line in lines:
        if line != "":
            stripped_line = line.split("&")
            time_of_reading.append(stripped_line[0])
            pitch.append(stripped_line[1])
            roll.append(stripped_line[2])

    return {"time": time_of_reading, "pitch": pitch, "roll": roll}
