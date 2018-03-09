import pygame, random, math

red = (255, 0, 0)
width = 800
height = 600
circle_num = 147
tick = 2
speed = 5

pygame.init()
screen = pygame.display.set_mode((width, height))

class circle():
    def __init__(self):
        self.x = random.randint(0,width)
        self.y = random.randint(0,height)
        self.r = 10

    def new(self):
        pygame.draw.circle(screen, red, (self.x,self.y), self.r, tick)

c = []
for i in range(circle_num):
    c.append('c'+str(i))
    c[i] = circle()
    shouldprint = True
    for j in range(len(c)):
        if i != j:
            dist = int(math.hypot(c[i].x - c[j].x, c[i].y - c[j].y))
            if dist < int(c[i].r*2):
                shouldprint = False
    if shouldprint:
        c[i].new()
        pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
