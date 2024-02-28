import tkinter
from PIL import Image
from tkinter import filedialog
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *

class Gui:
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    fileName = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        global MainWindow
        MainWindow = tkinter.Tk()
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)

        self.DT = DisplayTumor()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 50, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=50, height=4, command=self.browseWindow)
        browseBtn.place(x=690, y=200)

        detectBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Detect Tumor", width=20, height=2, command=lambda: self.check(1))
        detectBtn.place(x=120, y=630)

        viewBtn = tkinter.Button(self.FirstFrame.getFrames(), text="View Tumor Region", width=20, height=2, command=lambda: self.check(2))
        viewBtn.place(x=320, y=630)

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def check(self, option):
        global mriImage
        #print(mriImage)
        if option == 1:
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(mriImage)
            
            if res > 0.5:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Tumor Detected", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="red")
            else:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="No Tumor", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="green")

            resLabel.place(x=150, y=150+420+15)

        elif option == 2:
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):
                if i != 0:
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if len(self.listOfWinFrame) > 1:
                self.listOfWinFrame[0].btnView['state'] = 'active'
        else:
            print("Not Working")

mainObj = Gui()
