import matplotlib.pyplot as plt
import LogHandler


def plot_log(path):
    log = LogHandler.ReadLog(path)
    plt.plot(log.get("pitch"), label="pitch")
    plt.plot(log.get("roll"), label="roll")
    plt.legend()
    plt.show()