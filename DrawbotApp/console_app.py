from PIL import Image,ImageEnhance
import numpy as np
from lib.DrawBot import DrawBotLowLevel


class DBImageConverter():
    def __init__(self, file):
        self.thumbsize = 180
        self.raw_image = Image.open(file)
        self.raw_image.thumbnail((self.thumbsize,self.thumbsize))
        enhancer = ImageEnhance.Contrast(self.raw_image)
        self.raw_image = enhancer.enhance(2)
        self.shader()

    def as_array(self):
        return np.asarray(self.raw_image.getdata(),dtype=np.float64).reshape((self.raw_image.size[1],self.raw_image.size[0]))

    def shader(self,shades=10):
        shades -= 1
        ary = self.as_array()
        for x,row in enumerate(ary):
            for y,pixel in enumerate(row):
                ary[x,y] = int(int(pixel*(shades/255.0)) * (255.0/shades))
        self.raw_image = Image.fromarray(np.uint8(ary))
    
    @property
    def pixels(self):
        reverse = False
        for y,row in enumerate(self.as_array()):
            for x,pixel in (reversed([q for q in enumerate(row)]) if reverse else enumerate(row)):
                yield (x-(self.thumbsize/2),y,pixel,reverse)
            reverse = not reverse

    def show(self):
        self.raw_image.show()

dbic = DBImageConverter(r"C:\Users\jimmv\Desktop\apple_man.bmp")
dbic.show()
#input("Waiting ctrl-c to abort")
drawbot = DrawBotLowLevel("COM9")

canvas_size = 200
pixel_size = 1.0 * canvas_size/dbic.thumbsize
vert_line_size = pixel_size * 0.9
vert_offset = (pixel_size - vert_line_size)/2.0

def gcode(data,shades=10.0):
    shades -= 1
    x,y,pixel,reverse = data
    pixel = 255-pixel #invert the color 255 is now black and 0 is white

    pixel = int(pixel*(shades/255.0))

    x = x * pixel_size
    y = y * pixel_size
    if not pixel:
        yield "G0X" + str(round(x+pixel_size,4)) + "Y" + str(round(y+pixel_size/2,4)),"BLANK"
    else:
        increment = pixel_size/pixel

        lst = [i for i in range(0,pixel)]
        if reverse:
            lst = reversed(lst)

        for idx in lst:
            yield "G0X" + str(round(x+(idx*increment),4)) + "Y" + str(round(y+vert_offset,4)),"linestart"
            yield "G0X" + str(round(x+(idx*increment),4)) + "Y" + str(round(y+vert_offset+vert_line_size,4)),"lineend"

def gcode_lines(pixels):
    for i in pixels:
        for g,type in gcode(i):
            yield g,type

def penup_down_lines(pixels):
    penstate = "UP"
    yield "M5" #pen up
    for g,type in gcode_lines(pixels):
        if type != "BLANK":
            yield g
            if penstate == "UP":
                penstate = "DOWN"
                yield "M3"
        else:
            if penstate != "UP":
                yield "M5"
                penstate = "UP"

from tqdm import tqdm

gcode_count = sum([1 for i in penup_down_lines(dbic.pixels)])
print(gcode_count)
input("Waiting ctrl-c to abort")

drawbot.sendGCode("M17",True)
drawbot.sendGCode("G0F25",True)

[drawbot.sendGCode(g,True) for g in tqdm(iterable=penup_down_lines(dbic.pixels),total=gcode_count)]

drawbot.sendGCode("M18",True)
drawBot.shutdown()