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


Installing
----------------------

The requirements for the assignment are: a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

By using `pip`, it should be installed the pygame dependence by the command: 
```bash
$ pip install hg+https://bitbucket.org/pygame/pygame
``` 
Otherwise it can be used the operating system's package manager. `PyYAML` and `PyPyBox2D` can be clearly obtained by `pip install PyYAML` and `pip install PyPyBox2D` or it's just fine from `pip` or `easy_install`.

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

Running
-----------------------------

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

Formerly it checks if the robot is at a distance where it can pick up the token (0.4), then verifies if the method R.grab returns, so that it has grabbed the token and it manages to turn around and release the token, otherwise the robot approaches to it.

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

  if the robot is well aligned with the token, we go forward in order to reach it
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
### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has many attributes, included:

* `info`: a `MarkerInfo` object describing the marker itself. The program uses:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
* `dist`: the distance from the centre of the robot to the object (in metres).
* `rot_y`: rotation about the Y axis in degrees.

