# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


import aoa_locator as locator
import aoa_gui as gui
import time
import math
import tkinter as tk


import numpy as np


# Program to multiply two matrices using list comprehension

# 3x3 matrix
theta = math.pi
a=math.cos(theta*0.32)
b=math.sin(theta*0.32)
A = [[a,b],
    [-b,a]]
c=685
d=-1601
B = [[c],
     [d]]
# 3x4 matrix



# result is 3x4

result = np.dot(A,B)

print(result[0],result[1]) 
translation_x = 685
translation_y = -1601
result[0] += translation_x
result[1] += translation_y
print(result[0],result[1]) 

broker = '192.168.68.102'
topic = "sensor/uwb_tag"

#broker = 'broker.emqx.io'
port = 1883
#topic = "python/mqtt"
#topic = "1"
# Generate a Client ID with the publish prefix.
#client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

client_id = f'subscribe-{random.randint(0, 1000)}'
username = "wedo"
password = "123456"
#global s


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = s
        print("s=",s)
        #msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 1:
            break


def run():
    client = connect_mqtt()
    
    client.loop_start()
   
    publish(client)
    client.loop_stop()

def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))



#Constants
COM_PORT = 13
METER_TO_PIXEL_RATIO = 75
SCENE_SIZE_M = 10
ANC_HEIGHT_M = 1.1
INVALID_VAL = -999

AZIMUTH_INDEX = 0
ELEVATION_INDEX = 1

#variables
tag1 = [0,0] #[azimuth, elevation]
anchor_height = ANC_HEIGHT_M #Height of the anchor in meter, anchor is supposed to be on the ceilling


        
#Implement all uartTransport events
def onErrorReceived(fatal, data):
    print('Error:', data)
    if fatal == 1:
        exit()

def onIQReceived(data):
    pass

def onSWReceived(data):
    pass

def onRRReceived(data):
    pass

def onSSReceived(data):
    pass

def onFRReceived(data):
    pass

def onMEReceived(data):
    pass

def onMAReceived(data):
    pass

def onKEReceived(data):
    global tag1
    
    try:
        elevation = int(data)
        tag1[ELEVATION_INDEX] = elevation
        compute_position(tag1)
    except ValueError:
        print("not valid number")    

def onKAReceived(data):
    global tag1
    
    try:
        azimuth = int(data)
        tag1[AZIMUTH_INDEX] = azimuth
        compute_position(tag1)
    except ValueError:
        print("not valid number")

#Implement all gui events
def onGuiNotifEvent(NotifType, NotifData):
    global anchor_height
    
    if NotifType == "OpenPort":
        locator.set_port_config(115200, NotifData, 1)
        locator.open_port()
    elif NotifType == "closePort":
        locator.close_port()
    elif NotifType == "LocatorHeightChanged":
        try:
            anchor_height = float(NotifData)
        except (ValueError, TypeError):
            pass

def onGuiRequestEvent(RequestType, RequestData):
    if RequestType == "ListPortRequest":
        port_list = locator.get_port_list()
        gui.set_list_port(port_list)
        

#Implement methods
def compute_position(tag):
    if tag[AZIMUTH_INDEX] != INVALID_VAL and tag[ELEVATION_INDEX] != INVALID_VAL:
        #update  position
        x = anchor_height*math.tan(tag[ELEVATION_INDEX]*math.pi/180)*math.cos(tag1[AZIMUTH_INDEX]*math.pi/180)
        y = anchor_height*math.tan(tag[ELEVATION_INDEX]*math.pi/180)*math.sin(tag1[AZIMUTH_INDEX]*math.pi/180)
        x1 = int(x*100) + int(result[0])
        y1 = int(y*100) + int(result[1])
        z1 = int(2.05*100)
        
        p=(tohex(z1, 8))
        z_1=(p.replace('0x', '00'))
       # print(result[0],result[1]) 
        
        print("x1={x1}, y1= {y1} ,  z1= {z_1}".format(x1 = x1, y1 = y1 , z_1= z_1))
        #p="4447"+"4447"+"8000"+x1+y1+z1+"0000"+"0000"+"4000"
        #print(p)
        
        if(x1==0):
            print("zero")
            p=(tohex(x1, 8))
            x_1=(p.replace('0x', '000'))
            print("x1=",x_1)
        
        elif(x1>0):
            print("positive")
            p=(tohex(x1, 8))
            x_1=(p.replace('0x', '00'))
            print("x1=",x_1)
            
        elif(x1<0):
            print("negative")
            n=(tohex(x1, 8))
            x_1=(n.replace('0x', 'ff'))
            print("x1=",x_1)
            
        if(y1==0):
            print("zero")
            p=(tohex(x1, 8))
            y_1=(p.replace('0x', '000'))
            print("y_1=",y_1)   
            
        elif(y1>0):
            print("positive")
            p=(tohex(y1, 8))
            y_1=(p.replace('0x', '00'))
            print("y_1=",y_1)
            
        elif(y1<0):
            print("negative")
            n=(tohex(y1, 8))
            y_1=(n.replace('0x', 'ff'))
            print("y_1=",y_1)
            
        global s    
        s= "4447"+"4447"+"8000"+x_1+y_1+z_1+"0000"+"0000"+"4000"
        if __name__ == '__main__':
          #print("s=",s)
          run()

        #print("s=",s)
        
        #print("(x, y) =", "{:.2f}".format(x), "{:.2f}".format(y))
        #print("(x, y,A,E) =", "{:.2f}".format(x), "{:.2f}".format(y),"{:.2f}", .format(AZIMUTH_INDEX))
        gui.set_tag_coords(x, y, tag[AZIMUTH_INDEX], tag[ELEVATION_INDEX])
        
        #invalidate angles
        tag[AZIMUTH_INDEX] = INVALID_VAL
        tag[ELEVATION_INDEX] = INVALID_VAL

#Setup locator
locator = locator.Locator(COM_PORT, 115200, 1, onErrorReceived)
locator.subscribe_event('KE', onKEReceived)
locator.subscribe_event('KA', onKAReceived)
locator.get_port_config()

#Setup graphical interface

root = tk.Tk()
gui = gui.Gui2D(master=root, scene_size=SCENE_SIZE_M, ratio=METER_TO_PIXEL_RATIO, locator_height=anchor_height, request_subscriber=onGuiRequestEvent, notif_subscriber=onGuiNotifEvent)
gui.master.title("AoA Demo")

#display.master.maxsize(1000, 400)

#main loop
gui.mainloop()

print("Close locator port")
locator.close_port()







