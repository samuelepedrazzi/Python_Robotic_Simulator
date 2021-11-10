from __future__ import print_function

import time
from sr.robot import *



a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

g_th = 1.1
"""float: Threshold for golden markers"""

g_border_th = 0.9
""" float: Threshold for the control of the borders (golden markers)"""

vTurning = 36
"""int: Velocity for turning the robot during the grab movement"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver marker"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token in front of the robot

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=1.5
    for token in R.see():

        # research for a silver token in a range of 60 degrees in front of the robot
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -30<token.rot_y<30:
            # check if a silver token is detected behind a golden one, if it is, ignore it, otherwise update the silver token parameters
            if check_golden_between_silver(token.dist, token.rot_y) == False:   
                dist=token.dist
                rot_y=token.rot_y
    if dist==1.5:
        return -1, -1
    else:
        return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token in front of the robot

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():

        # research for a golden token in a range of 60 degrees in front of the robot
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -30<token.rot_y<30:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y

def check_golden_between_silver(dist, rot_y):
    """
    Function to check if there is a golden token between a silver detected from the robot

    Args:
        dist (float): distance of the closest silver token
        rot_y (float): angle between the robot and the token

    Returns:
        True: if a golden token is detected between the robot and a silver token
        False: the silver token is closer to the robot than the golden token
    """
    distG=100
    for token in R.see():

        # checks if a golden token in the same angle, in module, is detected with a distance less than a silver detected 
        if token.dist < distG and token.info.marker_type is MARKER_TOKEN_GOLD and abs(token.rot_y) < abs(rot_y): 
            distG = token.dist
   	if distG == 100 or dist < distG: return False
    else: return True


def turn_decision():
    """
    Function to decide where to turn
    Returns:
	    1: if the closest golden token is on the right, so the robot should turn on its left (counter clockwise),
        -1: if the closest golden token is on the left, so the robot should turn on its right (clockwise).
    """
    g_sx = 100
    g_dx = 100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_GOLD:
            # check the distance between the robot and a golden token on the left and on the right,
            # in a range of 40 degrees and choose the way with the furthest golden token
            if 70<token.rot_y<110 and token.dist < g_dx:
                g_dx = token.dist
            elif -110<token.rot_y<-70 and token.dist < g_sx:
                g_sx = token.dist
    if (g_sx == g_dx):
        return -1
    else:
        if g_sx < g_dx:
        # the robot turns right in proximity of a wall on the left
            return 1 
        # otherwise the robot turns left
        else: return -1 

def grab_silver_token(dist, rot_y):
    """
    Function to make the robot grab the closest silver token
    
    Args:
        dist (float): distance of the closest silver token
        rot_y (float): angle between the robot and the token
    """

    # if the robot is close to the token, it tries to grab it
    if dist <d_th: 
        print("Found it!")

        # if the robot grab the token, we make the robot turn around (clockwise), we release the token, and we go back to the initial position
        if R.grab(): 
            print("Gotcha!")
            turn(vTurning, 2)
            R.release()
            drive(-20,1)
            turn(-vTurning, 2)
            print("Silver token just grabbed")

        # if the robot can't grab it, it has to move nearer to it
        else:
            print("I'm not close enough.")

    # if the robot is well aligned with the token, we go forward in order to reach it
    elif -a_th<= rot_y <= a_th: 
        print("Ah, that'll do.")
        drive(50, 0.1)

    # if the robot is not well aligned with the token, it manage to adjust the trajectory
    elif rot_y < -a_th: 
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)


def main():

    # Infinite loop to make the routine go on until the program is closed by the user
    while 1:
        # Collision avoidance: if the robot detect a golden token approaching to its right it deviates
        # to its left, otherwise the robot decide to deviate to its right.
        dist, rot_y = find_golden_token()

        # the global variable g_border_th is used as a thrashold to checks the distance of lateral walls
        if dist < g_border_th:
            if 0<rot_y<150:
                print("I'm close to the wall, left a bit...")
                turn(-10,0.5)
            elif -150<rot_y<0:
                print("I'm close to the wall, right a bit...")
                turn(10,0.5)
        
        #  when the robot detects, in a range of 30 degrees in front of it, the presence of a wall,
        # it turns, the decision on where is based on the the distance from golden tokens on its left and right.
        if dist < g_th and -15<rot_y<15:
            print("There's a wall in front of me, I have to turn...")
            if turn_decision() == 1: 
                turn(17,2)
                drive(40,1)
            else: 
                turn(-17,2)
                drive(40,1)

        # if the way of the robot is clear and it is moving forward in the circuit, let's start the research of a silver token:
        else: 
            dist, rot_y = find_silver_token()

            # if the robot detects a silver token, it manages to reach it and grab it, otherwise it continues the path
            if dist != -1:
                grab_silver_token(dist, rot_y)
            else:
                drive(70,0.1)
            

main()

