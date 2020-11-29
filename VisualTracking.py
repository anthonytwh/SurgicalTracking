""" 
Notes:
    - Run with all SIX sensors
    - Developed for absolute calibration of prototype
""" 

__author__ = "anthonytwh"
__version__ = 1.0
import serial
from visual import *
import numpy as np



""" init """
readNum = 100   # Smoothing array size
readIndex = 0

PotArray1 = np.zeros(readNum)   # Initialize arrays per sensor
PotArray2 = np.zeros(readNum)
PotArray3 = np.zeros(readNum)
PotArray4 = np.zeros(readNum)
PotArray5 = np.zeros(readNum)
PotArray6 = np.zeros(readNum)

PotTotal1 = 0.0     # Set iterative value to 0
PotTotal2 = 0.0
PotTotal3 = 0.0
PotTotal4 = 0.0
PotTotal5 = 0.0
PotTotal6 = 0.0



""" Calculations """
def voltAngle(total1, total2, total3, total4, total5, total6):
    """ 
    Convert Voltage to Angle

    """
    global readNum

    # Calibration adjustment factors
    potCal1 = 4.33105468 #4.189410651
    potCal2 = 2.88555548
    potCal3 = 3.05908 # Pre deadband fix: 4.512  #4.57637209 #4.60449
    potCal4 = 0.25008139
    potCal5 = 2.630859 #Pre deadband fix: #2.6712 #2.63183593
    potCal6 = 0.23141841


    volts1 = round(potCal1 - ((np.sum(total1) / readNum) * (5 / 1024.0)), 5)
    angle1 = round((volts1 / 4.625) * 2 * np.pi, 5) 

    volts2 = round(((np.sum(total2) / readNum) * (5 / 1024.0)) - potCal2, 5)
    angle2 = round((volts2 / 4.632) * 2 * np.pi, 5)

    volts3 = round(potCal3 - ((np.sum(total3) / readNum) * (5 / 1024.0)), 5)
    angle3 = round((volts3 / 4.607) * 2 * np.pi, 5)

    volts4 = round(potCal4 - ((np.sum(total4) / readNum) * (5 / 1024.0)), 5)
    angle4 = round((volts4 / 4.612) * 2 * np.pi, 5)

    volts5 = round(potCal5 - ((np.sum(total5) / readNum) * (5 / 1024.0)), 5)
    angle5 = round((volts5 / 4.611) * 2 * np.pi, 5) 

    volts6 = round(potCal6 - ((np.sum(total6) / readNum) * (5 / 1024.0)), 5)
    angle6 = round((volts6 / 4.600) * 2 * np.pi, 5)

    return angle1, angle2, angle3, angle4, angle5, angle6


def FinalPosition(angle1, angle2, angle3, angle4, angle5, angle6):
    """ 
    Position Calculation

        DH Method Parameters:
            d = distance (xi+1, xi) along zi
            a = distance (zi, zi+1) along xi
            b = alpha = angle (zi, zi+1) about xi
    """
    d1 = 26
    d2 = 0
    d3 = 0
    d4 = 25.3 #25.2
    d5 = 0
    d6 = 20.48  + 7 - 1.45 #41.8

    a1 = 0
    a2 = 17.8
    a3 = 0
    a4 = 0
    a5 = 0 #-42
    a6 = 0

    b1 = -np.pi / 2
    b2 = 0
    b3 = -np.pi / 2
    b4 = np.pi / 2
    b5 = -np.pi / 2
    b6 = 0

    # Orientation of origin dependant on the real model vs. virtual position
    Origin = np.array([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]], dtype=np.float32)

    Joint1 = np.array([[np.cos(angle1), -np.sin(angle1)*np.cos(b1), np.sin(angle1)*np.sin(b1), a1*np.cos(angle1)],
            [np.sin(angle1), np.cos(angle1)*np.cos(b1), -np.cos(angle1)*np.sin(b1), a1*np.sin(angle1)],
            [0, np.sin(b1), np.cos(b1), d1],
            [0, 0, 0, 1]], dtype=np.float32)

    Joint2 = np.array([[np.cos(angle2), -np.sin(angle2)*np.cos(b2), np.sin(angle2)*np.sin(b2), a2*np.cos(angle2)],
            [np.sin(angle2), np.cos(angle2)*np.cos(b2), -np.cos(angle2)*np.sin(b2), a2*np.sin(angle2)],
            [0, np.sin(b2), np.cos(b2), d2],
            [0, 0, 0, 1]], dtype=np.float32)

    Joint3 = np.array([[np.cos(angle3 - np.pi/2), -np.sin(angle3 - np.pi/2)*np.cos(b3), np.sin(angle3 - np.pi/2)*np.sin(b3), a3*np.cos(angle3 - np.pi/2)],
            [np.sin(angle3 - np.pi/2), np.cos(angle3 - np.pi/2)*np.cos(b3), -np.cos(angle3 - np.pi/2)*np.sin(b3), a3*np.sin(angle3 - np.pi/2)],
            [0, np.sin(b3), np.cos(b3), d3],
            [0, 0, 0, 1]], dtype=np.float32)

    Joint4 = np.array([[np.cos(angle4), -np.sin(angle4)*np.cos(b4), np.sin(angle4)*np.sin(b4), a4*np.cos(angle4)],
            [np.sin(angle4), np.cos(angle4)*np.cos(b4), -np.cos(angle4)*np.sin(b4), a4*np.sin(angle4)],
            [0, np.sin(b4), np.cos(b4), d4],
            [0, 0, 0, 1]], dtype=np.float32)

    Joint5 = np.array([[np.cos(angle5), -np.sin(angle5)*np.cos(b5), np.sin(angle5)*np.sin(b5), a5*np.cos(angle5)],
            [np.sin(angle5), np.cos(angle5)*np.cos(b5), -np.cos(angle5)*np.sin(b5), a5*np.sin(angle5)],
            [0, np.sin(b5), np.cos(b5), d5],
            [0, 0, 0, 1]], dtype=np.float32)

    Joint6 = np.array([[np.cos(angle6), -np.sin(angle6)*np.cos(b6), np.sin(angle6)*np.sin(b6), a6*np.cos(angle6)],
            [np.sin(angle6), np.cos(angle6)*np.cos(b6), -np.cos(angle6)*np.sin(b6), a6*np.sin(angle6)],
            [0, np.sin(b6), np.cos(b6), d6],
            [0, 0, 0, 1]], dtype=np.float32)

    Tnet = Joint1.dot(Joint2).dot(Joint3).dot(Joint4).dot(Joint5).dot(Joint6).dot(Origin)

    xFin = Tnet[0,3]    # Extract P vector
    yFin = Tnet[1,3]
    zFin = Tnet[2,3]

    return xFin, yFin, zFin



""" 
Application Window & Environment

    Notes: 
        - center = Centered around Arm origin
        - range = View Range
        - fov =  Field of View
        - Shift of + 33.25 in X AXIS and + 16.75 in Y AXIS since Origin of robot base is off the center of virtual world
"""
# Window
AppWindow = display(title="Surgical Tracking")
AppWindow.center = (0 + 33.25 - 10, 0 + 16.75 - 10, 0)
AppWindow.width = 1600
AppWindow.height = 900
AppWindow.fullscreen = False
AppWindow.autoscale = False
AppWindow.range = (50,50,50)
AppWindow.fov =  0.0001

# Text 
PosText = label(text = 'Position (cm): ', pos = (35 + 33.25 - 15,23 + 16.75 - 10,0), height = 30, color = color.white, box = False)
XPos = label(text = 'X = ', pos = (38 + 33.25 - 15,18 + 16.75 - 10,0), height = 30, color = color.white, box = false)
YPos = label(text = 'Y = ', pos = (38 + 33.25 - 15,13 + 16.75 - 10,0), height = 30, color = color.white, box = false)
ZPos = label(text = 'Z = ', pos = (38 + 33.25 - 15,8 + 16.75 - 10,0), height = 30, color = color.white, box = false)
XPos.text = 'X = 0.00'
YPos.text = 'Y = 0.00'
ZPos.text = 'Z = 0.00'

# Effector
Point = sphere(material = materials.unshaded, color = (1, 0.1, 0.1), radius=0.3, pos=(0, 0, 0.5), make_trail = True, interval = 1, retain = 10)
# Tube = cylinder( color=color.orange, pos=(0, 0, 0), axis = (0, 0, 1), radius = 0.2, lendistancegth  = 20)     # Used to check FOV distortion in vPython

# Surface
Surface = box(material = materials.unshaded, color=color.gray(0.85) , length=30, width= 0.5, height=30, pos=(33.25 - 10,16.75 - 10,-0.5))

# Base
Base = box(material = materials.unshaded, color=color.gray(0.2) , length= 23.5, width= 0.5, height= 16.5, pos=(-3.5,0,-0.5))

# Borders
MidHorz = box(material = materials.unshaded, color=color.gray(0.7) , length=30, width=0.1, height=0.1, pos=(0 + 33.25 - 10,0 + 16.75 - 10,0))
TopHorz = box(material = materials.unshaded, color=color.gray(0.7) , length=30, width=0.1, height=0.1, pos=(0 + 33.25 - 10,25 + 16.75 - 20,0))
BotHorz = box(material = materials.unshaded, color=color.gray(0.7) , length=30, width=0.1, height=0.1, pos=(0 + 33.25 - 10,-25 + 16.75,0))
MidVert = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height=30, pos=(0 + 33.25 - 10,0 + 16.75 - 10,0))
LeftVert = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height=30, pos=(-25 + 33.25,0 + 16.75 - 10,0))
RightVert = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height=30, pos=(25 + 33.25 - 20,0 + 16.75 - 10,0))

# Diagonal Borders
Diag1 = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height=42.4264, pos=(0 + 33.25 - 10,0 + 16.75 - 10,0), axis = (1,1,0))
Diag2 = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height=42.4264, pos=(0 + 33.25 - 10,0 + 16.75 - 10,0), axis = (1,-1,0))
Quad1Diag = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height = 21.2132, pos=(-12.5 + 33.25 - 5,12.5 + 16.75 - 15,0), axis = (1,-1,0))
Quad2Diag = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height = 21.2132, pos=(12.5 + 33.25 - 15,12.5 + 16.75 - 15,0), axis = (1,1,0))
Quad3Diag = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height = 21.2132, pos=(-12.5+ 33.25 -5,-12.5 + 16.75 -5,0), axis = (1,1,0))
Quad4Diag = box(material = materials.unshaded, color=color.gray(0.7) , length=0.1, width=0.1, height = 21.2132, pos=(12.5 + 33.25 - 15,-12.5 + 16.75 - 5,0), axis = (1,-1,0))

# Points
MidPoint = sphere(material = materials.unshaded, color = (0.1, 1, 0.45), radius=0.25, pos=(0 + 33.25 - 10, 0 + 16.75 - 10, 0))
MidLabel = label(text = '(23.25, 6.75, 3.5)', pos=(0 + 33.25 - 10 + 3, 0 + 16.75 - 10 - 2, 0), height = 15, color = color.black, box = false, xoffset = 0, line = 0, yoffset = 0, opacity = 0)
Quad1MidPoint = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(-12.5 + 33.25 - 5,12.5 + 16.75 - 15,0))
Quad2MidPoint = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(12.5 + 33.25 - 15,12.5 + 16.75 - 15,0))
Quad3MidPoint = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(-12.5 + 33.25 - 5,-12.5 + 16.75 - 5,0))
Quad4MidPoint = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(12.5 + 33.25 - 15,-12.5 + 16.75 - 5,0))
Out1Point = sphere(material = materials.unshaded, color = (0.1, 1, 0.45), radius=0.25, pos=(-25 + 33.25, 25 + 16.75 - 20, 0))
Out1Label = label(text = '(8.25, 21.75, 3.5)', pos=(-25 + 33.25 - 2, 25 + 16.75 - 20 + 1, 0), height = 15, color = color.white, box = false, xoffset = 0, line = 0, yoffset = 0, opacity = 0)
Out2Point = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(0 + 33.25 - 10, 25 + 16.75 - 20, 0))
Out3Point = sphere(material = materials.unshaded, color = (0.1, 1, 0.45), radius=0.25, pos=(25 + 33.25 - 20, 25 + 16.75 - 20, 0))
Out3Label = label(text = '(38.25, 21.75, 3.5)', pos=(25 + 33.25 - 20 + 2, 25 + 16.75 - 20 + 1, 0), height = 15, color = color.white, box = false, xoffset = 0, line = 0, yoffset = 0, opacity = 0)
Out2Point = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(-25 + 33.25, 0 + 16.75 - 10, 0))
Out2Point = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(25 + 33.25 - 20, 0 + 16.75 - 10, 0))
Out2Point = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(-25 + 33.25, -25 + 16.75, 0))
Out2Point = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(-0 + 33.25 - 10, -25 + 16.75, 0))
Out2Point = sphere(material = materials.unshaded, color=color.gray(0.95), radius=0.2, pos=(25 + 33.25 - 20, -25 + 16.75, 0))
vWorldCenter = sphere(material = materials.unshaded, color=color.orange, radius=0.2, pos=(0, 0, 0.5))
vWorldLabel = label(text = '(0, 0, 0)', pos = (-2, -1, 0.5), height = 15, color = color.white, box = false, xoffset = 0, line = 0, yoffset = 0, opacity = 0)

# Axes
xAxis = arrow(material = materials.unshaded, color = color.red, pos = (-22, 27, 0), axis = (1,0,0), length = 3)
xAxisLabel = label(text = 'X', pos = (4 - 22, 27, 0), height = 15, color = color.white, box = false, xoffset = 0, line = 0, yoffset = 0)
yAxis = arrow(material = materials.unshaded, color = color.green, pos = (- 22, 27, 0), axis = (0,1,0), length = 3)
yAxisLabel = label(text = 'Y', pos = (0 - 22, 31, 0), height = 15, color = color.white, box = false, xoffset = 0, line = 0, yoffset = 0)
zAxis = arrow(material = materials.unshaded, color = color.blue, pos = (- 22, 27, 0), axis = (0,0,1), length = 3)
zAxisLabel = label(text = 'Z', pos = (0 - 23, 26, 0), height = 15, color = color.white, box = false, xoffset = 0, line = 0, yoffset = 0)



""" Serial Read 

    Note:
        - can manually adjust settings in ../Device Manager/Ports (Windows)
"""
sensorData = serial.Serial("com4", 115200, timeout = None, xonxoff = False, dsrdtr = False)

""" Main """ 
while (1==1):

    # Read Serial Data
    UnoData = sensorData.readline()
    dataNums = UnoData.split(' , ')
    Pot1Raw = float(dataNums[0])
    Pot2Raw = float(dataNums[1])
    Pot3Raw = float(dataNums[2])
    Pot4Raw = float(dataNums[3])
    Pot5Raw = float(dataNums[4])
    Pot6Raw = float(dataNums[5])

    # Remove previous value in Array
    PotTotal1 = PotTotal1 - PotArray1
    PotTotal2 = PotTotal2 - PotArray2
    PotTotal3 = PotTotal3 - PotArray3
    PotTotal4 = PotTotal4 - PotArray4
    PotTotal5 = PotTotal5 - PotArray5
    PotTotal6 = PotTotal6 - PotArray6

    # Array Read
    PotArray1[readIndex] = Pot1Raw
    PotArray2[readIndex] = Pot2Raw
    PotArray3[readIndex] = Pot3Raw
    PotArray4[readIndex] = Pot4Raw
    PotArray5[readIndex] = Pot5Raw
    PotArray6[readIndex] = Pot6Raw

    # Replace previous value in Array
    PotTotal1 = PotTotal1 + PotArray1 
    PotTotal2 = PotTotal2 + PotArray2
    PotTotal3 = PotTotal3 + PotArray3
    PotTotal4 = PotTotal4 + PotArray4
    PotTotal5 = PotTotal5 + PotArray5
    PotTotal6 = PotTotal6 + PotArray6

    # Index Counter
    readIndex = readIndex + 1

    if readIndex == readNum:

        # Index
        readIndex = 0 

        # Calculation
        AngleConv = voltAngle(PotTotal1, PotTotal2, PotTotal3, PotTotal4, PotTotal5, PotTotal6)
        PotAng1 = AngleConv[0]
        PotAng2 = AngleConv[1]
        PotAng3 = AngleConv[2]
        PotAng4 = AngleConv[3]
        PotAng5 = AngleConv[4]
        PotAng6 = AngleConv[5]
        EFPos = FinalPosition(PotAng1, PotAng2, PotAng3, PotAng4, PotAng5, PotAng6)

        # Update Labels
        XLabel = 'X = ' + str(np.round(EFPos[1] - 2, 2))
        XPos.text = XLabel
        YLabel = 'Y = ' + str(np.round(-EFPos[0], 2))
        YPos.text = YLabel
        ZLabel = 'Z = ' + str(np.round(EFPos[2], 2))
        ZPos.text = ZLabel

        Point.pos = vector(EFPos[1] - 2, -EFPos[0], EFPos[2])
