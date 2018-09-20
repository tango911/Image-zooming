# Image-zooming
In this python scrypt i have used k-times zooming algorithm for pixel replication taking pivot point as center of image. OpenCV is just used to handel the input and output of image.

## K-Time Zooming
k-time zooming is one of the most perfect zooming algorithm. It caters the challenges of both twice zooming and pixel replication. K in this zooming algorithm stands for zooming factor.

## WORKING:
It works like this way.

First of all , you have to take two adjacent pixels as you did in the zooming twice. Then you have to subtract the smaller from the greater one. We call this output (OP).

Divide the output(OP) with the zooming factor(K). Now you have to add the result to the smaller value and put the result in between those two values.

Add the value OP again to the value you just put and place it again next to the previous putted value. You have to do it till you place k-1 values in it.

Repeat the same step for all the rows and the columns , and you get a zoomed images.

