import serial
import threading
import time
from PIL import Image,ImageEnhance
import numpy as np

thumbsize = 180
canvas_size = 180
pixel_size = canvas_size/thumbsize

base_image = Image.open(r"C:\Users\jimmv\Desktop\IMG_20100912_152607.jpg")


base_image.thumbnail((thumbsize,thumbsize))
base_image = base_image.convert('L')
base_image.save(r"C:\Users\jimmv\Desktop\IMG_20100912_152607.bmp")
base_image.show()
#enhancer = ImageEnhance.Sharpness(base_image)
#time.sleep(3)
#base_image = enhancer.enhance(4)
#base_image.save(r"C:\Users\jimmv\Desktop\IMG_20100912_152607.bmp")
#base_image.show()
time.sleep(3)
enhancer = ImageEnhance.Contrast(base_image)
base_image = enhancer.enhance(2)
base_image.save(r"C:\Users\jimmv\Desktop\IMG_20100912_152607.bmp")
base_image.show()

#input("Waiting")

imgarray=np.asarray(base_image.getdata(),dtype=np.float64).reshape((base_image.size[1],base_image.size[0]))

def each_pixel():
    reverse = False
    for y,row in enumerate(imgarray):
        if reverse:
            for x,pixel in reversed([q for q in enumerate(row)]):
                yield (x-(thumbsize/2),y,pixel,reverse)
        else:
            for x,pixel in enumerate(row):
                yield (x-(thumbsize/2),y,pixel,reverse)
        reverse = not reverse

def gcode(data):
    x,y,pixel,reverse = data
    pixel = 255-pixel #invert the color 255 is now black and 0 is white
    pixel = int(pixel/32)
    if not pixel:
        yield None
    else:
        x = x * pixel_size
        y = y * pixel_size
        increment = pixel_size/pixel

        lst = [i for i in range(0,pixel)]
        if reverse:
            lst = reversed(lst)

        for idx in lst:
            yield "G0X" + str(round(x+(idx*increment),4)) + "Y" + str(y)
            yield "G0X" + str(round(x+(idx*increment),4)) + "Y" + str(y+pixel_size)


serial_port = serial.Serial('COM9', 115200, timeout=0)

okToGo = []

def handle_data(data):
    print(data)
    if data in ('Ok','Ready'):
        okToGo.append(1);

def read_from_port(ser):
    connected = True
    while connected:
        if ser.inWaiting():
            line = ser.readline().decode('ascii').rstrip()
            handle_data(line)
        time.sleep(0.01)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.daemon = True
thread.start()

def sendToSerial(g):
    global okToGo
    if not okToGo:
        #print("Waiting")
        while not okToGo:
            time.sleep(0.01)
    print("Sending " + g)
    g += '\n'
    serial_port.write(bytes(g.encode()))
    okToGo.remove(1)

sendToSerial("M17")
sendToSerial("G0F20")

for i in each_pixel():
    for g in gcode(i):
        if g is not None:
            sendToSerial(g)

sendToSerial("M18")

#while True:
#    var = input()
#    if var.rstrip() == 'quit':
#        print("Quitting")
#        connected = False
#        break
#    var += '\n'
    
thread.join()
serial_port.close()