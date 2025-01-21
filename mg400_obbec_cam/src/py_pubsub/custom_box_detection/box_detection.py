import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np
from message_filters import Subscriber, ApproximateTimeSynchronizer
import os
import csv
from ultralytics import YOLO

# Load the YOLO model with the specified ONNX model file
model = YOLO('/home/wedo2/ros2_ws/src/py_pubsub/custom_box_detection/custom_box/runs/segment/train4/weights/best.onnx')

# Global variables for saving location and saving cycle
save_location = os.path.expanduser('~/ros2_ws/src/py_pubsub/custom_box_detection/custom_box/csv')
csv_file_path = os.path.join(save_location, 'object_detection_log.csv')
max_saves = 3
save_count = 0

# Ensure the directory exists
os.makedirs(save_location, exist_ok=True)

# Initialize CvBridge
br = CvBridge()

# Initialize CSV file and write headers
def initialize_csv():
    if not os.path.isfile(csv_file_path):  # Check if file exists
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Object Number', 'CG_x (px)', 'CG_y (px)', 'Width (px)', 'Height (px)', 'Depth (mm)'])
            print(f"CSV file created: {csv_file_path}")

# Function to append data to CSV
def append_to_csv(object_number, cx, cy, width, height, depth_at_cg):
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([object_number, cx, cy, width, height, depth_at_cg])
        print(f"Data appended to CSV: {object_number}, {cx}, {cy}, {width}, {height}, {depth_at_cg}")

def camera_info_callback(msg):
    pass

def sync_callback(color_msg, depth_msg, publisher):
    global save_count

    # Convert ROS Image messages to OpenCV images
    color_image = br.imgmsg_to_cv2(color_msg, desired_encoding='bgr8')
    depth_image = br.imgmsg_to_cv2(depth_msg, desired_encoding='passthrough')

    # YOLO prediction on the RGB image
    results = model.predict(color_image, conf=0.015)

    # List to store bounding boxes and CGs
    boxes_with_cg = []

    # Loop over the prediction results and extract bounding box information
    for result in results:
        for box in result.boxes:
            # Get the coordinates of the bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Calculate the center point (CG) of the bounding box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Append bounding box and CG info to the list
            boxes_with_cg.append(((x1, y1, x2, y2), (cx, cy)))

    # Sort the bounding boxes by the CG's x-coordinate first, then by the y-coordinate
    boxes_with_cg.sort(key=lambda item: (item[1][0], item[1][1]))

    # Loop through the sorted boxes and draw them with the ordered numbers
    for idx, ((x1, y1, x2, y2), (cx, cy)) in enumerate(boxes_with_cg):
        # Draw the bounding box on the image
        cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Draw the center point (CG) on the image
        cv2.circle(color_image, (cx, cy), 5, (0, 0, 255), -1)  # Red dot for CG

        # Add the order number based on CG coordinates
        cv2.putText(color_image, f"#{idx+1}: CG ({cx}, {cy})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Get the depth at the center point (cx, cy) from the depth image
        depth_at_cg = depth_image[cy, cx]

        # Prepare the object information message
        object_info = f"Object #{idx+1}: CG(cx,cy) = ({cx}, {cy}), Width = {x2 - x1} pixels, Height = {y2 - y1} pixels, Depth = {depth_at_cg} mm"
        print(object_info)

        # Publish the object information
        msg = String()
        msg.data = object_info
        publisher.publish(msg)

        # Save the object information to the CSV file if the save count is less than the maximum saves
        if save_count < max_saves:
            append_to_csv(idx+1, cx, cy, x2 - x1, y2 - y1, depth_at_cg)

    # Increment save count after each detection cycle
    save_count += 1

    # Display the RGB image with YOLO predictions
    cv2.imshow('YOLO Prediction with Ordered CG', color_image)

    # Wait for a key press for 1 ms, this allows the window to refresh
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Close the windows if 'q' is pressed
        cv2.destroyAllWindows()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)

    # Create a ROS 2 node
    node = Node('color_depth_yolo_display')

    # Create a publisher for the object information on the 'object_info' topic
    publisher = node.create_publisher(String, 'object_info', 10)

    # Subscriptions for both color and depth images
    color_sub = Subscriber(node, Image, '/camera/color/image_raw')
    depth_sub = Subscriber(node, Image, '/camera/depth/image_raw')
    camera_info_sub = node.create_subscription(CameraInfo, '/camera/depth/camera_info', camera_info_callback, 10)

    # Synchronize color and depth topics
    ts = ApproximateTimeSynchronizer(
        [color_sub, depth_sub],
        queue_size=10,
        slop=0.1  # Allow small time differences
    )
    ts.registerCallback(lambda color_msg, depth_msg: sync_callback(color_msg, depth_msg, publisher))

    # Initialize the CSV file
    initialize_csv()

    # Spin the node
    rclpy.spin(node)

    # Cleanup
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


