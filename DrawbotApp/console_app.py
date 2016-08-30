from PIL import Image,ImageEnhance
import numpy as np

class DBImageConverter():
    def __init__(self, file):
        self.raw_image = Image.open(file)
        self.raw_image.thumbnail((thumbsize,thumbsize))
        enhancer = ImageEnhance.Contrast(self.raw_image)
        self.raw_image = enhancer.enhance(2)

        self.thumbsize = 180

    @property
    def vert_line_size(self):
        return self.pixel_size * 0.9

    @property
    def vert_offset(self):
        return (self.pixel_size - self.vert_line_size)/2.0

    def as_array(self):
        return np.asarray(self.raw_image.getdata(),dtype=np.float64).reshape((self.raw_image.size[1],self.raw_image.size[0]))
    
    @property
    def pixels(self):
        reverse = False
        for y,row in enumerate(self.as_array):
            if reverse:
                for x,pixel in reversed([q for q in enumerate(row)]):
                    yield (x-(thumbsize/2),y,pixel,reverse)
            else:
                for x,pixel in enumerate(row):
                    yield (x-(thumbsize/2),y,pixel,reverse)
            reverse = not reverse

    def show(self):
        self.raw_image.show()

dbic = DBImageConverter(r"C:\Users\jimmv\Desktop\apple_man.bmp")
dbic.show()

self.canvas_size = 200

def pixel_size(self):
    return self.canvas_size/thumbsize


def gcode(data,shades=8.0):
    x,y,pixel,reverse = data
    pixel = 255-pixel #invert the color 255 is now black and 0 is white
    #255/x = shades
    #1/x = shades/255
    #x = 255/shades

    pixel = int(pixel*(shades/255.0))

    x = x * pixel_size
    y = y * pixel_size
    if not pixel:
        yield "G0X" + str(round(x+pixel_size,4)) + "Y" + str(round(y+pixel_size/2,4))
    else:
        increment = dbic.pixel_size/pixel

        lst = [i for i in range(0,pixel)]
        if reverse:
            lst = reversed(lst)

        for idx in lst:
            yield "G0X" + str(round(x+(idx*increment),4)) + "Y" + str(round(y+dbic.vert_offset,4))
            yield "G0X" + str(round(x+(idx*increment),4)) + "Y" + str(round(y+dbic.vert_offset+dbic.vert_line_size,4))




input("Waiting ctrl-c to abort")


from lib.DrawBot import DrawBot
drawbot = DrawBot("COM9")
drawbot.sendGCode("M17",True)
drawbot.sendGCode("G0F20",True)

for i in each_pixel(dbic.pixels):
    for g in gcode(i):
        drawbot.sendGCode(g,True)

drawbot.sendGCode("M18",True)
drawBot.shutdown()