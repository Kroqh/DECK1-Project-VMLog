import matplotlib.pyplot as plt
import LogHandler


def plot_log(path):
    log = equalize(LogHandler.ReadLog(path))
    plt.plot(log.get("pitch"), label="pitch")
    plt.plot(log.get("roll"), label="roll")
    plt.legend()
    plt.ylim(0,360)
    plt.show()
    
def equalize(log):
    
    """
        The sensor currently reads with its equilibrium point being 0/360, which looks ugly graphed,
        this function therefore changes the equilibrium point to 180 for a prettier graph.
        :param log: the dictionary to be converted, needs a a roll and pitch array
        :return: An equalized dictionary with a roll and pitch array
    """
    
    new_pitch = []
    new_roll = []
    for pitch in log.get("pitch"):
        
        if pitch <= 180:
            pitch = pitch + 180
        else:
            pitch = pitch - 180
        new_pitch.append(pitch)
        
    for roll in log.get("roll"):
        if roll <= 180:
            roll = roll + 180
        else:
            roll = roll - 180
        new_roll.append(roll)
        
    return {"pitch": new_pitch, "roll": new_roll}
            