import cv, copy
import numpy
import os,sys

rect1=(00, 00, 200, 480)
rect2=(300, 0, 200, 480)

test_run=False
skip_diff=False

if test_run:
    cv.NamedWindow('Camera')
    cv.NamedWindow('Crop 1')
    cv.NamedWindow('Crop 2')
device = 0 
capture = cv.CreateCameraCapture(0)
#cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_WIDTH, 640)
#cv.SetCaptureProperty(capture, cv.CAP_PROP_FRAME_HEIGHT, 480)    

color_frame = cv.QueryFrame(capture)

frame_GS_32F = cv.CreateImage((color_frame.width,color_frame.height), cv.IPL_DEPTH_32F, 1)
frame_GS = cv.CreateImage((color_frame.width,color_frame.height), cv.IPL_DEPTH_8U, 1)
old_frame = cv.CreateImage((color_frame.width,color_frame.height), cv.IPL_DEPTH_8U, 1)
diff_frame = cv.CreateImage((color_frame.width,color_frame.height), cv.IPL_DEPTH_8U, 1)

crop1 = cv.CreateImage((rect1[2],rect1[3]), cv.IPL_DEPTH_8U, 1)
crop2 = cv.CreateImage((rect2[2],rect2[3]), cv.IPL_DEPTH_8U, 1)

hist1=cv.CreateHist([32], cv.CV_HIST_ARRAY, [[0,256]],1)
hist2=cv.CreateHist([32], cv.CV_HIST_ARRAY, [[0,256]],1)

while 1:
    color_frame = cv.QueryFrame(capture)
    cv.Copy(frame_GS,old_frame)
    cv.CvtColor(color_frame,frame_GS, cv.CV_RGB2GRAY)
    cv.AbsDiff(frame_GS, old_frame, diff_frame)
    if skip_diff: 
        cv.Copy(frame_GS, diff_frame)
    cv.SetImageROI(diff_frame, rect1)
    cv.Copy(diff_frame, crop1)
    cv.ResetImageROI(diff_frame)
    cv.SetImageROI(diff_frame, rect2)
    cv.Copy(diff_frame, crop2)
    cv.ResetImageROI(diff_frame)
    cv.CalcHist([crop1], hist1)
    cv.CalcHist([crop2], hist2)
    np_hist1=numpy.array([hist1.bins[i] for i in range(32)])
    np_hist2=numpy.array([hist2.bins[i] for i in range(32)])
    np_hist1=np_hist1/numpy.mean(np_hist1)
    np_hist2=np_hist2/numpy.mean(np_hist2)

    a=numpy.mean(np_hist1*numpy.arange(len(np_hist1)))
    b=numpy.mean(np_hist2*numpy.arange(len(np_hist2)))

    if a>0.2 and b<0.1:
        if test_run:
            print "%.8f %.8f"%(a, b)
        else: 
            sys.exit(0)
        
    #(keypoints, descriptors) = cv.ExtractSURF(frame_GS, None, cv.CreateMemStorage(), (0, 400, 3, 4))
    #for ((x, y), laplacian, size, dir, hessian) in keypoints:
    #    if size<30:
    #        cv.Circle(color_frame, (int(x),int(y)), int(size), cv.Scalar(0,0,256))
    if test_run:
        cv.ShowImage('Camera', diff_frame)
        cv.ShowImage('Crop 1', crop1)
        cv.ShowImage('Crop 2', crop2)
    k = cv.WaitKey(10)
    if k == 0x1b: # ESC
        print 'ESC pressed. Exiting ...'
        break
