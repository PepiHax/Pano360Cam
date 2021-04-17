import cv2 as cv2
import py360convert
import tkinter as tk
import tkinter.filedialog
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import threading
import time

import numpy as np

face_w = 4096

window = tk.Tk()
window.title("Epi to Cubemap")
status_var = tk.StringVar()
statusLabel = tk.Label(window, textvariable=status_var)
status_var.set("Running")
statusLabel.pack()

theFile = tk.filedialog.askopenfile()
myImage = cv2.imread(theFile.name)
myImageRGB = cv2.resize(cv2.cvtColor(myImage, cv2.COLOR_BGR2RGB), (int(
    myImage.shape[1] / 10), int(myImage.shape[0] / 10)))


def show_frame():
    fig = Figure(dpi=100)
    fig.add_subplot().imshow(myImageRGB)
    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



def mainFun():
    p = tk.filedialog.askdirectory()

    def image_converter():
        myImage2 = py360convert.e2c(myImage, face_w=face_w)

        left = myImage2[face_w:face_w+face_w, 0:0+face_w]
        front = myImage2[face_w:face_w+face_w, face_w:face_w+face_w]
        right = myImage2[face_w:face_w+face_w, face_w*2:face_w*2+face_w]
        back = myImage2[face_w:face_w+face_w, face_w*3:face_w*3+face_w]
        up = myImage2[0:0+face_w, face_w:face_w+face_w]
        down = myImage2[face_w*2:face_w*2+face_w, face_w:face_w+face_w]

        cv2.imwrite(p+"/map.png", myImage2)

        cv2.imwrite(p+"/left.png", left)
        cv2.imwrite(p+"/front.png", front)
        cv2.imwrite(p+"/right.png", right)
        cv2.imwrite(p+"/back.png", back)
        cv2.imwrite(p+"/up.png", up)
        cv2.imwrite(p+"/down.png", down)

        status_var.set("Done")


    thread = threading.Thread()
    thread.run = image_converter
    thread.start()

show_frame()
mainFun()
tk.mainloop()
