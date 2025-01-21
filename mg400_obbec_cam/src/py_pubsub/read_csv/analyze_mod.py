import sys
import os


import rclpy
from rclpy.node import Node
import time


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import math


import package_a as PA



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



img_path = '~/ros2_ws/src/py_pubsub/ex_find_cg/color_image.png'
img_path = '~/ros2_ws/src/py_pubsub/ex_find_cg/tg09.png'
img_path = os.path.expanduser(img_path)  # Expand the path

#raw data load path
table_path = '/home/wedo2/ros2_ws/src/py_pubsub/custom_box_detection/custom_box/csv/object_detection_log.csv'
table_path_r = os.path.expanduser(table_path)  # Expand the path

# Global variables for saving location and saving cycle
save_location = os.path.expanduser('~/ros2_ws/src/py_pubsub/read_csv/modify_tables')
csv_file_path = os.path.join(save_location, 'real_world_position.csv')




#Load dataset
df = pd.read_csv(table_path_r)

# 1.1. Exploring the DataFrame

df.info()
df.shape

print("explain mean of each columns\n")
print("Object Number mean assign number for each box")
print("CG_x mean coordinate of x pixel (cx)")
print("CG_y mean coordinate of y pixel (cy)")
print("Width mean shape of picture in width pixel")
print("Height mean shape of picture in height pixel")
print("Depth mean depth from camera lens to object in mm unit")


# Get unique values from every column
unique_values_per_column = {}
for column in df.columns:
    unique_values_per_column[column] = df[column].unique()

# Print unique values from every column
for column, unique_values in unique_values_per_column.items():
    print(f"Unique values in column '{column}': {unique_values}")


df.head()

df.tail()

# 1.2 Preprocess (Data Wragling)

#1.2 Preprocess (Data Wragling)
#check table have null data yes or no
df.isnull()

df.isna().sum()

# Exclude non-numeric columns before applying fillna mean
numeric_cols = df.select_dtypes(include=np.number).columns
df_filled_mean = df[numeric_cols].apply(lambda col: col.fillna(col.mean()), axis=0)
# Concatenate the filled numeric columns with the original non-numeric columns
df_filled_mean = pd.concat([df_filled_mean, df.drop(numeric_cols, axis=1)], axis=1)

clean_df_1 = df_filled_mean

clean_df_1.isna().sum()

#2.check duplicate data
clean_df_1.duplicated()

clean_df_1.duplicated().sum()
    
#remove duplicate data
clean_df_2=clean_df_1.drop_duplicates()
clean_df_2.shape


# 2.Exploratory Data Analysis


plt.figure(figsize=(10, 6))
sns.histplot(clean_df_1['CG_x (px)'], bins=20, kde=True, color='skyblue')
plt.title('Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# PA.get_pose()
m=PA.get_pose()
time.sleep(2)
# print(m)
print("fffff")
# Call the function and check the response type

# Check if the result is not None (meaning the service call was successful)
if m:
    # Define constants x axis
    x_cap_robot = m.pose1
    print(f"x_cap_robot = {x_cap_robot}")  # This will print "a = <pose1 value>"

    # Similarly, you can access other pose values
    y_cap_robot = m.pose2
    print(f"y_cap_robot = {y_cap_robot}")

    z_cap_robot = m.pose3
    print(f"z_cap_robot = {z_cap_robot}")
else:
    print("Failed to get pose data from the robot.")







# 3.find mean of each object number
# Group the data by 'Object Number' and calculate the mean for each group
mean_values = round(df.groupby('Object Number').mean(),3)



# Calculate the mean of the 'Depth (mm)' column
average_depth = mean_values['Depth (mm)'].mean()

# Add the new 'average_depth(mm)' column to mean_values DataFrame
mean_values['average_depth (mm)'] = round(average_depth,3)

# calculate pixel_x in mm unit
tan_33_163 = math.tan(math.radians(33.163))
px = 640
limit_x = 2*(average_depth*(tan_33_163))
pixel_x = (limit_x)/px
print(pixel_x)

# Add the new 'pixel_x (mm/px)' column to mean_values DataFrame
mean_values['pixel_x (mm/px)'] = round(pixel_x,3)


# calculate pixel_y in mm unit
tan_26_166 = math.tan(math.radians(26.166))
py = 480
limit_y = 2*(average_depth*(tan_26_166))
pixel_y = (limit_y)/py
print(pixel_y)

# Add the new 'pixel_y (mm/px)' column to mean_values DataFrame
mean_values['pixel_y (mm/px)'] = round(pixel_y,3)


# Define constants x axis
x_cap_robot = x_cap_robot * 1000  # Convert to mm
x_dist_cam = limit_y /2
x_ofset_tool = 52

# Initialize an empty list to store the x_robot_zero values
new_x_robot = []

# Define constants y axis
y_cap_robot = y_cap_robot * 1000  # Convert to mm
y_dist_cam = limit_x /2
y_ofset_tool = 9

# Initialize an empty list to store the y_robot_zero values
new_y_robot = []

# Define constants z axis
z_cap_robot = z_cap_robot  * 1000  # Convert to mm
z_dist_cam = average_depth
z_ofset_tool = 45.8

# Initialize an empty list to store the z_robot_zero values
new_z_robot = []


# Loop through each Object Number in the mean_values DataFrame
for object_number in mean_values.index:
    # Retrieve CG_y (px) for the current Object Number
    cg_y = mean_values.loc[object_number, 'CG_y (px)']
    cg_x = mean_values.loc[object_number, 'CG_x (px)']
    average_depth = mean_values.loc[object_number, 'average_depth (mm)']


    # Calculate x_robot_zero
    x_robot_zero = round(((cg_y * pixel_y) + (x_cap_robot - (x_dist_cam - x_ofset_tool))) / 1000, 3)

    # Calculate y_robot_zero
    y_robot_zero = round(((cg_x * pixel_x) + (y_cap_robot - (y_dist_cam - y_ofset_tool))) / 1000, 3)

    # Calculate y_robot_zero
    z_robot_zero = round(( (z_cap_robot - (z_dist_cam - z_ofset_tool))) / 1000, 3)

    # Append the result to the new_x_robot list
    new_x_robot.append(x_robot_zero)

    # Append the result to the new_y_robot list
    new_y_robot.append(y_robot_zero)

    # Append the result to the new_z_robot list
    new_z_robot.append(z_robot_zero)

    # Print the calculated x_robot_zero value for each object
    print(f"Object Number {object_number}: x_robot_zero = {x_robot_zero}")

    # Print the calculated y_robot_zero value for each object
    print(f"Object Number {object_number}: y_robot_zero = {y_robot_zero}")


    # Print the calculated y_robot_zero value for each object
    print(f"Object Number {object_number}: z_robot_zero = {z_robot_zero}")


# Add the new_x_robot list as a new column in the mean_values DataFrame
mean_values['new_x_robot (m)'] = new_x_robot

# Add the new_x_robot list as a new column in the mean_values DataFrame
mean_values['new_y_robot (m)'] = new_y_robot

# Add the new_x_robot list as a new column in the mean_values DataFrame
mean_values['new_z_robot (m)'] = new_z_robot


# Save the updated DataFrame to CSV
mean_values.to_csv(csv_file_path )

# Display the mean values
print(mean_values)

print(f"Mean values with average_depth saved to {csv_file_path}")


#raw data load path
table_path_new = '~/ros2_ws/src/py_pubsub/read_csv/modify_tables/real_world_position.csv'
table_path_new_r = os.path.expanduser(table_path_new)  # Expand the path

#Load dataset
df_new = pd.read_csv(table_path_new_r)

# print(df_new.columns)



# Extract unique Object Numbers from the DataFrame
available_object_numbers = df_new['Object Number'].unique().tolist()
print("Available Object Numbers:")
print(available_object_numbers)



# # Request input from the user for Object Number
try:
    object_number_input = int(input("Enter the Object Number to display: "))

    # Check if the entered Object Number exists in the DataFrame
    if object_number_input in available_object_numbers:
        # Print the corresponding row from mean_values
        print(f"Details for Object Number {object_number_input}:")

        # Retrieve values based on Object Number input
        x_robot_value = df_new[df_new['Object Number'] == object_number_input]['new_x_robot (m)'].values[0]
        y_robot_value = df_new[df_new['Object Number'] == object_number_input]['new_y_robot (m)'].values[0]
        z_robot_value = df_new[df_new['Object Number'] == object_number_input]['new_z_robot (m)'].values[0]

        # Print the values in the desired format
        print(f"new_x_robot (m) = {x_robot_value}")
        print(f"new_y_robot (m) = {y_robot_value}")
        print(f"new_z_robot (m) = {z_robot_value}")

        # Example usage of PA functions if needed

        PA.speed_factor(100)


        PA.Mov_L(0.226851666,0.001727872,0.10525501300000001,55.435604)


        PA.Mov_L(x_robot_value, y_robot_value, z_robot_value, 55.435604)

        PA.Mov_L(0.25569685600000003 ,-0.16821522100000003 ,0.042535084 ,56.06)
        
        PA.Mov_L(0.226851666,0.001727872,0.10525501300000001,55.435604)
    else:
        print(f"Object Number {object_number_input} not found in the data.")
except ValueError:
    print("Invalid input. Please enter a valid Object Number.")




            # PA.speed_factor(40)
        # PA.Mov_L(0.226851666,0.001727872,0.10525501300000001,55.435604)


