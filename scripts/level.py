from sense_hat import SenseHat
import time

sense = SenseHat()
DECIMALS = 4

G = (0, 255, 0)     # GREEN
Y = (255, 255, 0)   # YELLOW
O = (255, 140, 0)   # ORANGE
R = (255, 0, 0)     # RED
X = (0,0,0)         # BLACK (OFF)

# MAIN FUNCTION

def main():      
  #for i in range(1000):  
  while True: 
    roll_angle, pitch_angle = get_orientation_degrees(sense)  # for LED
    acc_x, acc_y, acc_z = get_accelerometer_geforce(sense)    # DECK1 demo request
    acc_x = round(acc_x * 10, 3)    # *10 to get gravitational pull as e.g. 9.81 (m/s²)
    acc_y = round(acc_y * 10, 3)    # *10 to get gravitational pull as e.g. 9.81 (m/s²)
    acc_z = round(acc_z * 10, 3)    # *10 to get gravitational pull as e.g. 9.81 (m/s²)
   
    print('The value of acc_x :',acc_x)      # terminal
    print('The value of acc_y :',acc_y) 
    print('The value of acc_y :',acc_z) 
    
    print(roll_angle, pitch_angle)  # terminal
    
    sense.clear()                   # clears previous LEDs
    set_roll_level(roll_angle)      # show LEDs for roll
    set_pitch_level(pitch_angle)    # show LEDs for pitch
    time.sleep(0.010)               # short enough delay for (acceptable) sensor precision (200Hz), but slow enough for LED matrix to react/show proberly

# FUNCTIONS

def get_orientation_degrees(sense):             # angle of each axis in degrees
  ori = sense.get_orientation_degrees()
  roll  = int(ori['roll'])      # no decimals (int)
  pitch = int(ori['pitch'])     # no decimals (int)
  return roll, pitch

def get_accelerometer_geforce(sense):           # acceleration intensity (gravitational pull) on each axis measured in G
    acc = sense.get_accelerometer_raw()
    ax_g = round(acc['x'], DECIMALS)
    ay_g = round(acc['y'], DECIMALS)
    az_g = round(acc['z'], DECIMALS)
    return ax_g, ay_g, az_g
    
#######[CONNECTORPINS]########
#
# (0,0)(1,0)(2,0)(3,0)(4,0)(5,0)(6,0)(7,0)                  [LAN]
# (0,1)(1,1)(2,1)(3,1)(4,1)(5,1)(6,1)(7,1)
# (0,2)(1,2)(2,2)(3,2)(4,2)(5,2)(6,2)(7,2)
# (0,3)(1,3)(2,3)(3,3)(4,3)(5,3)(6,3)(7,3)
# (0,4)(1,4)(2,4)(3,4)(4,4)(5,4)(6,4)(7,4)                  [USB]
# (0,5)(1,5)(2,5)(3,5)(4,5)(5,5)(6,5)(7,5)
# (0,6)(1,6)(2,6)(3,6)(4,6)(5,6)(6,6)(7,6)
# (0,7)(1,7)(2,7)(3,7)(4,7)(5,7)(6,7)(7,7)
#                                               [JOYSTICK]  [USB]
# [USB-C]       [HDMI-0]    [HDMI-1]

# ROLL
def set_roll_level(roll):
  if (roll > 30) and (roll < 180): # over 30
    sense.set_pixel(3, 0, R)
    sense.set_pixel(4, 0, R)
  elif (roll > 15) and (roll <= 30): # 15 til 30
    sense.set_pixel(3, 0, R)
    sense.set_pixel(4, 0, R)
    sense.set_pixel(3, 1, R)
    sense.set_pixel(4, 1, R)
  elif (roll > 5) and (roll <= 15): # 5 til 15
    sense.set_pixel(3, 1, Y)
    sense.set_pixel(4, 1, Y)
    sense.set_pixel(3, 2, Y)
    sense.set_pixel(4, 2, Y)
  elif (roll > 2) and (roll <= 5): # 2 til 5
    sense.set_pixel(3, 2, G)
    sense.set_pixel(4, 2, G)
    sense.set_pixel(3, 3, G)
    sense.set_pixel(4, 3, G)
  ###  
  elif (roll <= 2):             # 0 til 2
    sense.set_pixel(3, 3, G)
    sense.set_pixel(4, 3, G)
    sense.set_pixel(3, 4, G)
    sense.set_pixel(4, 4, G)
  ### CENTER ###
  elif (roll >= 358):           # 0 til 2
    sense.set_pixel(3, 3, G)
    sense.set_pixel(4, 3, G)
    sense.set_pixel(3, 4, G)
    sense.set_pixel(4, 4, G)
  ###
  elif (roll < 358) and (roll >= 355): # 2 til 5
    sense.set_pixel(3, 4, G)
    sense.set_pixel(4, 4, G)
    sense.set_pixel(3, 5, G)
    sense.set_pixel(4, 5, G)
  elif (roll < 355) and (roll >= 345): # 5 til 15
    sense.set_pixel(3, 5, Y)
    sense.set_pixel(4, 5, Y)
    sense.set_pixel(3, 6, Y)
    sense.set_pixel(4, 6, Y)
  elif (roll < 345) and (roll >= 330): # 15 til 30
    sense.set_pixel(3, 6, R)
    sense.set_pixel(4, 6, R)
    sense.set_pixel(3, 7, R)
    sense.set_pixel(4, 7, R)
  elif (roll < 330) and (roll > 180):
    sense.set_pixel(3, 7, R)
    sense.set_pixel(4, 7, R)
  

# PITCH
def set_pitch_level(pitch):
  if (pitch > 30) and (pitch < 180): # over 30
    sense.set_pixel(7, 3, R)
    sense.set_pixel(7, 4, R)
  elif (pitch > 15) and (pitch <= 30): # 15 til 30
    sense.set_pixel(7, 3, R)
    sense.set_pixel(7, 4, R)
    sense.set_pixel(6, 3, R)
    sense.set_pixel(6, 4, R)
  elif (pitch > 5) and (pitch <= 15): # 5 til 15
    sense.set_pixel(6, 3, Y)
    sense.set_pixel(6, 4, Y)
    sense.set_pixel(5, 3, Y)
    sense.set_pixel(5, 4, Y)
  elif (pitch > 2) and (pitch <= 5): # 2 til 5
    sense.set_pixel(5, 3, G)
    sense.set_pixel(5, 4, G)
    sense.set_pixel(4, 3, G)
    sense.set_pixel(4, 4, G)
  ###  
  elif (pitch <= 2):             # 0 til 2
    sense.set_pixel(4, 3, G)
    sense.set_pixel(4, 4, G)
    sense.set_pixel(3, 3, G)
    sense.set_pixel(3, 4, G)
  ### CENTER ###
  elif (pitch >= 358):           # 0 til 2
    sense.set_pixel(4, 3, G)
    sense.set_pixel(4, 4, G)
    sense.set_pixel(3, 3, G)
    sense.set_pixel(3, 4, G)
  ###
  elif (pitch < 358) and (pitch >= 355): # 2 til 5
    sense.set_pixel(3, 3, G)
    sense.set_pixel(3, 4, G)
    sense.set_pixel(2, 3, G)
    sense.set_pixel(2, 4, G)
  elif (pitch < 355) and (pitch >= 345): # 5 til 15
    sense.set_pixel(2, 3, Y)
    sense.set_pixel(2, 4, Y)
    sense.set_pixel(1, 3, Y)
    sense.set_pixel(1, 4, Y)
  elif (pitch < 345) and (pitch >= 330): # 15 til 30
    sense.set_pixel(1, 3, R)
    sense.set_pixel(1, 4, R)
    sense.set_pixel(0, 3, R)
    sense.set_pixel(0, 4, R)
  elif (pitch < 330) and (pitch > 180):
    sense.set_pixel(0, 3, R)
    sense.set_pixel(0, 4, R)


# run MAIN
if __name__ == "__main__":
    main()
