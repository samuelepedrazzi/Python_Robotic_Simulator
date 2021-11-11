# Assignment #1 for Research Track 1
## Python Robotics Simulator
## Introduction
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

By using `pip`, it should be installed the pygame dependence by the command: ```bash
$ pip install hg+https://bitbucket.org/pygame/pygame``` Otherwise it can be used the operating system's package manager. `PyYAML` and `PyPyBox2D` can be clearly obtained by `pip install PyYAML` and `pip install PyPyBox2D` or it's just fine from `pip` or `easy_install`.

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

Running
-----------------------------

In order to run the assignment in the simulator, simply use `run.py`, passing it the file name, in the specific case, `assignment1.py`, as seen below:

```bash
$ python run.py assignment1.py
```

