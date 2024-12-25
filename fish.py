import math
import pygame
from trig_operations import convertAngle
from trig_operations import clampAngle

class fish:
    turnclamp=0.12
    speed=0.132
    fins=[
        ((1,0,0.9,130),(1,0,1.8,130),(1,1,2.1,125),(1,2,1.8,120),(1,2,0.9,120)),
        ((6,5,0.9,130),(6,5,1.4,130),(6,6,1.7,125),(6,7,1.4,120),(6,7,0.9,120))
        ]

    bodyfins=[
        ((3,2,0,0),(3,2,0.2,0.8),(3,4,0.1,0.5),(3,6,0,0),(3,2,0.01,1)),
        ((11,11,0.3,1),(11,11,0.25,4.5),(11,11,0.2,5),(11,11,0.1,3.5),(11,11,0,4),(11,11,0,1))
    ]
    
    def __init__(self,color,fincolor,scale=1,speedscale=1,startx=450,starty=450,dist=8,sizes=[13,14,15,15,14,14,13,12,10,8,7,6],rotconstrt=15):
        self.locs=[[startx+dist*i,starty] for i in range(len(sizes))]
        self.rots=[0 for i in range(len(sizes))]
        self.sizes=sizes
        
        self.color=color    
        self.fincolor=fincolor    
        self.dist=dist
        self.scale=scale
        self.rotconstrt=rotconstrt
        self.speedscale=speedscale
    
    def getPos(self):
        return self.locs[0]

    def getRot(self):
        return (self.rots[0]+180)%360
    
    def getPoint(self,jointrot,jointloc,angle,radius):
        newrot=(self.rots[jointrot]+180+angle)%360
        newx=self.locs[jointloc][0]+math.cos(newrot*math.pi/180)*radius
        newy=self.locs[jointloc][1]+math.sin(newrot*math.pi/180)*radius
        return (newx,newy)
    
    def getTilt(self):
        tilt=0
        rotstemp=self.rots
        for i in range(1,len(self.locs)):
            while(abs(rotstemp[i]+360-rotstemp[i-1])<abs(rotstemp[i]-rotstemp[i-1])):
                rotstemp[i]+=360
            while(abs(rotstemp[i]-360-rotstemp[i-1])<abs(rotstemp[i]-rotstemp[i-1])):
                rotstemp[i]-=360
            tilt+=rotstemp[i-1]-rotstemp[i]
        return tilt
    
    def move(self,pos,dt):
        vecx=pos[0]-self.locs[0][0]
        vecy=pos[1]-self.locs[0][1]
        if(vecx==0):
            vecx=0.001
        if(vecy==0):
            vecy=0.001
        
        angle=math.atan(abs(vecy)/abs(vecx))*180/math.pi
        angle=convertAngle(angle,vecx,vecy)
        angle=clampAngle(angle,(self.rots[0]+180)%360-fish.turnclamp*dt*self.speedscale,(self.rots[0]+180)%360+fish.turnclamp*self.speedscale*dt)
        
        self.locs[0][0]+=math.cos(angle*math.pi/180)*dt*fish.speed*self.scale*self.speedscale
        self.locs[0][1]+=math.sin(angle*math.pi/180)*dt*fish.speed*self.scale*self.speedscale
        
        self.rots[0]=(angle+180)%360
    
    def update(self):
        for i in range(1,len(self.sizes)):
            vecx=self.locs[i][0]-self.locs[i-1][0]
            vecy=self.locs[i][1]-self.locs[i-1][1]
            if(vecx==0):
                vecx=0.001
            if(vecy==0):
                vecy=0.001
            
            angle=math.atan(abs(vecy)/abs(vecx))*180/math.pi
            angle=convertAngle(angle,vecx,vecy)
            
            angle=clampAngle(angle,self.rots[i-1]-self.rotconstrt,self.rots[i-1]+self.rotconstrt)
            
            self.rots[i]=angle
            
            self.locs[i][0]=self.locs[i-1][0]+math.cos(angle*math.pi/180)*self.dist*self.scale
            self.locs[i][1]=self.locs[i-1][1]+math.sin(angle*math.pi/180)*self.dist*self.scale
    
    def draw(self,surface):
        for fin in fish.fins:
            fin1=[]
            fin2=[]
            
            for point in fin:
                fin1.append(self.getPoint(point[0],point[1],point[3],point[2]*self.sizes[point[0]]*self.scale))
                fin2.append(self.getPoint(point[0],point[1],-point[3],point[2]*self.sizes[point[0]]*self.scale))
                
            pygame.draw.polygon(surface,self.fincolor,fin1)
            pygame.draw.polygon(surface,self.fincolor,fin2)
        
        points=[]
        
        points.append(self.getPoint(0,0,-30,self.sizes[0]*self.scale))
        points.append(self.getPoint(0,0,0,self.sizes[0]*self.scale))
        points.append(self.getPoint(0,0,30,self.sizes[0]*self.scale))
        
        for i in range(len(self.locs)):
            drawpos=self.getPoint(i,i,90,self.sizes[i]*self.scale)
            points.append(drawpos)
            
        points.append(self.getPoint(len(self.locs)-1,len(self.locs)-1,180,self.sizes[len(self.locs)-1]*self.scale))
        
        for i in range(len(self.locs)):
            drawpos=self.getPoint(len(self.locs)-i-1,len(self.locs)-i-1,-90,self.sizes[len(self.locs)-i-1]*self.scale)
            points.append(drawpos)
        pygame.draw.polygon(surface,self.color,points)
        
        eyeloc=0
        eyewidth=0.7
        
        for fin in fish.bodyfins:
            points=[]
            for point in fin:
                points.append(self.getPoint(point[0],point[1],(self.getTilt()*point[2])+180,self.sizes[point[0]]*point[3]*self.scale))
            pygame.draw.polygon(surface,self.fincolor,points)
        
        pygame.draw.circle(surface,(0,0,0),self.getPoint(eyeloc,eyeloc,75,self.sizes[eyeloc]*eyewidth*self.scale),4*self.scale)
        pygame.draw.circle(surface,(0,0,0),self.getPoint(eyeloc,eyeloc,-75,self.sizes[eyeloc]*eyewidth*self.scale),4*self.scale)