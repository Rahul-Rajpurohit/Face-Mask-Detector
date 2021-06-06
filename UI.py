import subprocess
import tkinter
from tkinter import filedialog

from PIL import Image, ImageTk


def run():
    subprocess.run(["python3", "detect_mask_video.py"])


def image(filename):
    subprocess.run(["python3", "detect_mask_image.py", "--image", filename])


def browse():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    image(filename)


w1 = tkinter.Tk()
path = '/Users/rounaksingh/Desktop/dsce.png'
w1.title("Mask Detection System")
w1.geometry("800x800")
img = ImageTk.PhotoImage(Image.open(path))
panel = tkinter.Label(w1, image=img)
panel.pack()
spc = tkinter.Label(text="")
spc.pack()
l001 = tkinter.Label(text="FACE MASK DETECTOR")
l001.config(font=("Times New Roman", 30))
l001.pack()
spc = tkinter.Label(text="")
spc.pack()
l001 = tkinter.Label(text="Under the Guidance of Dr. Preeti Satish")
l001.config(font=("Times New Roman", 12))
l001.pack()
spc = tkinter.Label(text="")
spc.pack()
b1 = tkinter.Button(text="LAUNCH VIDEO FEED", command=run, width=40, height=2, highlightbackground="green")
b1.pack()
spc = tkinter.Label(text="")
spc.pack()
l001 = tkinter.Label(text="OR")
l001.config(font=("Times New Roman", 12))
l001.pack()
spc = tkinter.Label(text="")
spc.pack()
b2 = tkinter.Button(text="LOAD IMAGE", command=browse, width=40, height=2, highlightbackground="blue")
b2.pack()
spc = tkinter.Label(text="")
spc.pack()
spc = tkinter.Label(text="")
spc.pack()
spc = tkinter.Label(text="")
spc.pack()
spc = tkinter.Label(text="")
spc.pack()
b3 = tkinter.Button(text="EXIT", command=w1.destroy, width=40, height=2, highlightbackground="red")
b3.pack()
w1.mainloop()
