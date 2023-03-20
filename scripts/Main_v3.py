from sense_hat import SenseHat
import time

# settings

delay_seconds = 1     # setting time between readings
decimals_imu = 2        # setting number of decimals for the IMU (motion sensor) readings
sense = SenseHat()      # instance of SenseHat to be used
base_x = 0
base_y = 0
base_z = 0
base_x_lowerlimit = 0
base_x_upperlimit = 0
# sensor_data = []        # list for storing data

# definition of functions to be used

def get_gyroscope_degrees(sense):               # angle of the axis in degrees (degrees/second?)
    gyr = sense.get_gyroscope()
    gx_d = round(gyr['roll'], decimals_imu)
    gy_d = round(gyr['pitch'], decimals_imu)
    gz_d = round(gyr['yaw'], decimals_imu)
    return gx_d, gy_d, gz_d

def get_gyroscope_radians(sense):               # rotational intensity of the axis in radians/second
    gyr = sense.get_gyroscope_raw()
    gx_r = round(gyr['x'], decimals_imu)
    gy_r = round(gyr['y'], decimals_imu)
    gz_r = round(gyr['z'], decimals_imu)
    return gx_r, gy_r, gz_r

def get_accelerometer_degrees(sense):           # angle of the axis in degrees
    acc = sense.get_accelerometer()
    ax_d = round(acc['roll'], decimals_imu)
    ay_d = round(acc['pitch'], decimals_imu)
    az_d = round(acc['yaw'], decimals_imu)
    return ax_d, ay_d, az_d

def get_accelerometer_geforce(sense):           # acceleration intensity of the axis in G
    acc = sense.get_accelerometer_raw()
    ax_g = round(acc['x'], decimals_imu)
    ay_g = round(acc['y'], decimals_imu)
    az_g = round(acc['z'], decimals_imu)
    return ax_g, ay_g, az_g

def get_magnetometer_data(sense):               # magnetic intensity of the axis in microtesla 
    mag = sense.get_compass_raw()
    mx = round(mag['x'], decimals_imu)
    my = round(mag['y'], decimals_imu)
    mz = round(mag['z'], decimals_imu)
    return mx, my, mz

def get_orientation_degrees(sense):             # angle of the axis in degrees
    ori = sense.get_orientation_degrees()
    roll_d  = round(ori['roll'], decimals_imu)
    pitch_d = round(ori['pitch'], decimals_imu)
    yaw_d   = round(ori['yaw'], decimals_imu)
    return roll_d, pitch_d, yaw_d

def get_orientation_radians(sense):             # angle of the axis in radians
    ori = sense.get_orientation_radians()
    roll_r  = round(ori['roll'], decimals_imu)
    pitch_r = round(ori['pitch'], decimals_imu)
    yaw_r   = round(ori['yaw'], decimals_imu)
    return roll_r, pitch_r, yaw_r

def set_parameter_limit():
    if (base_x+30)>360:
        base_x_lowerlimit = base_x+30-360
    else:
        base_x_lowerlimit = base_x+30
    if (base_x-30)<0:
        base_x_upperlimit = base_x-30+360
    else:
        base_x_upperlimit = base_x-30
    return base_x_lowerlimit, base_x_upperlimit
# main
roll_d, pitch_d, yaw_d = get_orientation_degrees(sense)
print("###base level###")
print({roll_d}, {pitch_d}, {yaw_d})
base_x = roll_d
base_y = pitch_d
base_z = yaw_d
print("###base level###")

base_x_lowerlimit, base_x_upperlimit = set_parameter_limit()

while True:

    gx_d, gy_d, gz_d = get_gyroscope_degrees(sense)
    gx_r, gy_r, gz_r = get_gyroscope_radians(sense)

    ax_d, ay_d, az_d = get_accelerometer_degrees(sense)
    ax_g, ay_g, az_g = get_accelerometer_geforce(sense)

    mx, my, mz = get_magnetometer_data(sense)

    roll_d, pitch_d, yaw_d = get_orientation_degrees(sense)
    roll_r, pitch_r, yaw_r = get_orientation_radians(sense)

    # sensor_data.append({
    #     'gx_d' : gx_d,
    #     'gy_d' : gy_d,
    #     'gz_d' : gz_d,
    #     'gx_r' : gx_r,
    #     'gy_r' : gy_r,
    #     'gz_r' : gz_r,
        
    # })

    # print(f"Gyro (deg/sec) - x: " + {gx_d} + ", y: " + {gy_d} + ", z: " + {gz_d})
    # print(f"Gyro (rad/sec) - x: {gx_r}, y: {gy_r}, z: {gz_r}")

    # print(f"Accel (deg) - x: {ax_d}, y: {ay_d}, z: {az_d}")
    # print(f"Accel (G) - x: {ax_g}, y: {ay_g}, z: {az_g}")

    # print(f"Magnet (microtesla) - x: {mx}, y: {my}, z: {mz}")

    # print(f"Orientation (degrees) - x: {roll_d}, y: {pitch_d}, z: {yaw_d}")
    # print(f"Orientation (radians) - x: {roll_r}, y: {pitch_r}, z: {yaw_r}")

    # print("")

    #print("Gyro (deg/sec), ")
    #print({gx_d}, {gy_d}, {gz_d})
    print("Gyro (rad/sec)")
    print({gx_r}, {gy_r}, {gz_r})

    #print("Accel (deg)")
    #print({ax_d}, {ay_d}, {az_d})
    print("Accel (G)")
    print({ax_g}, {ay_g}, {az_g})

    print("Magnet (microtesla)")
    print({mx}, {my}, {mz})

    print("Orientation (degrees)")
    print({roll_d}, {pitch_d}, {yaw_d})
    #print("Orientation (radians)")
    #print({roll_r}, {pitch_r}, {yaw_r})
    print(f"lower limit: {base_x_lowerlimit}")
    print(f"upper limit: {base_x_upperlimit}")
    if (roll_d > base_x_lowerlimit) and (roll_d < base_x_upperlimit):
           print("hjælp")


    print("")
    time.sleep(delay_seconds)