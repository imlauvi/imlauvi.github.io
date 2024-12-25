import pygame
import asyncio
import fish
import random
from boids import boid

pygame.init()
screen=pygame.display.set_mode((1158,752))

color=(220,130,120)
colorVar=0.1

fishes=[]

for i in range(40):
    fishes.append(fish.fish(
        (
            max(0,
                min(
                    color[0]+random.randint(
                        int(-color[0]*colorVar),
                        int(color[0]*colorVar)
                    )
                ,255)
            ),
            max(0,
                min(
                    color[1]+random.randint(
                        int(-color[1]*colorVar),
                        int(color[1]*colorVar)
                    )
                ,255)
            ),
            max(0,
                min(
                    color[2]+random.randint(
                        int(-color[2]*colorVar),
                        int(color[2]*colorVar)
                    )
                ,255)
            )
        ),
        (
            max(0,
                min(
                    color[0]+random.randint(
                        int(-color[0]*colorVar),
                        int(color[0]*colorVar)
                    )
                ,255)
            )/2,
            max(0,
                min(
                    color[1]+random.randint(
                        int(-color[1]*colorVar),
                        int(color[1]*colorVar)
                    )
                ,255)
            )/2,
            max(0,
                min(
                    color[2]+random.randint(
                        int(-color[2]*colorVar),
                        int(color[2]*colorVar)
                    )
                ,255)
            )/2
        ),
        scale=0.5+(random.random()-0.5)*0.2,
        speedscale=1+(random.random()-0.5)*0.4,
        startx=random.randint(0,1128),
        starty=random.randint(0,752)
    ))

running=True
clock=pygame.time.Clock()

async def main():
    global running
    while running:
        await asyncio.sleep(0)
        screen.fill((100,180,210))
        
        dt=clock.tick(60)
        mousepos=pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        
        positions=[fishobj.getPos() for fishobj in fishes]
        rotations=[fishobj.getRot() for fishobj in fishes]
        
        movements=boid(positions,rotations,mousepos,dt)
        
        for i in range(len(fishes)):
            movement=[fishes[i].getPos()[0]+movements[i][0],fishes[i].getPos()[1]+movements[i][1]]
            fishes[i].move(movement,dt)
            fishes[i].update()
            fishes[i].draw(screen)
            
        pygame.display.flip()

asyncio.run(main())