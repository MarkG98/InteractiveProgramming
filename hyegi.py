# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time
import csv
import pylab
import random
import math
import matplotlib.pyplot as plt
import numpy as np

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
        rad = 200
        num = 147
        t = np.random.uniform(0, 2*np.pi, num)
        r = rad * np.sqrt(np.random.uniform(0, 1, num))

        for i in range(count):
            x = r * np.cos(t)
            y = r * np.sin(t)
            self.dots.append(Dot(10, int(x[i]), int(y[i])))

    def __str__(self):
        output_lines = []
        for dot in self.dots:
            output_lines.append(str(dot))
        return "\n".join(output_lines)

class Dot(object):
    """ Encodes the state of a dot in the visualizer """
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = 500 + x
        self.y = 500 + y

    def __str__(self):
        return "Dot radius=%f, x=%f, y=%f" % (self.radius,
                                              self.x,
                                              self.y)


if __name__ == '__main__':
    pygame.init()

    size = (1000, 1000)

    model = VisualizerModel()
    print(model)
    view = PyGameWindowView(model, size)

    while(True):
        view.draw()
