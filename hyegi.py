# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import time
import csv
import pylab
import random
import math

with open('fandango_score_comparison.csv') as f:
    reader = csv.reader(f)
    count = 0
    w = []
    for row in reader:
        w.extend(row)
        movie = row[0]
        RT_cri = row[9],
        RT_user = row[10],
        Meta_cri = row[11],
        Meta_user = row[12],
        IMDB = row[13],
        count +=1
    print(count)


class PyGameWindowView(object):
    """ A view of movie visualizer rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(255,250,240))
        for dot in self.model.dots:
            pygame.draw.circle(self.screen,
                             pygame.Color(100,149,237),
                             (dot.x, dot.y),
                             dot.radius)
        pygame.display.update()

class VisualizerModel(object):
    """ Encodes a model of the game state """
    def __init__(self):
        self.dots = []
        for i in range(count):
            self.dots.append(Dot(10, random.randrange(640), random.randrange(480)))

        c = []
        for i in range(count):
            c.append('c'+str(i))
            c[i] = Dot(10, random.randrange(640), random.randrange(480))
            shouldprint = True
            for j in range(len(c)):
                if i != j:
                    dist = int(math.hypot(c[i].x - c[j].x, c[i].y - c[j].y))
                    if dist < int(c[i]. radius *2):
                        shouldprint = False
            # if shouldprint:
            #     c[i].new()
            #     pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting
        for dot in self.dots:
            output_lines.append(str(dot))
        # print one brick per line
        return "\n".join(output_lines)

class Dot(object):
    """ Encodes the state of a dot in the visualizer """
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y

    def __str__(self):
        return "Dot radius=%f, x=%f, y=%f" % (self.radius,
                                              self.x,
                                              self.y)
    def new(self):
        self.dots = []
        self.dots.append(Dot(10, random.randrange(640), random.randrange(480)))

if __name__ == '__main__':
    pygame.init()

    size = (640, 480)

    model = VisualizerModel()
    print(model)
    view = PyGameWindowView(model, size)

    while(True):
        view.draw()
