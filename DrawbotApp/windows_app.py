

from tkinter import Tk,Frame,Canvas,BOTH,X,RAISED,Button,filedialog,Label,W,SUNKEN,BOTTOM
from svg.path import parse_path,path

path.ERROR = 1.0
path.MIN_DEPTH = 2
from SVGScale import resize

class InnerCanvasFrame(Frame):
    def __init__(self, master = None, cnf = {}, **kw):
        super().__init__(master, cnf, **kw)
        self.padding = 5
        self.pack(expand=1, fill=BOTH, pady=self.padding, padx=self.padding)
        self.canvas = Canvas(self, bg='red', width=500, height=500)
        self.canvas.pack()


class MainWindow(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.window_size = (800,800)
        self.parent = parent
        self.parent.title("Centered window")
        self.pack(fill=BOTH, expand=1)
        icf = InnerCanvasFrame(self, bd=2, relief=RAISED)
        self.canvas = icf.canvas
        btn = Button(self, text="Loadit",command=self.load_svg)
        btn.pack()
        self.status_label = Label(self, text="", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.pack(side=BOTTOM, fill=X)
        self.centerWindow()
        
    def set_status(self,text):
        self.status_label.config(text = text)
        self.status_label.update_idletasks()

    def centerWindow(self):
        w,h = self.window_size
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def load_svg(self):
        filename = filedialog.askopenfilename( filetypes = (("SVG files","*.svg"),("All files","*.*")))
        threaded_loader(filename,self)
        

def threaded_loader(filename,master):
    from threading import Thread
    def run():
        master.set_status("Loading file")
        with open(filename) as svg_file:
            from xml.dom import minidom
            doc = minidom.parse(svg_file)
            path_strings = [path.getAttribute('d') for path
                            in doc.getElementsByTagName('path')]
            doc.unlink()
        for path_string in path_strings:
            last_x,last_y = None,None
            for x,y in points(path_string):
                if last_x is not None:
                    master.canvas.create_line((last_x,last_y,x,y))
                last_x = x
                last_y = y
        master.set_status("Done... Idle")
    thread = Thread(target = run)
    thread.start()


def points(path_string,max_len=2.0):
    path = parse_path(path_string)
    print(path)
    len = path.length()
    step = int(len/max_len)

    for i in range(0,step):
        point = path.point(i/step)
        yield(round(point.real),round(point.imag))
    point = path.point(1)
    yield(round(point.real),round(point.imag))


def main():
  
    root = Tk()
    ex = MainWindow(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  