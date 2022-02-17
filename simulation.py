from robot import ROBOT
from world import WORLD
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import time
import numpy

class SIMULATION:

    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT()

    def run(self):

        #targetAnglesFront = c.amplitude * numpy.sin(c.frequency * numpy.linspace(0, 2 * numpy.pi, 1000) + c.phaseOffset)
        #targetAnglesBack = c.amplitude * numpy.sin(c.frequency * numpy.linspace(0, 2 * numpy.pi, 1000) + c.phaseOffset)
        for current_time_step in range(c.timeSteps):
            p.stepSimulation()
            self.robot.sense(current_time_step)
            self.robot.prepare_to_act()
            self.robot.act()
            time.sleep(c.timeTics)

    def __del__(self):
        p.disconnect()