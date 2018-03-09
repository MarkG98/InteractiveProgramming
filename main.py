# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import time

class PyGameWindowView(object):
    """ A view of movie data visualizer rendered in a Pygame window """
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
                             pygame.Color(dot.color[0], dot.color[1], dot.color[2]),
                             (dot.x, dot.y),
                             dot.radius)
        pygame.display.update()

class VisualizerModel(object):
    """ Encodes a model of the game state """
    def __init__(self):
        self.dots = []
        self.dots.append(Dot(50, 640//2, 480//2))

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
        self.color = 100,149,237

    def __str__(self):
        return "Dot radius=%f, x=%f, y=%f" % (self.radius, self.x, self.y)

    def zoomStep(self):
        # Increases size of circle when clicked on
        self.radius += 3
        time.sleep(0.0001)

class PyGameMouseController(object):
    """ A controller that uses the mouse to move the paddle """
    def __init__(self,model,view):
        self.model = model
        self.view = view

    def handle_event(self,event):
        """ Handle the mouse event so the paddle tracks the mouse position """
        if event.type == MOUSEBUTTONUP:
            dot = self.model.dots[0]

            originalRadius = dot.radius
            originalColor = dot.color
            for _ in range(400):
                dot.zoomStep()
                view.draw()

            dot.color = (255,255,255)
            dot.radius = originalRadius
            dot.color = originalColor




if __name__ == '__main__':
    pygame.init()

    size = (640, 480)

    model = VisualizerModel()
    print(model)
    view = PyGameWindowView(model, size)

    controller = PyGameMouseController(model,view)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        #model.update()
        view.draw()
