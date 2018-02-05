import cv2
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import os



root = Tk()
root.title('.:: PancreaS ::.')

class Morphologic():
        
        dir_a1=""
        init_dir="/"
        imageFile=""
        font = cv2.FONT_HERSHEY_SIMPLEX
        kernel = np.ones((3,3),np.uint8)

        def fileOpener(self):
                filename = askopenfilename(initialdir=str(self.init_dir),title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")))     
                return filename

        def pathDiverter(self):
                global init
                global file
                global imageFile
                global directory
                global dir_a1
                self.file=self.fileOpener()
                directory,imageFile = os.path.split(self.file)
                self.init_dir = directory               
                imageFile,ext=imageFile.split(".")
                dir_a1=directory+"/experiment_results"
                if not os.path.exists(dir_a1):
                        os.makedirs(dir_a1)


        def Morphology(self):
                
                # Convert BGR to HSV
                
                img = cv2.imread(self.file)
                height, width=img.shape[:2]
                img=cv2.resize(img,(int(width/1.5) ,int(height/1.5)))
                img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

                kernel = np.ones((3,3),np.uint8)
                

                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                # define range of blue color in HSV
                lower_blue = np.array([100,0,0])
                upper_blue = np.array([140,255,255])
                lower_wh = np.array([0,0,80])
                upper_wh = np.array([360,35,255])
                # Threshold the HSV image to get only blue colors
                mask_B = cv2.inRange(hsv, lower_blue, upper_blue)
                mask_W = cv2.inRange(hsv, lower_wh, upper_wh)
                mask=mask_B+mask_W
                ret, mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

                # Bitwise-AND mask and original image
                mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel, iterations = 1)
                bg=cv2.dilate(mask,kernel,iterations=4)                                                 
                dist_transform = cv2.distanceTransform(mask,cv2.DIST_L2,5)
                ret, fg = cv2.threshold(dist_transform,0.01*dist_transform.max(),255,0)
                fg = np.uint8(fg)
                unknown = cv2.subtract(bg,fg)
                
                # Marker labelling
                ret, markers = cv2.connectedComponents(bg)
                # Add one to all labels so that sure background is not 0, but 1
                markers = markers+1
                printer="Detected Cells: " + str(ret)
                
                # Now, mark the region of unknown with zero
                markers[unknown==255] = 0
                markers = cv2.watershed(img,markers)

                img[markers == -1] = [0,255,255]
                

                
                res = cv2.bitwise_and(img,img, mask= bg)



                lower_brown = np.array([70,0,0])
                upper_brown = np.array([190,255,255])
                mask = cv2.inRange(res, lower_brown, upper_brown)
                mask=cv2.dilate(mask,kernel,iterations = 2)
                mask=cv2.medianBlur(mask,5)     
                mask=cv2.erode(mask,kernel,iterations = 1)
                

                res = cv2.bitwise_and(img,img, mask= mask)

                cv2.putText(res,printer,(5,30), self.font, 0.8,(0,0,255),2,cv2.LINE_AA)
                                
                path_1=dir_a1+"/"+imageFile +"_result.jpg"
                path_2=dir_a1+"/"+imageFile +"_detected.jpg"
                cv2.imwrite(path_1,res)
                cv2.imwrite(path_2,img)

                cv2.imshow('ORIGINAL',img)
                cv2.imshow('RESULT',res)                
                k = cv2.waitKey() & 0xFF
                
                if k == 27:     
                        del img,mask,res,kernel
                        cv2.destroyAllWindows()
                



        


n=Morphologic()
w=500
h=400
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))


frame=Frame(root,width=w,height=h)
frame.pack(fill="both")
title=Label(frame,text="The Cellular Thresholding",bg="blue",fg="yellow")
title.pack(fill="both")

back=Frame(master=frame, width=350, height=370, bg='black')
back.pack_propagate(0) 
back.pack(fill="both", expand=1) #Adapts the size to the window
gui_img = ImageTk.PhotoImage(Image.open("medical.png"))
panel = Label(back, image = gui_img)
panel.pack(fill = "both", expand = "yes")

buttons=Frame(master=back, width=100, height=100)
buttons.pack(side="bottom",fill="both") #Adapts the size to the window

button1=Button(buttons,text="Browse",command=n.pathDiverter)
button2=Button(buttons,text="Apply",command=n.Morphology)

button2.pack(side="bottom",fill="both")
button1.pack(side="bottom",fill="both")

root.mainloop()
