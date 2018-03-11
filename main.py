# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import time
import math

color = 100,149,237
screen_color = 255,250,240

class PyGameWindowView(object):
    """ A view of movie data visualizer rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.home = True

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(255,250,240))
        for dot in self.model.dots:
            pygame.draw.circle(self.screen,
                             pygame.Color(dot.color[0], dot.color[1], dot.color[2]),
                             (dot.x, dot.y),
                             dot.radius)
        pygame.display.update()

    def zoom(self, dot):
        """Displays the individual movie-rating dots for the inputed 'dot'"""
        self.screen.fill(pygame.Color(255,250,240))
        self.model.dots = self.model.dot_to_child[dot.label]


class VisualizerModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.size = size
        self.dots = []
        self.home_dots = []
        self.dot_to_child = {}
        self.dots.append(Dot(50, 80, 80, "test"))

        for dot in self.dots:
            self.dot_to_child[dot.label] = [Dot(50, 160, 160, "fandango"), Dot(50, 240, 240, "rt")]
            self.home_dots.append(dot)

    def __str__(self):
        output_lines = []
        # convert each brick to a string for outputting
        for dot in self.dots:
            output_lines.append(str(dot))
        # print one brick per line
        return "\n".join(output_lines)

class Dot(object):
    """ Encodes the state of a dot in the visualizer """
    def __init__(self, radius, x, y, label=None):
        if label == None:
            label = ""

        self.label = label
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return "Dot radius=%f, x=%f, y=%f" % (self.radius, self.x, self.y)


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
            self.model.dots = self.model.home_dots
            self.view.home = not self.view.home


if __name__ == '__main__':
    pygame.init()

    size = (640, 480)

    model = VisualizerModel(size)
    print("Home dots:", model)
    view = PyGameWindowView(model, size)

    controller = PyGameMouseController(model,view)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
    pygame.quit()
