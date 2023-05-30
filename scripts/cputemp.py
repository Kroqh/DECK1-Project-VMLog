import time
from gpiozero import CPUTemperature

def get_cpu_temperature():
    current_cpu_temp = CPUTemperature()
    return current_cpu_temp


for i in range(100):
    curr_cpu_temp = get_cpu_temperature()
    print(f"CPU Temp: {curr_cpu_temp.temperature:.1f} *C")
    time.sleep(1)