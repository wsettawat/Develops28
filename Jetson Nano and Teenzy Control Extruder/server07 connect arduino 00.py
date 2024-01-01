import socket

import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element, SubElement

from time import sleep #time.sleep() relace to sleep()
import Jetson.GPIO as GPIO

import decimal
import math
import multiprocessing as mp

import logging

#!/user/bin/env python3
import serial

ENA = 11 # Controller Enable(spin) Bit (High to Enable(spin) / LOW to Disable(not spin)).

DIR = 13 # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).

PUL = 15 # Stepper Drive Pulses how fast to spin

#

# NOTE: LEAVE DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.

#

#set pin mode

GPIO.setmode(GPIO.BOARD)

#

#

#set GPIO of Jetson Nano for output

GPIO.setup(ENA, GPIO.OUT)

GPIO.setup(DIR, GPIO.OUT)

GPIO.setup(PUL, GPIO.OUT)

#

#

#

#print('Initialization Completed')

#

# Could have used only one DURATION constant but chose two. This gives play options. 

durationFwd = 0 # This is the duration of the motor spinning. used for forward direction

durationBwd = 0 # This is the duration of the motor spinning. used for reverse direction

#print('Duration Fwd set to ' + str(durationFwd))

#print('Duration Bwd set to ' + str(durationBwd))

#

delay = 0.001 # 0.0000001 This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed. (lower delay will make fast rotate but higher delay will make slow rotate)

#print('Speed set to ' + str(delay))

#

#

new_data = 10

current_data = 0

previous_data = 1



cal_Fwd = 0

cal_Bwd = 0



reset_data1 = -10

reset_data2 = -100



int_data = 0

test = 0


x = 0


X0=1000000

z=0

host = '172.31.1.10'
port = 59152

def float_range(start, stop, step):

  while start < stop:

    yield float(start)

    start += decimal.Decimal(step)

def forward():
    #cal_Fwd = (47.068 * (current_data)) + 37.88
    #cal_Fwd = (250* (current_data)) 
    #cal_Fwd = (125* (current_data)) 
    #cal_Fwd = (75* (current_data)) 
    #cal_Fwd = (35* (current_data)) 
    cal_Fwd = (25* (current_data))+50
    #cal_Fwd = (100* (current_data))

    # print("cal_Fwd = %f"%(cal_Fwd))

    durationFwd = math.ceil(cal_Fwd)

    ##print(durationFwd)
    # x = 0
    # while x < durationFwd:
    # for x in range(durationFwd):

    # x = x + 1
    # sleep(delay)

    # sleep(delay)

    # print('x=%f'%(x))

    # sleep(.5)  # pause for possible change direction
    return durationFwd


def loopforward(q, w):
    #set pin mode

    GPIO.setmode(GPIO.BOARD)

    #

    #

    #set GPIO of Jetson Nano for output

    GPIO.setup(ENA, GPIO.OUT)

    GPIO.setup(DIR, GPIO.OUT)

    GPIO.setup(PUL, GPIO.OUT)

    #

    GPIO.output(ENA, GPIO.HIGH)


    sleep(.5) # pause due to a possible change direction

    GPIO.output(DIR, GPIO.LOW) # ccw old LOW new HIGH

    #print('DIR set to HIGH- Moving Forward at ' + str(delay))
    #

    f = w
   # f=5000
    print('%s=%d'%(q,f))
    for x in range(f):
        #print('koko\n')
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        #print('koko\n')
        sleep(delay)

    GPIO.output(ENA, GPIO.LOW)    
    sleep(.5)  # pause for possible change direction
    dfdata = f
    print("dfdata = %f" % (dfdata))
    return

def reverse():
    
    #cal_Bwd = (47.068 * (current_data)) + 37.88
    #cal_Bwd = (250 * (current_data))
    #cal_Bwd = (125 * (current_data))
    #cal_Bwd = (75 * (current_data))
    #cal_Bwd = (35 * (current_data))
    cal_Bwd = (25 * (current_data))+50
    #cal_Bwd = (200 * (current_data))+50

    # print("cal_Bwd = %f" % (cal_Bwd))

    durationBwd = math.ceil(cal_Bwd)

    ##print(durationBwd)
    # x=0
    # while x < durationBwd:
    # for x in range(durationBwd):

    # durationBwd = durationBwd+1
    # sleep(delay)

    # sleep(delay)

    # print('d')

    ##sleep(.5)  # pause for possible change direction

    return durationBwd

def loopbackward(a,s):
    #set pin mode

    GPIO.setmode(GPIO.BOARD)

    #

    #

    #set GPIO of Jetson Nano for output

    GPIO.setup(ENA, GPIO.OUT)
  
    GPIO.setup(DIR, GPIO.OUT)

    GPIO.setup(PUL, GPIO.OUT)

    #

    GPIO.output(ENA, GPIO.HIGH)

    #

    sleep(.5) # pause due to a possible change direction

    GPIO.output(DIR, GPIO.HIGH) #  cw  old HIGH new LOW


    #print('DIR set to LOW - Moving Backward at ' + str(delay))


    #
    r = s
    print('%s=%d' % (a, r))
    for x in range(r):
        GPIO.output(PUL, GPIO.HIGH)
        #print('jojo\n')
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        #print('jojo\n')
        sleep(delay)
        
    GPIO.output(ENA, GPIO.LOW)    
    sleep(.5)  # pause for possible change direction
    drdata = r
    print("drdata = %f" % (drdata))
    return

def senddata():
    sleep(.5)
    ser.write(str(float_data).encode('utf-8'))  
    a=5
    b=6
    c=a+b
    print("c=%d" %c)
    a=0
    b=1
    c1 =a+b
    print("c=%d" %c1)




def cal_speed(v):

    root = ET.parse('ReceivedData.xml').getroot()
    X=root[1].attrib['X'] #stream X and change to float

    #print("rdata = %s" % (rdata))

    X = float(X)


    Y=root[1].attrib['Y'] #stream X and change to float

    #print("rdata = %s" % (rdata))

    Y = float(Y)


    Z=root[1].attrib['Z'] #stream X and change to float

    #print("rdata = %s" % (rdata))

    Z = float(Z)


    A=root[1].attrib['A'] #stream X and change to float

    #print("rdata = %s" % (rdata))

    A = float(A)


    B=root[1].attrib['B'] #stream X and change to float

    #print("rdata = %s" % (rdata))

    B = float(B)


    C=root[1].attrib['C'] #stream X and change to float

    #print("rdata = %s" % (rdata))

    C = float(C)

    
    E=root[1].attrib['E1'] #stream X and change to float

    #print("rdata = %s" % (rdata))

    E = float(E)
    
    
    #velocity mm/s
    velocity = (X-X0)
    
    
    
   
        

    #(math.sqrt( ((X1-X)**2) + ((Y1-Y)**2) + ((Z1-Z)**2)  ) )/ (((E1-E)/60))/60)
    #v= velocity
    
    v.put(velocity)



def steamX(x):
    #root = ET.parse('ReceivedData.xml').getroot()
    X=root[1].attrib['X'] #stream X and change to float
    
    
    #print("X = %s" % (X))

    X = float(X)
    X=X+1000
    #X=str(X)

    x.put(X)


def steamYZ(x):
    print('k')





def job(a,q):
    q.put(a**3)    












def DataTransfer():
    #TRANSFERRED_DATA TEMPLATE
    '''
    <Sensor>
    <Message>Example message</Message>
    <Positions>
        <Current X="4645.2" />
        <Before>
        <X>0.9842</X>
        </Before>
    </Positions>
    <Nmb>8</Nmb>
    <Status>
        <IsActive>1</IsActive>
    </Status>
    <Read>
        <xyzabc X="210.3" Y="825.3" Z="234.3" A="84.2" B="12.3" C="43.5" />
    </Read>
    <Show error="0" temp="9929">Taginfo in attributes</Show>
    <Free>2912</Free>
    </Sensor>
    '''
    #Main Node
    external = Element('External')
    #Node Status Define
    status = SubElement(external, 'Status')
    mode = SubElement(status, 'Mode')
    liveActive = SubElement(status, 'LiveActive')
    errorActive = SubElement(status, 'ErrorActive')
    programNumber = SubElement(status, 'ProgramNumber')
    taskEnable = SubElement(status, 'TaskEnable')
    message = SubElement(status, 'Message')
    #Node : Status Initialize
    mode.text = 'AUT'
    liveActive.text = '1'
    errorActive.text = '0'
    programNumber.text = '0'
    taskEnable.text = '0'
    message.text = 'External Node is Initilized'

    #Node : PoseRequest Define/Initailize
    poseRequest = SubElement(external, 'PoseRequest', 
        X = '100.101', Y = '200.002', Z = '300.003', 
        A = '10.1', B = '20.2', C = '30.3')

    #Node : Extruder Define
    extruder = SubElement(external, "Extruder")
    filamentFeed = SubElement(extruder, "FilamentFeed")
    filamentExtrusion = SubElement(extruder, "FilamentExtrusion")
    #Node : Extruder Initialize
    filamentFeed.text = '0.0'
    filamentExtrusion.text = '0.0'

    #Node : HeatCartridge Define
    heatCartridge = SubElement(external, "HeatCartridge")
    temperatureC = SubElement(heatCartridge, "TemperatureC")
    #Node : HeatCartridge Initialize
    temperatureC.text = '0'

    #Transferred Data Creation
    transferData = open('TransferData.xml', 'w')
    transferData.write('<?xml version="1.0"?>')
    transferData.write(ET.tostring(external).decode('utf-8'))
    transferData.close()

    #TRANSFERRED_DATA TEMPLATE
    '''
    <Robot>
        <Status>
            <Mode></Mode>
            <LiveActive>0</LiveActive>
            <ErrorActive>0</ErrorActive>
            <ProgramNumber>0</ProgramNumber>
            <TaskEnable>0</TaskEnable>
            <Message></Message>
        </Status>
        <PoseCurrent X="85.067657" Y="5.151343" Z="20.812719" A="4.355326" B="-1.605621" C="0.000000" E1="0.000000" E2="0.000000" E3="0.000000" E4="0.000000" E5="" E6="">
        </PoseCurrent>
        <Information>
            <Data1>0.000000</Data1>
            <Data2>0.000000</Data2>
            <Data3>0.000000</Data3>
            <Data4>0.000000</Data4>
        </Information>
    </Robot>
    '''
def ReceiveData(data):
    receivedData = open('ReceivedData.xml', 'w')
    receivedData.write('<?xml version="1.0"?>')
    receivedData.write(data)
    receivedData.close()

if __name__ == '__main__':
     #Port, Socket Initialize
    #sever = socket.socket()
    sever = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    sever.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Reused Port
    #server = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    sever.bind((host, port)) 
    sever.listen(1)


    ser = serial.Serial('/dev/ttyACM0',250000,timeout=1)
    ser.flush()



    while True:
        try:
            #Program Initialize 
            command = ''        
            DataTransfer() #>>> TransferData.xml
            with open('TransferData.xml', 'r') as f:
                command = command + f.read()
            command = command.encode()
        
            #Port, Socket Initialize
            ##sever = socket.socket()
            #sever = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            ##sever.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Reused Port
            #server = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            ##sever.bind((host, port)) 
            ##sever.listen(1)
            print('Waitting for client')
        
            client, addr = sever.accept()
            data = client.recv(1024).decode('utf-8')
        
            client.send(command)
            ReceiveData(data) #>>> #ReceivedData.xml

            root = ET.parse('ReceivedData.xml').getroot()
        
            print('Connected from ', str(addr))

        
            rdata=root[1].attrib['E1'] #stream E1 and change to float

            #print("rdata = %s" % (rdata))

            float_data = float(rdata)
            
            
            v=mp.Queue()
            p1 = mp.Process(target=cal_speed, args=(v, ))
            p1.start()
            v0=v.get()
            print("v = %f" % (v0))

            #X=root[1].attrib['X'] #stream E1 and change to float

            #print("X = %s" % (X))

            #X = float(X)
            

            #q = mp.Queue()
            #p = mp.Process(target=job,args=(2,q))
            #p.start()
            #a = q.get()
            #print("a=%d" %(a))

            #x = mp.Queue()
            #p2 = mp.Process(target=steamX,args=(x,))
            #p2.start()
            #h= x.get()
            #print(h)
            #print("X = %f" % (h))
            #i=float(h)


            


            #durationBwd = math.ceil(float_data)
            #ser.write(str(float_data).encode('utf-8'))

            #p3 = mp.Process(target=senddata)
            #p3.start()

            #ser.write(str(float_data).encode('utf-8'))
            
            #print("float_data =%f"%(float_data))
            #line = ser.readline().decode('utf-8').rstrip()
            #line = ser.readline().decode('utf-8', errors='replace').rstrip()
            #print ("line = %s"%(line))
            
            
            test = float_data + 2
            #print("test = %f\n" %(test))
            new_data = float_data
            #print("new_data = %f " %(new_data))

            #EMA =  new_data*0.00206*previous_data*0.99794

            #new_data = EMA

            current_data = new_data - previous_data
            # print(list(float_range(0, 1, '0.1')))
            #print("previous_data = %f" % (previous_data))
            #print("current_data = %f" % (current_data))
             
            
            if (current_data < reset_data1):
                current_data = new_data
                #f = forward()
                #print("f=%d" % f)

                #p1 = mp.Process(target=loopforward, args=('f', f))
                #p1.start()

                previous_data = current_data


                print("a")
                client.close
            elif (new_data > previous_data):
                #current_data = +(current_data)
                #f = forward()
                #print("f=%d" % f)

                #p1 = mp.Process(target=loopforward, args=('f', f))
                #p1.start()


                ser.write(str(float_data).encode('utf-8'))
                #ser.write(b"ON\n")
                line = ser.readline().decode('utf-8').rstrip()
                print (line)
                

                #if (line == "You sent me: ON"):
                   # previous_data=new_data
                    #print("previous_data =%f"%(previous_data))
                    #time.sleep(1)
                previous_data=new_data    
                #previous_data = current_data
                print("b")
                client.close
            elif (new_data < previous_data):
                #current_data = -(current_data)
                #r = reverse()
                #print("r=%d" % r)

                #p2 = mp.Process(target=loopbackward, args=('r', r))
                #p2.start()

                ser.write(str(float_data).encode('utf-8'))
                #ser.write(b"OFF\n")
                line = ser.readline().decode('utf-8').rstrip()
                print (line)
                #if (line == "You sent me: OFF"):
                    #previous_data=new_data
                    #print("previous_data =%f"%(previous_data))
                    #time.sleep(1)

                previous_data=new_data
                #previous_data = current_data
                print("c")  ### may be disable it have some error and may be use try...error or run server before client
                client.close
            else:
                print("f")
                client.close
                    

            GPIO.cleanup()
            client.close
            print('Connection Endded')

        except Exception:
            logging.exception("processing request")   

    