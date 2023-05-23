# Import  libraries
from Class.Complex import *
from Functions.algorithm import *
from Functions.conversion import *
import pygame
from multiprocessing import cpu_count
import time

pygame.init()


# collect screen's information
v_screen_size = pygame.display.Info()
v_screen_width = v_screen_size.current_w
v_screen_height = v_screen_size.current_h

# define the center of the screen
v_center = (v_screen_width // 2, v_screen_height // 2)


v_targ = "julia"

v_w = Complex(-1, 0)
v_width = int(v_screen_width // 2)
v_height = int(v_screen_height // 2)
v_zoom = 100
v_spreadX = cpu_count() * 2
v_spreadY = cpu_count() * 2


if __name__ == "__main__":

    v_window = pygame.display.set_mode((v_width, v_height), pygame.RESIZABLE)
    v_window.fill("white")

    v_cont = True

    t_mouseX = [0.0] * 50
    t_mouseY = [0.0] * 50
    v_k = 0

    start = time.time()
    multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX, t_mouseY, v_zoom,v_targ, v_w, v_k)
    end = time.time()
    print(end-start)

    # main loop
    while v_cont:

        # gather inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v_cont = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    v_cont = False

            elif event.type == pygame.VIDEORESIZE:
                v_height = event.h
                v_width = event.w
                v_window.fill("white")

                start = time.time()
                multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX, t_mouseY, v_zoom, v_targ, v_w, v_k)
                end = time.time()
                print(end - start)

            elif pygame.mouse.get_pressed()[0]:
                v_window.fill("white")
                v_screen_position = screen_to_complex_plan(pygame.mouse.get_pos())
                v_k += 1
                t_mouseX[v_k] = t_mouseX[v_k - 1] + v_screen_position[0] / v_zoom
                t_mouseY[v_k] = t_mouseY[v_k - 1] + v_screen_position[1] / v_zoom
                v_zoom *= 2
                start = time.time()
                multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX, t_mouseY, v_zoom,v_targ, v_w, v_k)
                end = time.time()
                print(end-start)


        # refresh display
        pygame.display.flip()

    pygame.quit()
