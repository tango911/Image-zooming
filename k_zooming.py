import cv2
import argparse
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="Path to input image", required=True)
ap.add_argument("-p", "--pivot-point", help="Pivot point coordinates x, y separated by comma (,)",
                required=True)
ap.add_argument("-s", "--scale", help="Scale to zoom", type=int, required=True)
args = vars(ap.parse_args())

image_path = args["image"]
x, y = map(int, args["pivot_point"].split(","))
scale = args["scale"]
image = cv2.imread(image_path)

#My Code Starts here


b = image
m,n,_ = image.shape

# New size for image before zooming/sacling

new_row = ((m-1)/scale)/2
new_column = ((n-1)/scale)/2
x_top = x - new_row 
x_bottom = x + new_row+1
y_left = y - new_column 
y_right = y + new_column+1



#handling the pivot point for the cases where the image size can not be the same as input size. 


if x_top<0:
    x_bottom += -1*(x_top)
    x_top = 0 
if x_bottom>m:
    x_top -= (x_bottom-m)
    x_bottom = m
if y_left<0:
    y_right += -1*(y_left)
    y_left = 0
if y_right>n:
    y_left -= (y_right-n)
    y_right = n



#selecting the portion of image which is to be scaled
    
crop = b[int(x_top):int(x_bottom),int(y_left):int(y_right)]
crop_m,crop_n,_ = crop.shape

#Taking care of pivot point in case of overflow

x,y =  (x_bottom+x_top)/2,(y_left+y_right)/2


# Appling K-TIMES ZOOMING ALGO


out = np.zeros((crop_m,scale*(crop_n-1)+1,3),dtype=np.int16)
out[:,::scale] = crop

#Row wise Zooming
for row in range(0,out.shape[0]-1):
    for column in range(0,out.shape[1]-scale,scale):
        for channel in range(3):
            diff = abs(out[row,column,channel] - out[row,column+scale,channel])
            op = diff//scale
            if out[row,column,channel]>out[row,column+scale,channel]:
                for mid_elem in range(0,scale-1):
                    out[row,column+mid_elem+1,channel] = out[row,column+mid_elem,channel] - op
            else:
                for mid_elem in range(0,scale-1):
                    out[row,column+mid_elem+1,channel] = out[row,column+mid_elem,channel] + op


zoomed_image = np.zeros((scale*(crop_m-1)+1,scale*(crop_n-1)+1,3),dtype=np.int16)
zoomed_image[::scale,:,:] = out

#Column wise zooming
for column in range(0,zoomed_image.shape[1]):
    for row in range(0,zoomed_image.shape[0]-scale,scale):
        for channel in range(0,3):
            diff = zoomed_image[row,column,channel] - zoomed_image[row+scale,column,channel]
            op = diff//scale
            if zoomed_image[row,column,channel] > zoomed_image[row+scale,column,channel]:
                for mid_elem in range(0,scale-1):
                    zoomed_image[row+mid_elem+1,column,channel] = zoomed_image[row+mid_elem,column,channel] - op
            else:
                for mid_elem in range(0,scale-1):
                    zoomed_image[row+mid_elem+1,column,channel] = zoomed_image[row+mid_elem,column,channel] + op

#My Code Ends here
"""
There may be a approx change in dimension of zoomed image if scale is not perfectly divisible by (x-1),(y-1) where x and y
are deminsions of image.
i have applied k time zoom just on croped image which is to be displayed """                    
        
cv2.imwrite("zoomed_image.jpg", np.array(zoomed_image, dtype="uint8"))