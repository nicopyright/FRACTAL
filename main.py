# Import  libraries
from Class.Complex import *
from Functions.algorithm import *
from Functions.conversion import *
import pygame
from multiprocessing import Process, cpu_count
import time
import threading

pygame.init()

# collect screen's informations
v_screen_size = pygame.display.Info()
v_screen_width = v_screen_size.current_w
v_screen_height = v_screen_size.current_h

# define the center of the screen
v_center = (v_screen_width // 2, v_screen_height // 2)


v_targ = "julia"

v_w = Complex(-1.0, 0.0)
v_hauteur = 400
v_largeur = 400
v_zoom = 100
v_spreadX = cpu_count() * 2
v_spreadY = cpu_count() * 2


if __name__ == "__main__":

    v_window = pygame.display.set_mode((v_screen_width // 2, v_screen_height // 2))
    v_window.fill("white")

    v_cont = True

    v_mouseX = [0.0] * 50
    v_mouseY = [0.0] * 50
    v_k = 0

    # main loop
    while v_cont:

        # gather inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v_cont = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    v_cont = False

            elif pygame.mouse.get_pressed()[0]:
                start = time.time()
                v_k += 1
                v_mouseX[v_k] = v_mouseX[v_k - 1] + screen_to_complex_plan(pygame.mouse.get_pos())[0] / v_zoom
                v_mouseY[v_k] = v_mouseY[v_k - 1] + screen_to_complex_plan(pygame.mouse.get_pos())[1] / v_zoom
                v_window.fill("white")
                v_zoom *= 2

        """if v_targ == "mandelbrot":
            ths = [[threading.Thread(target=mandelbrot, args=(
                v_window, i * (v_largeur // v_spreadX), j * (y // v_spreadY), (i + 1) * (v_largeur // v_spreadX),
                (j + 1) * (v_hauteur // v_spreadY),
                v_mouseX[v_k], v_mouseY[v_k], v_zoom)) for i in range(-v_spreadX // 2, v_spreadX // 2)] for j in
                   range(-v_spreadY // 2, v_spreadY // 2)]"""


        if v_targ == "julia":
            v_ths = [[threading.Thread(target=julia, args=(
                v_window, i * (v_largeur // v_spreadX), j * (v_hauteur // v_spreadY),
                (i + 1) * (v_largeur // v_spreadX), (j + 1) * (v_hauteur // v_spreadY), v_w,
                0, 0,
                v_zoom)) for i in range(-v_spreadX // 2, v_spreadX // 2)] for j in
                   range(-v_spreadY // 2, v_spreadY // 2)]

            for thx in v_ths:
                for th in thx:
                    th.start()

            for thx in v_ths:
                for th in thx:
                    th.join()

        # refresh display
        pygame.display.flip()

    pygame.quit()
