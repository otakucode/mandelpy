__author__ = 'otakucode'

import pygame
from pygame.locals import *
import math
import numpy as np

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1280, 720

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.mandelbrot = None

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        if self.mandelbrot:
            self.mandel_draw()
        else:
            self._display_surf.fill((255, 0, 0, 255))
            self.mandelbrot = Mandelbrot(self.width, self.height)
            print("Calculating...")
            self.mandelbrot.calc()
            print("Done.")
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def mandel_draw(self):
        iterdata = self.mandelbrot.iterdata
        pixel_array = pygame.PixelArray(self._display_surf)

        for x in range(self.mandelbrot.width):
            for y in range(self.mandelbrot.height):
                pixel_array[x, y] = (iterdata[x, y], iterdata[x, y], iterdata[x, y], 255)



class Mandelbrot(object):
    def __init__(self, width, height):
        self.min_x = -2.0
        self.max_x = 1.0
        self.min_y = -1.25
        self.max_y = 1.25
        self.width = width
        self.height = height
        self.iterdata = np.zeros((width, height))

    def calc(self):
        x_stride = (self.max_x - self.min_x) / float(self.width)
        y_stride = (self.max_y - self.min_y) / float(self.height)

        for x in range(self.width):
            for y in range(self.height):
                cur_x = self.min_x + (x_stride * float(x))
                cur_y = self.min_y + (y_stride * float(y))
                cur_z = complex(cur_x, cur_y)
                c = complex(cur_x, cur_y)
                iteration_count = 0

                while abs(cur_z) < 2.0 and iteration_count < 255:
                    cur_z = (cur_z * cur_z) + c
                    iteration_count += 1

                self.iterdata[x, y] = iteration_count




if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()

