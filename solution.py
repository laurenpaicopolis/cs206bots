import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
length = width = height = 1
x = 0
y = 0.5
z = 1

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = (numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2) - 1
        self.weights = self.weights * c.numMotorNeurons - 1

    def start_simulate(self, type):
        self.create_world()
        self.create_body()
        self.create_brain()
        os.system("python3 simulate.py " + type + " " + str(self.myID) + " &")

    def wait_for_simulation_to_end(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        with open("fitness" + str(self.myID) + ".txt", "r") as f:
            fitnessValue = f.read()
        self.fitness = float(fitnessValue)
        os.system("rm fitness" + str(self.myID) + ".txt")

    def create_world(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[4, 4, 0], size=[length, width, height])
        pyrosim.End()

    def create_body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 1, 2], size=[0.25, 0.5, 1])  # root link

        # SHOULDERS
        pyrosim.Send_Cube(name="BackLeg", pos=[0, 0.1, 0], size=[0.2, 0.2, 0.2])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, -0.1, 0], size=[0.2,0.2,0.2])

        # UPPER LEGS
        pyrosim.Send_Cube(name="LeftLeg", pos=[0, 0, -0.25], size=[0.2, 0.2, 0.5])
        pyrosim.Send_Cube(name="RightLeg", pos=[0, 0, -0.25], size=[0.2, 0.2, 0.5])

        # LOWER LEGS
        pyrosim.Send_Cube(name="LeftLowerLeg",pos=[0, 0, -0.2], size=[0.2, 0.2, 0.4])
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.2], size=[0.2, 0.2, 0.4])

        # ARMS
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.375], size=[0.2, 0.25, 0.75])
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.375], size=[0.2, 0.25, 0.75])

        # FEET
        pyrosim.Send_Cube(name="FootOne", pos=[0.05, 0, -0.05], size=[0.3, 0.2, 0.1])
        pyrosim.Send_Cube(name="FootTwo", pos=[0.05, 0, -0.05], size=[0.3, 0.2, 0.1])

        # SHOULDER JOINTS
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute",
                           position=[0, 1.25, 2.2], jointAxis = "0 1 0")
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute",
                           position=[0, 0.75, 2.2], jointAxis = "0 1 0")

        # UPPER LEG JOINTS
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                          position=[0, 0.875, 1.5], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                          position=[0, 1.125, 1.5], jointAxis="0 1 0")

        # ARM JOINTS
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute",
                          position=[0, -0.2, -0.1], jointAxis="1 0 0")
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute",
                          position=[0, 0.2, -0.1], jointAxis="1 0 0")

        # LOWER LEG JOINTS
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                           position=[0,0,-0.5], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                           position=[0, 0, -0.5], jointAxis="0 1 0")

        # FEET JOINTS
        pyrosim.Send_Joint(name="LeftLowerLeg_FootOne", parent="LeftLowerLeg", child="FootOne", type="revolute",
                          position=[0, 0, -0.4], jointAxis="0 1 0")
        pyrosim.Send_Joint(name="RightLowerLeg_FootTwo", parent="RightLowerLeg", child="FootTwo", type="revolute",
                          position=[0, 0, -0.4], jointAxis="0 1 0")

        pyrosim.End()

    def create_brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="RightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=9, linkName="FootOne")
        pyrosim.Send_Sensor_Neuron(name=10, linkName="FootTwo")
        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=13, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=17, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=18, jointName="RightLeg_RightLowerLeg")
        pyrosim.Send_Motor_Neuron(name=19, jointName="LeftLowerLeg_FootOne")
        pyrosim.Send_Motor_Neuron(name=20, jointName="RightLowerLeg_FootTwo")


        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn+c.numSensorNeurons,
                                     weight= self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(-1, c.numMotorNeurons)
        randomColumn = random.randint(-1, 1)
        self.weights[randomRow, randomColumn] = random.random() * c.numMotorNeurons - 1

    def setID(self, nextAvailableID):
        self.myID = nextAvailableID
