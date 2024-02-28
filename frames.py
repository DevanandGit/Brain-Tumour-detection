import tkinter
from PIL import ImageTk, Image
import cv2 as cv
import numpy as np
import imutils

class Frames:
    xAxis = 0
    yAxis = 0
    MainWindow = 0
    MainObj = 0
    winFrame = object()
    btnClose = object()
    btnView = object()
    btnBack = object()  # New Back button
    image = object()
    method = object()
    callingObj = object()
    labelImg = 0
    # currentImageIndex = 0
    # imageNames = ["Original MRI Scan", "Binary Image", "Grayscale ROI"]

    def __init__(self, mainObj, MainWin, wWidth, wHeight, function, Object, xAxis=10, yAxis=10):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.MainWindow = MainWin
        self.MainObj = mainObj
        self.MainWindow.title("Brain Tumor Detection")
        if (self.callingObj != 0):
            self.callingObj = Object

        if (function != 0):
            self.method = function

        self.winFrame = tkinter.Frame(self.MainWindow, width=wWidth, height=wHeight)
        self.winFrame['borderwidth'] = 5
        self.winFrame['relief'] = 'ridge'
        self.winFrame.place(x=xAxis, y=yAxis)

        self.btnClose = tkinter.Button(self.winFrame, text="Close", width=50, height=4,
                                      command=lambda: self.quitProgram(self.MainWindow))
        self.btnClose.place(x=690, y=440)
        self.btnView = tkinter.Button(self.winFrame, text="View", width=50, height=4, command=lambda: self.NextWindow(self.method))
        self.btnView.place(x=690, y=320)
        # self.btnBack = tkinter.Button(self.winFrame, text="Back", width=50, height=4, command=self.Back)  # New Back button
        # self.btnBack.place(x=690, y=390)  # New Back button

    def setCallObject(self, obj):
        self.callingObj = obj

    def setMethod(self, function):
        self.method = function

    def quitProgram(self, window):
        self.MainWindow.destroy()

    def getFrames(self):
        return self.winFrame

    def unhide(self):
        self.winFrame.place(x=self.xAxis, y=self.yAxis)

    def hide(self):
        self.winFrame.place_forget()

    def NextWindow(self, methodToExecute):
        listWF = list(self.MainObj.listOfWinFrame)

        if (self.method == 0 or self.callingObj == 0):
            print("Calling Method or the Object from which Method is called is 0")
            return

        if (self.method != 1):
            methodToExecute()
        if (self.callingObj == self.MainObj.DT):
            img = self.MainObj.DT.getImage()
        else:
            print("Error: No specified object for getImage() function")

        jpgImg = Image.fromarray(img)
        current = 0

        for i in range(len(listWF)):
            listWF[i].hide()
            if (listWF[i] == self):
                current = i

        if (current == len(listWF) - 1):
            listWF[current].unhide()
            listWF[current].readImage(jpgImg)
            listWF[current].displayImage()
            self.btnView['state'] = 'disable'
        else:
            listWF[current + 1].unhide()
            listWF[current + 1].readImage(jpgImg)
            listWF[current + 1].displayImage()

        print("Step " + str(current) + " Extraction complete!")

    # def Back(self):
    #     self.currentImageIndex = max(0, self.currentImageIndex - 1)

    #     image_name_label = tkinter.Label(self.winFrame, text=self.imageNames[self.currentImageIndex], height=1, width=20)
    #     image_name_label.place(x=700, y=400)

    #     self.displayImage()

    def removeComponent(self):
        self.btnClose.destroy()
        self.btnView.destroy()
        self.btnBack.destroy()

    def readImage(self, img):
        self.image = img

    #positioning of image on tkinter panel
    def displayImage(self):
        imgTk = self.image.resize((420, 420), Image.ANTIALIAS)
        imgTk = ImageTk.PhotoImage(image=imgTk)
        self.image = imgTk
        self.labelImg = tkinter.Label(self.winFrame, image=self.image)
        self.labelImg.place(x=80, y=140)


