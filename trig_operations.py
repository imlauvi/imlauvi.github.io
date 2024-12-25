import math
import random

def convertAngle(theta,x,y):
    if(x>=0 and y>0):
        return theta
    elif(x<0 and y>=0):
        return 180-theta
    elif(x<=0 and y<0):
        return 180+theta
    else:
        return 360-theta

def clampAngle(angle,lower,upper):
    while(lower<0):
        lower+=360
    while(upper<lower):
        upper+=360
    while(angle>upper):
        angle-=360
    while(angle<lower):
        angle+=360
    if(angle>upper):
        if(abs(angle-(lower+360))<abs(angle-upper)):
            angle=lower
        else:
            angle=upper
    angle=angle%360
    return angle

def getDist(point1,point2):
    distx=point2[0]-point1[0]
    disty=point2[1]-point1[1]
    dist=math.sqrt(distx*distx+disty*disty)
    if(dist==0):
        return random.random()
    return dist