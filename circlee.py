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
        self.screen.fill(pygame.Color(245,241,232))
        for dot in self.model.dots:
            pygame.draw.circle(self.screen,
                             pygame.Color(int(dot.movie.newR),0, int(dot.movie.newB)),
                             (dot.x, dot.y),
                             dot.radius)
        pygame.display.update()


class VisualizerModel(object):
    """ Encodes a model of the game state """
    def __init__(self):
        self.dots = []

    def __str__(self):
        output_lines = []
        return "\n".join(output_lines)

    def run(self):
        rad = 400
        num = 146

        Initial = Movie(0)
        self.dots.append(MovieDot(10, 0, 0, Initial))

        i = 0
        while i < num:
            t = np.random.uniform(0, 2*np.pi)
            r = rad * np.sqrt(np.random.uniform(0, 1))
            x = r * np.cos(t)
            y = r * np.sin(t)

            overlapped = False

            for dot in self.dots:
                dist = math.sqrt((x - dot.x) ** 2 + (y - dot.y) ** 2)
                dif = dist - dot.radius * 2

                if dif < 50  :
                    print("true")
                    overlapped = True


            if not overlapped:
                Overwrite = Movie(i)
                self.dots.append(MovieDot(10, int(x), int(y),Overwrite))
                i += 1


class Dot(object):
    """ Encodes the state of a dot in the visualizer """
    def __init__(self, radius, x, y ):
        self.radius = radius
        self.x = 500 + x
        self.y = 500 + y


    def __str__(self):
        return "Dot radius=%f, x=%f, y=%f" % (self.radius,
                                              self.x,
                                              self.y)

class MovieDot(Dot):
    def __init__(self,radius,x,y,movie0):
        Dot.__init__(self,radius,x,y)
        self.movie = movie0


class Movie(object):
    def __init__(self,index) :
        with open('fandango_score_comparison.csv') as f:
            reader = csv.DictReader(f)
            count = 0
            movies = []
            RT_cris =[]
            RT_users = []
            Meta_cris =[]
            Meta_users = []
            w = []
            for row in reader:
                w.extend(row)
                movie = row['FILM']
                movies.append(movie)
                RT_cri = row['RT_norm'],
                RT_cris.append(RT_cri)
                RT_user = row['RT_user_norm'],
                RT_users.append(RT_user)
                Meta_cri = row['Metacritic_norm']
                Meta_cris.append(Meta_cri)
                Meta_user = row['Metacritic_user_norm'],
                Meta_users.append(Meta_user)
                count +=1
        self.name = movies[index]
        self.critic = float(RT_cris[index][0]) + float(Meta_cris[index][0])
        self.user = float(RT_users[index][0]) + float(Meta_users[index][0])
        self.newR = self.critic* 25.5 + 20
        self.newB = self.user * 25.5 + 20

if __name__ == '__main__':
    pygame.init()

    size = (1000, 1000)

    model = VisualizerModel()
    model.run()
    view = PyGameWindowView(model, size)

    while(True):
        view.draw()
