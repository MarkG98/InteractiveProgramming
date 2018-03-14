# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *
import time
import math
import copy

#color =
screen_color = 255,250,240

class PyGameWindowView(object):
    """ A view of movie data visualizer rendered in a Pygame window """
    def __init__(self, model, size):
        """ Initialize the view with a reference to the model and the
            specified game screen dimensions (represented as a tuple
            containing the width and height """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.size = size
        self.home = True

        self.default_font = pygame.font.get_default_font()
        self.font_renderer = pygame.font.Font(self.default_font, 70)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(255,250,240))
        for dot in self.model.dots:
            pygame.draw.circle(self.screen,
                             pygame.Color(dot.color[0], dot.color[1], dot.color[2]),
                             (dot.x, dot.y),
                             int(dot.radius))
        label = self.font_renderer.render("Some Text", 1, (255,255,255))
        pygame.display.update()
        self.screen.blit(label, (self.size[0]//2, self.size[1]//2))

    def zoom(self, target):
        """Displays the individual movie-rating dots for the inputed 'dot'"""
        vr = 1.5
        vx = 1
        vy = 1
        color_loc = pygame.Color(target.color[0], target.color[1], target.color[2])

        #copy dots so originals aren't modified and find the target to be zoomed in on
        dots = copy.deepcopy(self.model.dots)
        for dot in dots:
            if dot.label == target.label:
                target = dot

        while target.x < size[0]//2 and target.y < size[1]//2:
            self.screen.fill(pygame.Color(255,250,240))
            for dot in dots:
                if dot.x <= self.size[0]//2 and dot.y < self.size[1]//2:
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
            target.radius += vr

            for dot in dots:
                pygame.draw.circle(self.screen,
                                            color_loc,
                                            (dot.x, dot.y),
                                            int(dot.radius))

            pygame.display.update()
            time.sleep(0.01)


        self.screen.fill(pygame.Color(255,250,240))
        self.model.dots = self.model.dot_to_child[dot.label]



    def returnHome(self):
        """Returns to the screen with all of the movie dots when in a zoomed in state."""
        self.model.dots = self.model.home_dots
        self.home = not self.home

class VisualizerModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.size = size
        self.dots = []
        self.home_dots = []
        self.dot_to_child = {}
        self.dots.append(Dot(50, 80, 80, "test"))
        self.dots.append(Dot(50, 160, 160, "test2"))
        self.dots.append(Dot(50, 300, 100, "test3"))

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
        self.color = 100,149,237

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
            self.view.returnHome()


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
