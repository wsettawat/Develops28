import sys
import os


import rclpy
from rclpy.node import Node
import time
import open3d as o3d

print(o3d.__version__)
#print(sys.path)

# ----- Add from another folder level ------
# path_file = sys.dir
folderFile, filename = os.path.split(os.path.realpath(__file__))
#print("/////")
#print(folderFile)
#print("/////")
#print(filename)

# Get the parent directory (removing the last part of the path)
parent_directory = os.path.dirname(folderFile)
#print(parent_directory)


# Check if the last part is 'src' and remove it
if folderFile.endswith('src'):

    # Get the parent directory (removing the last part of the path)
    folderFile = os.path.dirname(folderFile)
    #print("/////")
    #print(folderFile)

folder_lib = os.path.join(folderFile, 'Lib')
print(folder_lib)
#print(sys.path)
if not folder_lib in sys.path:
    sys.path.append(folder_lib)
    #print("/////")
    #print(folder_lib)

import package_a as PA

import numpy as np

def cxcy_to_robot(c_x, c_y):
    # x = round(c_y * 0.348 + 207.69, 2)
    # x = round((c_y * 0.348 + 207.69)/1000 ,2)     
    # y = round((c_x * 0.365 + (-127.32))/1000,2)
    ###################
    # x = round((c_y * 0.433 + 193.98-10)/1000 ,3)     
    # y = round((c_x * 0.455 + (-136.92)-24-7)/1000,3)

    x = round((c_y * 0.354 + 212.9-5)/1000 ,3)     
    y = round((c_x * 0.359 + (-109.52-13))/1000,3)


    
    # Create a tuple for robot coordinates
    robot_coor = (x, y)
    print(robot_coor)

    # Return the coordinates
    return robot_coor
# Now call PA.Mov_L() with P2 unpacked
def PA_Mov_L(x, y, z, w):
    # Simulating the PA.Mov_L function
    print(f"PA.Mov_L({x}, {y}, {z}, {w})")
# Define c_x and c_y

def analyze_modify():
    print("read_table")


def main(args=None):
    goals = [
        (0.326, -0.233, 0.035,34.999),  # Example parameters for the first command
        (0.206, 0.301, 0.039,100.388),  # Example parameters for the second command
        # Add more goals as needed
    ]

    PA.get_pose()
    PA.clear_error()
    PA.enable_robot()
    PA.speed_factor(50)
    #Box
    PA.Mov_L(0.226851666,0.001727872,0.10525501300000001,55.435604)

    PA.Mov_L(0.25569685600000003 ,-0.16821522100000003 ,0.042535084 ,56.06)
    PA.Mov_L(0.36869269200000004,-0.05009864000000001,-0.145048965,56.06)
    PA.Mov_L(0.316094856,-0.008879292,0.014018547999999999,56.06)
    PA.Mov_L(0.258293844,0.063134724,-0.14552252200000002,56.06)
    PA.Mov_L(0.091364735,0.275780752,0.031665892,56.06)
 
    PA.disable_robot()
#######################################
    #     # Define c_x and c_y      Marker ID: 3,  (515.0, 221.0, 0.000)    10 441.0, 287.0     17  (358.0, 371.0, 0.000)    24 287.0, 442.0    26,  (209.0, 138.0, 0.000) 
    # c_x, c_y = (209.0, 138.0)

    # # Calculate the robot coordinates
    # P1 = cxcy_to_robot(c_x, c_y)

    # # Add 431.1 and 143.56 to P1 and create P2
    # P2 = P1 + (-0.145,56.06)
    # PA.get_pose()
    # print(*P2)
    # # #PA.emergency_stop()
    # PA.clear_error()
    # PA.enable_robot()
    # PA.speed_factor(40)
    # # PA.Mov_L(P2[0],P2[1],P2[2],P2[3])

    
        
    # #camera coor  for box
    # GetPose_Response(error_id=0, pose1=0.226851045, pose2=0.001743107, pose3=0.10525537900000001, pose4=0.055439178, pose5=0.0, pose6=0.0)
    # PA.Mov_L(0.257 ,-0.047 ,-0.145 ,56.06)


    # #camera coor  for qr tag
    # # PA.Mov_L(0.2459,-0.00352,-0.01783,56.06)

    # time.sleep(1)
    # PA.disable_robot()
###############################33

     #home position new 7
    # PA.Mov_L(0.245,-0.005602,0.036995,38.15)
    # time.sleep(1)


    #home position
    # PA.Mov_L(0.245,-0.005602,0.04995,38.15)



    #PA.emergency_stop()
    #PA.clear_error()
    #PA.enable_robot()
    # PA.do(1,1)
    # time.sleep(1)
    # PA.do(1,0)
    # time.sleep(1)
    # PA.do(2,1)
    # time.sleep(1)
    # PA.do(2,0)
    # time.sleep(1)
    #PA.speed_factor(40)
    #time.sleep(1)
    #PA.Mov_L(0.34, 0.0, 0.0,0)
    #time.sleep(2)
    # PA.Mov_J(-0.1, 0.0, 0.0,45.028)
    # time.sleep(2)
    #PA.Mov_L(0.248, -0.00186, 0.006075,37.1819)

    #home position
    #PA.Mov_L(0.245,-0.005602,0.04995,38.15)


    # #qr01 position  ok
    # PA.Mov_L(0.3549,0.04008,-0.1438,45.919)

    # #home position
    # PA.Mov_L(0.245,-0.005602,0.04995,38.15)


    # #qr02 position ok
    # PA.Mov_L(0.35504,-0.02944,-0.14413,34.711)

    # #home position
    # PA.Mov_L(0.245,-0.005602,0.04995,38.15)


    # #qr03 position ok 
    # PA.Mov_L(0.32157,-0.03073,-0.14445,32.376)

    # #home position
    # PA.Mov_L(0.245,-0.005602,0.04995,38.15)


    # #qr04 position
    # PA.Mov_L(0.29914,0.014643,-0.14378,40.631)

    # #home position
    # PA.Mov_L(0.245,-0.005602,0.04995,38.15)


    # #qr05 position ok
    # PA.Mov_L(0.25435,-0.030984,-0.14462,39.920)

    # #home position
    # PA.Mov_L(0.245,-0.005602,0.04995,38.15)


    # #qr06 position
    # PA.Mov_L(0.24230,0.02653,-0.14574,45.740)

    # #home position
    # PA.Mov_L(0.245,-0.005602,0.04995,38.15)





    #time.sleep(2)
    #PA.Mov_L(0.206, 0.301, 0.039,100.388)
    #time.sleep(2)
    # PA.Mov_L(0.34, 0.0, 0.0,0)
    # time.sleep(2)
   # PA.disable_robot()
    #PA.tool_do_execute(1,0)
    #PA.do(1,0)
    #PA.di(2)
    #PA.enable_robot()
    #PA.disable_robot()

    # PA.speed_factor(40)

    # position_x = 0.34
    # position_y = 0.0
    # position_z = 0.0
    # orientation_x = 0.0
    # orientation_y = 0.0
    # orientation_z = 0.0
    # orientation_w = 1.0

    # PA.Mov_J(position_x, position_y, position_z, orientation_x, orientation_y, orientation_z, orientation_w)

    

if __name__ == '__main__':
     main()






