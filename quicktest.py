from datetime import datetime
import LogHandler
import Plotter

#print(datetime.now())

#WriteLog([datetime.now().strftime("%Y-%B-%d_%H_%M_%S"), datetime.now().strftime("%Y-%B-%d_%H_%M_%S")],[0,5], [3,6])

#print(LogHandler.ReadLog("logs/test/2023-March-12_16_33_56.txt").get("roll")[0])

Plotter.plot_log("logs/test/2023-March-12_16_33_56.txt")