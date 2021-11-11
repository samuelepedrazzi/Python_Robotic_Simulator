# Assignment #1 for Research Track 1
## Python Robotics Simulator
## Introduction and aim of the project
The main target for the requested commission was to manage the movement and other actions of a robot into a simulation software environment.
The demanded tasks were:
* `The movement of the robot`: it should drive in the counter-clockwise direction around a circuit, which depends on the "Arena" that was already given; 
* `Keeping the robot away from the walls`: it must avoid touching the golden boxes, which delimit the perimeter of the circuit;
* `The management of silver boxes`: when the robot is close to a silver box, it should grab it and move it behind itself.

## Environmental elements
For a visible recognization of the robot in the simulator it's used an holonomic robot icon: 

![alt text](https://github.com/samuelepedrazzi/Research-Track-1/blob/main/images/robot.png)

Silver tokens are the ones that should be grabbed for the aim of the project:

![alt text](https://github.com/samuelepedrazzi/Research-Track-1/blob/main/images/token_silver.png)

Golden tokens are those that should be avoided and they are represented below:

![alt text](https://github.com/samuelepedrazzi/Research-Track-1/blob/main/images/token.png)

The dedicated circuit along which the robot has to move:

![alt text](https://github.com/samuelepedrazzi/Research-Track-1/blob/main/images/arena.jpeg)


### Installing ###

The requirements for the assignment are: a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

By using `pip`, it should be installed the pygame dependence by the command: 
```bash
$ pip install hg+https://bitbucket.org/pygame/pygame
``` 
Otherwise it can be used the operating system's package manager. `PyYAML` and `PyPyBox2D` can be clearly obtained by `pip install PyYAML` and `pip install PyPyBox2D` or it's just fine from `pip` or `easy_install`.

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

### Running ###

In order to run the assignment in the simulator, simply use `run.py`, passing it the file name, in the specific case, `assignment1.py`, as seen below:

```bash
$ python run.py assignment1.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the motors, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

The previous code is used to implement the function to make the holonomic robot turn, `turn(speed, seconds)`; contrariwise both the motors are set to a certain `speed` to make the robot drive in a straight direction.

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

In order to use this capacity of the robot, an implemented function deals with the grabbing management: `grab_silver_token(dist, rot_y)`.

Formerly it checks if the robot is at a distance where it can pick up the token (the thrashold is set to 0.4), then verifies if the method R.grab returns, so that it has grabbed the token and it manages to turn around and release the token, otherwise the robot approaches to it.

```python
if R.grab(): 
           print("Gotcha!")
           turn(vTurning, 2)
           R.release()
           drive(-20,1)
           turn(-vTurning, 2)
else:
           print("I'm not close enough.")
           drive(10,0.5)
```

Another condition to be verified is that the robot has to be aligned to the token which it wants to reach.

```python
    elif -a_th<= rot_y <= a_th: 
        print("Ah, that'll do.")
        drive(50, 0.1)
```

Here the robot trajectory corresponds to the one of the detected silver token, at the expense of an angle of 4 degrees. 
Otherwise it should adjust the corner of vision in front of itself to the token. Below it can be seen the control of the correct trajectory: 

```python
    elif rot_y < -a_th: 
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)
```
   
### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has many attributes, such as:

* `info`: a `MarkerInfo` object describing the marker itself. The program uses:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `rot_y`: an alias for `centre.rot_y`

The most used ones for the assignment (in my case) are "marker_type" for the research of tokens and "dist" and "rot_y" to manage the correct movement of the robot and the avoidance of collisions.

Important to notice that the robot with the method R.see() has a reliable detection of 360°, so it can be useful to make the robot have a range of vision into a cone of 60 degrees in front of it.

Two function are made to identify silver or golden tokens, here following the code:

```python
def find_silver_token():
   
    dist=1.5
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -30<token.rot_y<30:
      
            if check_golden_between_silver(token.dist, token.rot_y) == False:   
                dist=token.dist
                rot_y=token.rot_y
    if dist==1.5:
        return -1, -1
    else:
        return dist, rot_y
```

After the initialization of a variable dist which has to be compared with the actual distance of the robot from a silver token, if the distance is under a certain threshold (it has put to 1.5 after some attempts) the token of the marker_type silver is relevated.
Important to underline the function check_golden_token(token.dist, token.rot_y), which is used in find_silver_token() to avoid this situation: if a silver token is detected but there is also a golden token between the robot and the silver, it should ignore it.
So check_golden_token(token.dist, token.rot_y) returns a boolean (True) if the measure of distance of the golden token is less than the silver one's. Another constraint for the comparison of the distances is that the allignment of both the tokens of different color must be equal (angle of golden one must be the same of the silver detected).

The same happened to golden tokens, so that the robot can pinpoint exactly where they are. Thanks to some checks in the "main()" function, the robot is able to keep itself away from the walls and not collide with them.

### Movement around the arena ###

The aim of the robot, as already said, is to move around the circuit clockwise, grabbing silver tokens if there are any along the path.
In this paragraph let's analize only the part regard to the movement.
The two main problems to make the robot move safely are to face up to the collision avoidance from lateral golden tokens, which represent the wall or the perimeter of the circuit, and to make it turn properly in correspondence of a wall in front of it, specifically deciding where to go in order to continue the path in the same orientation (clockwise).

When the robot is approaching to a wall but not clearly in front of it, so that golden tokens of the side can be considered lateral, in an angle up to 150° and -150°, the main() function manage to adjust the trajectory.

The global variable g_border_th is set to 0.9 and it's compared with the real time distance of the robot, if the check passes it means that a golden token is near to the robot.

To solve the problem of choosing the right way to turn in proximity of an angle of the arena or a wall directly posed in front of the robot, comes to our aid the function `turn_decision()` which determines what is the best way to go to continue the path, depending on the distance on the left and on the right of the robot. It returns "-1" if the distance of the golden token in a range of 40 degrees on his right is less than the distance on its left, otherwise it chooses the other way around and returns "1", as can be seen below:

```python
def turn_decision():
    
    g_sx = 100
    g_dx = 100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_GOLD:
            
            if 70<token.rot_y<110 and token.dist < g_dx:
                g_dx = token.dist
            elif -110<token.rot_y<-70 and token.dist < g_sx:
                g_sx = token.dist
    if (g_sx == g_dx):
        return -1
    else:
        if g_sx < g_dx:
            return 1 
        else: return -1 
```

At this point, is simply necessary to select the exact velocity to turn 90° left or right based on the return of the function turn_decision().

Flowchart
--------------

<p align="center">
    
<img src="https://github.com/samuelepedrazzi/Research-Track-1/blob/main/images/Assignment1_Diagram.png" width="600" height="600">
    
</p>

Simulation video
-----------------

![alt text](https://github.com/samuelepedrazzi/Research-Track-1/blob/main/images/SimulationVideo.gif)

## Conclusions ##

I found a lot of interest in the designated project even though I have encountered some difficulties such as:

* There are so many different ways to approach to the dedicate assignment and it is not easy to choose first which will be the most efficient.
* The choice of velocity in respect of the motors is not taken for granted because the run of the code isn't deterministic so every time the robot can do something different.



### Possible improvements ###


