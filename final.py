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
import copy


class PyGameWindowView(object):
    """ A view of movie visualizer rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.size = size
        self.home = True

        self.myfont = pygame.font.Font(None, 40)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(245,241,232))
        for dot in self.model.dots:
            pygame.draw.circle(self.screen,
                             pygame.Color(int(dot.movie.newR),0, int(dot.movie.newB)),
                             (dot.x, dot.y),
                             dot.radius)
        if not self.home:
            self.label = self.myfont.render("Movie: %s" % str(self.text), True, (0, 0, 0))
            self.screen.blit(self.label, (self.size[0]//4, self.size[1]//4))
        pygame.display.update()

    def zoom(self, target):
        """Displays the individual movie-rating dots for the inputed 'dot'"""
        vr = 1.5
        vx = 1
        vy = 1
        self.text = target.label

        #copy dots so originals aren't modified and find the target to be zoomed in on
        dots = copy.deepcopy(self.model.dots)
        for dot in dots:
            if dot.label == target.label:
                target = dot

        while target.radius < 600:
            self.screen.fill(pygame.Color(255,250,240))
            for dot in dots:
                if dot.x < self.size[0]//2 and dot.y < self.size[1]//2:
                    dot.x += vx
                    dot.y += vy
                elif dot.x > self.size[0]//2 and dot.y < self.size[1]//2:
                    dot.x -= vx
                    dot.y += vy
                elif dot.x < self.size[0]//2 and dot.y > self.size[1]//2:
                    dot.x += vx
                    dot.y -= vy
                elif dot.x > self.size[0]//2 and dot.y > self.size[1]//2:
                    dot.x -= vx
                    dot.y -= vy
                elif (dot.x == self.size[0]//2 or dot.y == self.size[1]//2) and dot != target:
                    dot.x = 2000
                    dot.y = 2000
            target.radius += vr

            for dot in dots:
                pygame.draw.circle(self.screen,
                                            pygame.Color(int(dot.movie.newR),0, int(dot.movie.newB)),
                                            (dot.x, dot.y),
                                            int(dot.radius))

            pygame.display.update()
            time.sleep(0.001)


        self.screen.fill(pygame.Color(255,250,240))
        self.model.dots = self.model.dot_to_child[dot.label]

    def returnHome(self):
        """Returns to the screen with all of the movie dots when in a zoomed in state."""
        self.model.dots = self.model.home_dots

class VisualizerModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.size = size
        self.dots = []
        self.home_dots = []
        self.dot_to_child = {}
        self.run()

        for dot in self.dots:
            self.dot_to_child[dot.label] = []
            self.home_dots.append(dot)

    def __str__(self):
        output_lines = []
        for dot in self.dots:
            output_lines.append(str(dot))
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
                    #print("true")
                    overlapped = True


            if not overlapped:
                Overwrite = Movie(i)
                self.dots.append(MovieDot(10, int(x), int(y),Overwrite))
                i += 1


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

class MovieDot(Dot):
    def __init__(self,radius,x,y,movie0):
        Dot.__init__(self,radius,x,y)
        self.movie = movie0
        self.label = self.movie.name


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

class PyGameMouseController(object):
    """ Uses the mouse to zoom in and out of a specific movie. """
    def __init__(self,model,view):
        self.model = model
        self.view = view

    def handle_event(self,event):
        """ Handle the mouse event so that when a movie is clicked on, its individual movie-rating sites are displayed.
            of those are already displayed, then it will go back to the movie dots."""

        if event.type == MOUSEBUTTONUP and self.view.home:
            for dot in self.model.dots:
                #checks which circle the mouse click was in the radius of
                if math.hypot(dot.x - pygame.mouse.get_pos()[0], dot.y - pygame.mouse.get_pos()[1]) < dot.radius:
                    self.view.zoom(dot)
                    self.view.home = not self.view.home

        elif event.type == MOUSEBUTTONUP and not self.view.home:
            self.view.returnHome()
            self.view.home = not self.view.home

if __name__ == '__main__':
    pygame.init()

    size = (1000, 1000)

    model = VisualizerModel(size)
    #model.run()
    view = PyGameWindowView(model, size)

    controller = PyGameMouseController(model,view)

    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
