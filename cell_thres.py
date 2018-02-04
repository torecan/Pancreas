import cv2
import numpy as np


img = cv2.imread('11.jpg')
height, width=img.shape[:2]
img=cv2.resize(img,(width//2 ,height//2))
img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel = np.ones((3,3),np.uint8)


while(1):
	
	# Convert BGR to HSV

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# define range of blue color in HSV
	lower_blue = np.array([100,0,0])
	upper_blue = np.array([140,255,255])
	lower_wh = np.array([0,0,80])
	upper_wh = np.array([360,35,255])
	# Threshold the HSV image to get only blue colors
	mask_B = cv2.inRange(hsv, lower_blue, upper_blue)
	mask_W = cv2.inRange(hsv, lower_wh, upper_wh)

		
	# Bitwise-AND mask and original image
	mask_B=cv2.erode(mask_B,kernel,3)
	mask_W=cv2.erode(mask_W,kernel,3)	
								
	mask=mask_B+mask_W
	mask=cv2.medianBlur(mask,5)	
	cv2.imshow('res1',mask)		

	
	mask_fin=mask
	
	res = cv2.bitwise_and(img,img, mask= mask)
	res=img-res


	lower_brown = np.array([75,0,0])
	upper_brown = np.array([185,255,255])
	mask = cv2.inRange(res, lower_brown, upper_brown)
	mask=cv2.dilate(mask,kernel,iterations = 2)
	mask=cv2.medianBlur(mask,5)	
	mask=cv2.erode(mask,kernel,iterations = 1)
	
	res = cv2.bitwise_and(img,img, mask= mask)


	
	cv2.imshow('frame',img)
	cv2.imshow('mask',mask)
	cv2.imshow('res',res)
	cv2.imwrite('org.jpg',img)
	cv2.imwrite('result.jpg',res)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
