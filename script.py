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
import os
import numpy as np
import webp
from PIL import Image

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
        maps = py360convert.e2c(cv2.cvtColor(myImage, cv2.COLOR_BGR2RGB), face_w=face_w, cube_format='list')

        #webp.save_image(Image.fromarray(maps[0]), os.path.realpath(p + "/front.webp"), quality=80, lossless=False)
        #webp.save_image(Image.fromarray(maps[1]), os.path.realpath(p + "/right.webp"), quality=80, lossless=False)
        #webp.save_image(Image.fromarray(maps[2]), os.path.realpath(p + "/back.webp"), quality=80, lossless=False)
        #webp.save_image(Image.fromarray(maps[3]), os.path.realpath(p + "/left.webp"), quality=80, lossless=False)
        #webp.save_image(Image.fromarray(maps[4]), os.path.realpath(p + "/up.webp"), quality=80, lossless=False)
        #webp.save_image(Image.fromarray(maps[5]), os.path.realpath(p + "/down.webp"), quality=80, lossless=False)

        cv2.imwrite(os.path.realpath(p + "/front2.webp"), maps[0], [cv2.IMWRITE_WEBP_QUALITY, 80])
        cv2.imwrite(os.path.realpath(p + "/right.webp"), maps[1], [cv2.IMWRITE_WEBP_QUALITY, 80])
        cv2.imwrite(os.path.realpath(p + "/back.webp"), maps[2], [cv2.IMWRITE_WEBP_QUALITY, 80])
        cv2.imwrite(os.path.realpath(p + "/left.webp"), maps[3], [cv2.IMWRITE_WEBP_QUALITY, 80])
        cv2.imwrite(os.path.realpath(p + "/up.webp"), maps[4], [cv2.IMWRITE_WEBP_QUALITY, 80])
        cv2.imwrite(os.path.realpath(p + "/down.webp"), maps[5], [cv2.IMWRITE_WEBP_QUALITY, 80])

        status_var.set("Done")


    thread = threading.Thread()
    thread.run = image_converter
    thread.start()

show_frame()
mainFun()
tk.mainloop()
