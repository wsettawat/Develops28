import re
import cv2 
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt

IMG_DIR = 'images/'

# # get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 


# Plot original image
image = cv2.imread(IMG_DIR + 'flight_log_00.png')

b,g,r = cv2.split(image)
rgb_img = cv2.merge([r,g,b])

areas = [
    (576, 777, 833, 1551),
    (1084, 780, 1449, 828),
    (156, 1664, 855, 1783),
    (1155, 1648, 1431, 1778) 
]

for (x1, y1, x2, y2) in areas:
    # Extract the area to be converted
    area = image[y1:y2, x1:x2]
    #print(x1, y1, x2, y2)



# Convert the extracted area to grayscale
    gray_area = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)

# Apply a binary threshold to the grayscale area
    (thresh, bw_area) = cv2.threshold(gray_area, 82, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #_, bw_area = cv2.threshold(gray_area, 77, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   #_,The first returned value is the threshold that was used.It's often used when the function is set to automatically determine the threshold using methods like Otsu's binarization.hence it is assigned to _, a common convention for unused variables in Python.



# Convert the grayscale area back to BGR format to match the original image's format
    gray_area_bgr = cv2.cvtColor(bw_area, cv2.COLOR_GRAY2BGR)



# Replace the original area with the grayscale area
    image[y1:y2, x1:x2] = gray_area_bgr


startX, startY = 142, 278  # top-left corner
endX, endY = 1450, 1782  # bottom-right corner

# Step 3: Crop the image using array slicing
cropped_image = image[startY:endY, startX:endX]

# Step 4: Save or display the cropped image
# Save the cropped image
cv2.imwrite('images/modified_image_03c.png', cropped_image)





image = cv2.imread(IMG_DIR + 'modified_image_03c.png')

b,g,r = cv2.split(image )
rgb_img = cv2.merge([r,g,b])
plt.imshow(rgb_img)
plt.title('AUREBESH ORIGINAL IMAGE')
plt.show()

# Preprocess image 

gray = get_grayscale(image)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)
images = {'gray': gray, 
          'thresh': thresh, 
          'opening': opening, 
          'canny': canny}


# Plot images after preprocessing

fig = plt.figure(figsize=(13,13))
ax = []

rows = 2
columns = 2
keys = list(images.keys())
for i in range(rows*columns):
    ax.append( fig.add_subplot(rows, columns, i+1) )
    ax[-1].set_title('AUREBESH - ' + keys[i]) 
    plt.imshow(images[keys[i]], cmap='gray')    


# Get OCR output using Pytesseract


# print('-----------------------------------------')
# print(pytesseract.image_to_string(image))
custom_config = r'--oem 3 --psm 6'
print('-----------------------------------------')
print('TESSERACT OUTPUT --> ORIGINAL IMAGE')
print('-----------------------------------------')
#print(pytesseract.image_to_string(image))
print(pytesseract.image_to_string(images[keys[0]], config=custom_config))
print('-----------------------------------------')
# Define a variable
a = pytesseract.image_to_string(images[keys[0]], config=custom_config)
# Determine the data type of 'a'
data_type = type(a)
# Print the data type
print("The data type of a is:", data_type)
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> THRESHOLDED IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(images[keys[1]], config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> OPENED IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(images[keys[2]], config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> CANNY EDGE IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(images[keys[3]], config=custom_config))


import re

data = a

match = re.search(r'Flight Logs >\s*([a-zA-Z]+)', data)

if match:
    # Extract the text that comes after 'Flight Logs >'
    flight_log = match.group(1).strip()
    print(flight_log)
else:
    print("The keyword 'Flight Logs >' was not found in the string.")



# Define the regular expression pattern to find the flight ID
pattern = r'Flight ID\s*([a-zA-Z0-9]+)'

# Perform the search using the regular expression pattern
match1 = re.search(pattern, data)

if match:
    # Extract the flight ID that comes after 'Flight ID'
    flight_id = match1.group(1).strip()
    print(flight_id)
else:
    print("The keyword 'Flight ID' was not found in the string.")


# Define the regular expression pattern to find the date
pattern = r'\d{2} \w{3} \d{4}'

# Perform the search using the regular expression pattern
match2 = re.search(pattern, data)

if match2:
    # Extract the date
    date = match2.group(0).strip()
    print(date)
else:
    print("The date was not found in the string.")


# Define the regular expression pattern to find the timestamp
pattern = r'\d{2}:\d{2}[AP]M - \d{2}:\d{2} [AP]M \(GMT\+\d{2}:\d{2}\)'

# Perform the search using the regular expression pattern
match3 = re.search(pattern, data)

if match3:
    # Extract the timestamp
    timestamp = match3.group(0)
    print(timestamp)
else:
    print("Timestamp not found in the string.")


# Define the regular expression pattern to find the Drone vehicle ID
#pattern = r'Drone vehicle ID\s*([A-Za-z0-9\.]+ -)'
pattern = r'Drone vehicle ID\s+(\w+)'
# Perform the search using the regular expression pattern
match4 = re.search(pattern, data)

if match4:
    # Extract the Drone vehicle ID that comes after 'Drone vehicle ID'
    drone_vehicle_id = match4.group(1).strip()
    print(drone_vehicle_id)
else:
    print("The keyword 'Drone vehicle ID' was not found in the string.")


# Define the regular expression pattern to find the docking station name
pattern = r'Docking station name\s*([A-Za-z0-9\.\-]+)'

# Perform the search using the regular expression pattern
match5 = re.search(pattern, data)

if match5:
    # Extract the docking station name
    docking_station_name = match5.group(1).strip()
    print(docking_station_name)
else:
    print("The docking station name was not found in the string.")

# Define the regular expression pattern to find the docking station name
pattern = r'Station vehicle ID\s*([A-Za-z0-9\.\-]+)'

# Perform the search using the regular expression pattern
match6 = re.search(pattern, data)

if match6:
    # Extract the docking station name
    station_vehicle_id = match6.group(1).strip()
    print(station_vehicle_id)
else:
    print("The Station vehicle ID name was not found in the string.")


# Define the regular expression pattern to find the Total distance
pattern = r'Total distance\s+(\d+\s+m)'

# Perform the search using the regular expression pattern
match7 = re.search(pattern, data)

if match7:
    # Extract the Total distance
    total_distance = match7.group(1).strip()
    print(total_distance)
else:
    print("The Total distance name was not found in the string.")


# Define the regular expression pattern to find the Flight time
pattern = r'Flight time\s+(\d+\.\d+\s+min)'

# Perform the search using the regular expression pattern
match8 = re.search(pattern, data)

if match8:
    # Extract the flight time
    flight_time = match8.group(1).strip()
    print(flight_time)
else:
    print("The flight time was not found in the string.")


# Define the regular expression pattern to find the Maximum altitude
pattern = r'Maximum altitude\s+(\d+\.\d+\s+m)'

# Perform the search using the regular expression pattern
match9 = re.search(pattern, data)

if match9:
    # Extract the Maximum altitude
    maximum_altitude = match9.group(1).strip()
    print(maximum_altitude)
else:
    print("The maximum altitude was not found in the string.")


# Define the regular expression pattern to find the Maximum speed
pattern = r'Maximum speed\s+(\d+\.\d+\s+m/s)'

# Perform the search using the regular expression pattern
match10 = re.search(pattern, data)

if match10:
    # Extract the Maximum speed
    maximum_speed = match10.group(1).strip()
    print(maximum_speed)
else:
    print("The maximum speed was not found in the string.")


# Define the regular expression pattern to find the takeoff time
pattern = r'Takeoff time\s+(\d{2}:\d{2}\s+[APM]{2})'

# Perform the search using the regular expression pattern
match11 = re.search(pattern, data)

if match11:
    # Extract the takeoff time
    takeoff_time = match11.group(1).strip()
    print(takeoff_time)
else:
    print("The takeoff time was not found in the string.")


# Define the regular expression pattern to find the Landing time
pattern = r'Landing time\s+(\d{2}:\d{2}\s+[APM]{2})'
pattern1 = r'Landing time\s+(\d{2}\d{2}\s+[APM]{2})'
# pattern = r'Landing time (\d{2}:\d{2} [AP]M)'
# pattern = r'Landing time (\d{2}:\d{2} [AP]M)'
# Perform the search using the regular expression pattern
match12 = re.search(pattern, data)
match12_5 = re.search(pattern1, data)

if match12:
    # Extract the Landing time
    landing_time = match12.group(1).strip()
    print(landing_time)
elif match12_5:
    landing_time = match12_5.group(1).strip()
    original_string = landing_time
    # Extract hours and minutes
    hours = original_string[:2]
    minutes = original_string[2:4]
    am_pm = original_string[4:]

# Construct the new string with the desired format
    landing_time = f"{hours}:{minutes}{am_pm}"

    print(landing_time)
else:
    print("The Landing time was not found in the string.")


# Define the regular expression pattern to find the Mission type
#pattern = r'Finish action (\w+)'
pattern = r'Mission type\s+(\w+)'

# Perform the search using the regular expression pattern
match13 = re.search(pattern, data)

if match13:
    # Extract the mission type
    mission_type = match13.group(1)
    print(mission_type)
else:
    print("Mission type not found in the string.")


# Define the regular expression pattern to find Finish action
pattern = r'Finish action (\w+)'

# Perform the search using the regular expression pattern
match14 = re.search(pattern, data)

if match14:
    # Extract "RTH"
    finish_action = match14.group(1)
    print(finish_action)
else:
    print("RTH not found in the string.")


# Define the regular expression pattern to find "RC Link Loss"  Failsafes_type
pattern = r'Type (\w+ \w+ \w+)'

# Perform the search using the regular expression pattern
match15 = re.search(pattern, data)

if match15:
    # Extract "RC Link Loss"
    failsafes_type = match15.group(1)
    print(failsafes_type)
else:
    print("RC Link Loss not found in the string.")


# Define the regular expression pattern to find "99 %"
pattern = r'Start battery (\d+ %)'

# Perform the search using the regular expression pattern
match16 = re.search(pattern, data)

if match16:
    # Extract "99 %"
    start_battery = match16.group(1)
    print(start_battery)
else:
    print("Battery percentage not found in the string.")


# Define the regular expression pattern to find End battery
pattern = r'End battery (\d+ %)'
pattern1 = r'End battery (\d+%)'
# Perform the search using the regular expression pattern
match17 = re.search(pattern, data)
match17_5 = re.search(pattern1, data)
if match17:
    # Extract "100 %"
    end_battery = match17.group(1)
    print(end_battery)
elif match17_5:
    end_battery = match17_5.group(1)
    #print(end_battery)

    # Original string
    original_string = end_battery
    # Change the string to add a space before the percentage sign
    end_battery = original_string.replace("%", " %")

    print(end_battery)

else:
    print("Battery percentage not found in the string.")



# #//////////////////////////////
import pandas as pd


SHEET_DIR = 'sheets/'
df = pd.read_csv(SHEET_DIR +  'Flight_Logs_Sheet_1.csv')

# Check if all data in each row is empty (NaN)
#empty_rows = df.isnull()
empty_rows = df.isna().all(axis=1)

# Check if there are any non-empty rows
if empty_rows.all():
    clean_df = df.isnull()
    clean_df = df.dropna()
    
    


    new_data = {
        'No.': ['1'],
        'Flight_Logs': [flight_log],
        'Flight_ID': [flight_id],
        'Date': [date],
        'Timestamp': [timestamp],
        'Drone_vehicle_ID': [drone_vehicle_id],
        'Docking_station_name': [docking_station_name],
        'Station_vehicle_ID': [station_vehicle_id],
        'Total_distance': [total_distance],
        'Flight_time': [flight_time],
        'Maximum_altitude': [maximum_altitude],
        'Takeoff_time': [takeoff_time],
        'Landing_time': [landing_time],
        'Mission_type': [mission_type],
        'Finish_action': [finish_action],
        'Failsafes_Type': [failsafes_type],
        'Start_battery': [start_battery],
        'End_battery': [end_battery]


    }


# Create a DataFrame from the new data
    new_df = pd.DataFrame(new_data)

# Append the new DataFrame to the existing DataFrame
#df.to_csv('existing.csv', mode='a', index=False, header=False)
    clean_df = clean_df._append(new_df, ignore_index=True)
    print(clean_df)

    # # Replace data in empty rows
    # df.loc[empty_rows, :] = new_data
    #  # Append new data to the DataFrame
    # clean_df = pd.concat([clean_df, new_df], ignore_index=True)


# Save DataFrame to CSV
    clean_df=clean_df.to_csv('sheets/Flight_Logs_Sheet_1.csv', mode='w', index=False, header=True)

elif not empty_rows.all():

    clean_df = df.isnull()
    clean_df = df.dropna()
    
    # # Convert the 'Age' column to int
    df['No.'] = df['No.'].astype(int)

# # Check the data types after conversion
    print("\nData types after handling non-numeric values and conversion:")
   #print(df.dtypes)




# # Get the values from the last row of the 'Name' and 'City' columns

    last_row_data_No = df['No.'].iloc[-1]  #show "number"
#last_row_data = df.iloc[-1][['No.']] # show "No. number"
# #last_row_data = df.iloc[-1][['Name', 'City']]

    print("Last row of the DataFrame:")
    print(last_row_data_No)
    Update_No=last_row_data_No+1
    #print(Update_No)


    new_data = {
        'No.': [Update_No],
        'Flight_Logs': [flight_log],
        'Flight_ID': [flight_id],
        'Date': [date],
        'Timestamp': [timestamp],
        'Drone_vehicle_ID': [drone_vehicle_id],
        'Docking_station_name': [docking_station_name],
        'Station_vehicle_ID': [station_vehicle_id],
        'Total_distance': [total_distance],
        'Flight_time': [flight_time],
        'Maximum_altitude': [maximum_altitude],
        'Takeoff_time': [takeoff_time],
        'Landing_time': [landing_time],
        'Mission_type': [mission_type],
        'Finish_action': [finish_action],
        'Failsafes_Type': [failsafes_type],
        'Start_battery': [start_battery],
        'End_battery': [end_battery]


    }


# Create a DataFrame from the new data
    new_df = pd.DataFrame(new_data)

# Append the new DataFrame to the existing DataFrame

    clean_df = clean_df._append(new_df, ignore_index=True)
    print(clean_df)

# Save DataFrame to CSV
    clean_df=clean_df.to_csv('sheets/Flight_Logs_Sheet_1.csv', mode='w', index=False, header=True)

