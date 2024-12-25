import math
from trig_operations import getDist

radius=200
clearRadius=128
pushStrength=1
predictionSpeed=1

separationStrength=4.8
alignmentStrength=168.0
cohesionStrength=0.000004
targetStrength=0.002
centerStrength=0.00001
center=(450,450)

def boid(positions,rotations,target,dt):
    forces=[[0,0] for i in range(len(positions))]
    
    for i in range(len(positions)):
        neighbours=[]
        
        for j in range(len(positions)):
            if(j==i):
                continue
            
            dist=getDist(positions[i],positions[j])
            
            if(dist==0):
                dist=1
            
            if(dist<radius):
                neighbours.append((positions[j],dist,rotations[j]))
        
        #targeting
        
        targetdist=getDist(positions[i],target)
        if(targetdist<clearRadius):
            forces[i][0]+=(positions[i][0]-target[0])*(clearRadius**2)*targetStrength*pushStrength*max(len(neighbours),1)/(targetdist**2)
            forces[i][1]+=(positions[i][1]-target[1])*(clearRadius**2)*targetStrength*pushStrength*max(len(neighbours),1)/(targetdist**2)
        
        #centering
        
        forces[i][0]+=(center[0]-positions[i][0])*centerStrength*max(len(neighbours),1)
        forces[i][1]+=(center[1]-positions[i][1])*centerStrength*max(len(neighbours),1)
        
        if(len(neighbours)==0):
            continue
        
        #cohesion
        
        neighbourCenter=[0,0]
        for boid in neighbours:
            neighbourCenter[0]+=(boid[0][0]-positions[i][0])*0.5*radius
            neighbourCenter[1]+=(boid[0][1]-positions[i][1])*0.5*radius
        
        neighbourCenter[0]/=len(neighbours)
        neighbourCenter[1]/=len(neighbours)
        
        neighbourCenter[0]+=positions[i][0]
        neighbourCenter[1]+=positions[i][1]
        
        forces[i][0]+=(neighbourCenter[0]-positions[i][0])*cohesionStrength*max(len(neighbours),1)
        forces[i][1]+=(neighbourCenter[1]-positions[i][1])*cohesionStrength*max(len(neighbours),1)
            
        for boid in neighbours:
            vecx=math.cos(boid[2]*math.pi/180)
            vecy=math.sin(boid[2]*math.pi/180)
            
            #separation
            
            predictedx=boid[0][0]+vecx*dt*predictionSpeed
            predictedy=boid[0][1]+vecy*dt*predictionSpeed
            
            forces[i][0]+=(positions[i][0]-predictedx)*separationStrength/(boid[1]**2)
            forces[i][1]+=(positions[i][1]-predictedy)*separationStrength/(boid[1]**2)
            
            #alignment
            
            forces[i][0]+=vecx*alignmentStrength/(boid[1]**2)
            forces[i][1]+=vecy*alignmentStrength/(boid[1]**2)
    
    return forces