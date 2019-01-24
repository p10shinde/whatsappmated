from tkinter import *
from PIL import Image
from PIL import ImageTk

class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        # self.QUIT = Button(self)
        # self.QUIT["text"] = "QUIT"
        # self.QUIT["fg"]   = "red"
        # self.QUIT["command"] =  self.quit

        # self.QUIT.pack({"side": "left"})

        # self.hi_there = Button(self)
        # self.hi_there["text"] = "Hello",
        # self.hi_there["command"] = self.say_hi

        # self.hi_there.pack({"side": "left"})
        # try:
	       #  width = 500
	       #  height = 500
	       #  size = width,height
	       #  img = Image.open("C:\\xampp\\htdocs\\python\\capture.png")
	       #  img = img.resize(size, Image.ANTIALIAS)
	       #  photoImg =  ImageTk.PhotoImage(img)
	       #  self.photoLabel = Label(self, image=photoImg)
	       #  self.photoLabel.pack()
        # except:
        #     print("Eror")

        self.grid(row=0)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = Image.open('capture.png')
        resized = self.original.resize((500, 400),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized) # Keep a reference, prevent GC
        self.display = Label(self, image = self.image)
        self.display.grid(row=0)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()