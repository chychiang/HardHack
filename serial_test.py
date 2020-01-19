import serial
import time
import threading
import csv

order = ["Ben","Nimish","Oliver","Roy","Pepe"]
x = 0
tookTrash = False
start = 0
trashVal = 0
numberNames = 5
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0,
        parity=serial.PARITY_EVEN, rtscts=1)
ser.write([0X2E, 0X31, 0X30, 0X30, 0X30, 0X31]);
ser.write([0X2E, 0X32, 0X30, 0X30, 0X30, 0X32])
def getPerson( nameCode ):
        if(nameCode == [0X2E, 0X32, 0X30, 0X30, 0X30, 0X32]):
                return "Ben"
        if(nameCode == [0X2E, 0X32, 0X30, 0X30, 0X30, 0X33]):
                return "Nimish"
        if(nameCode == [0X2E, 0X32, 0X30, 0X30, 0X30, 0X34]):
                return "Oliver"
        if(nameCode == [0X2E, 0X32, 0X30, 0X30, 0X30, 0X35]):
                return "Roy"
        if(nameCode == [0X2E, 0X32, 0X30, 0X30, 0X30, 0X36]):
                return "Pepe"

def getData():
        global trashVal
        global tookTrash
        ser1 = serial.Serial('/dev/ttyUSB0', 57600)
        read_serial=ser1.readline()
        # print (read_serial)
        data_ascii = read_serial[0]     # otput is a raw decimal ascii
        data = chr(data_ascii)         # converts into readable character
        if(int(data) != 2):
                trashVal += int(data)
        if(trashVal > 10):
                tookTrash = False
        else:
                tookTrash = True
        ser1.close()

def buttonControl():
        global x
        global start
        global order
        global tookTrash
        global trashVal
        global switch
        # read up to one hundred bytes
        # or as much is in the buffer
        s = ser.read(1)
        command = [[0X2E, 0X32, 0X30, 0X30, 0X30, 0X32],[0X2E, 0X32, 0X30, 0X30, 0X30, 0X33],[0X2E, 0X32, 0X30, 0X30, 0X30, 0X34],[0X2E, 0X32, 0X30, 0X30, 0X30, 0X35],[0X2E, 0X32, 0X30, 0X30, 0X30, 0X36]]

        if (s == b'\x81'):
                x+=1
                x= x%5
                start = time.time()
                ser.write(command[x])

        if(s == b'\xb1'):
                end = time.time()
                if((end - start) > 1):
                        for j in range (0,3):
                                ser.write([0X2E, 0X32, 0X30, 0X30, 0X30, 0X37])
                                for i in range (0,11):
                                        time.sleep(.1)
                                        ser.write([0X2E, 0X34])
                        ser.write(command[x])
        if (s== b'\x82'):
                start = time.time()
                tookTrash = False
                trashVal = 0
                order.remove(getPerson(command[x]))
                order.append(getPerson(command[x]))
        
        if(s == b'\xb2'): #palpatine order 66
                end = time.time()
                if((end - start) > 0.5):
                        ser.write([0X2E, 0X31, 0X30, 0X30, 0X31, 0X33])
                        ser.write([0X2E, 0X32, 0X30, 0X30, 0X31, 0X34])
                time.sleep(2)
                ser.write([0X2E, 0X31, 0X30, 0X30, 0X30, 0X31])
                ser.write(command[x])
def isFull():
        if(tookTrash):
                return 0
        else:
                return 1
        
while True:
        getData()
        if(tookTrash):
                print("Empty")
        else:
                print("Full")
        with open('ftp/files/data.txt','w', newline='') as csvfile:
                mywriter = csv.writer(csvfile, delimiter=',')
                mywriter.writerow([isFull(), order[0]])
        buttonControl()
