import cv2
import numpy as np

def MotionDetection(frame1,frame2):
  d=cv2.absdiff(frame1,frame2)
  grey=cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
  blur =cv2.GaussianBlur(grey,(5,5),0)
  ret,th=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
  dilated=cv2.dilate(th,np.ones((3,3),np.uint8),iterations=3)
  c,h=cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  cv2.drawContours(frame1,c,-1,(0,255,0),2)
  return frame1

def main():

   cap=cv2.VideoCapture('Assets/video/test.mp4')

   ret,frame1 = cap.read()
   ret,frame2 = cap.read()

   while ret:
      frame1=MotionDetection(frame1,frame2)
      cv2.imshow("inter",frame1)
      if cv2.waitKey(40) == 27:
         break
      frame1 = frame2
      ret,frame2= cap.read()

   cv2.destroyAllWindows()
   cap.release()
main()   