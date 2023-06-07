# Import  libraries
from Class.Complex import *
from Functions.algorithm import *
from Functions.conversion import *
from Functions.video_encoding import *
import pygame
from multiprocessing import cpu_count
import time
from pathlib import Path
import threading

#initialize pygame
pygame.init()

#crete the directories for the captures if they doesn't exist
Path(".\Capture_For_Video").mkdir(parents=True, exist_ok=True)
Path(".\Capture").mkdir(parents=True, exist_ok=True)

# collect screen's information
v_screen_size = pygame.display.Info()
v_screen_width = v_screen_size.current_w
v_screen_height = v_screen_size.current_h

# define the center of the screen
v_center = (v_screen_width // 2, v_screen_height // 2)

#define what fractal it displays between "julia" and "mandelbrot"
v_targ = "julia"

#main variables
v_w = Complex(-1, 0.30)
v_width = 800
v_height = 800
v_zoom_initial = 200
v_zoom = v_zoom_initial
v_spreadX = cpu_count() * 2
v_spreadY = cpu_count() * 2


if __name__ == "__main__":

    v_window = pygame.display.set_mode((v_width, v_height), pygame.RESIZABLE)
    v_window.fill("white")
    pygame.display.flip()
    v_cont = True

    t_mouseX = [0.0] * 50
    t_mouseY = [0.0] * 50
    v_k = 0

    #first fractal to display
    start = time.time()
    multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX[v_k], t_mouseY[v_k], v_zoom,v_targ, v_w)
    end = time.time()

    #print the time it takes to display it
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
                #if s key is pressed it takes a screenshot and stock it into Capture file
                if event.key == pygame.K_s:
                    path=new_path(".png","Capture")
                    pygame.image.save(v_window, path)
            elif event.type == pygame.VIDEORESIZE:
                v_height = event.h
                v_width = event.w
                v_window.fill("white")
                start = time.time()
                multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX[v_k], t_mouseY[v_k], v_zoom, v_targ, v_w)
                end = time.time()
                print(end - start)
            # if left click is pressed it zoom one time into the fractal
            elif pygame.mouse.get_pressed()[0]:
                v_window.fill("white")
                v_screen_position = screen_to_complex_plan(pygame.mouse.get_pos())
                v_k += 1
                t_mouseX[v_k] = t_mouseX[v_k - 1] + v_screen_position[0] / v_zoom
                t_mouseY[v_k] = t_mouseY[v_k - 1] + v_screen_position[1] / v_zoom
                v_zoom *= 1.5
                start = time.time()
                multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX[v_k], t_mouseY[v_k], v_zoom,v_targ, v_w)
                end = time.time()
                print(end-start)
                pygame.display.flip()
                v_title="cap{}.png".format(v_k)
                pygame.image.save(v_window,"Capture_For_Video\{}".format(v_title))
            # if right click is pressed a video is recorded
            elif pygame.mouse.get_pressed()[2]:
                v_window.fill("white")
                v_screen_position = screen_to_complex_plan(pygame.mouse.get_pos())
                start = time.time()
                for i in range(0,100):
                    v_zoom *= 1.05
                    multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, (v_screen_position[0])/v_zoom_initial, (v_screen_position[1])/v_zoom_initial, v_zoom,v_targ, v_w)
                    print(i)
                    v_title="cap{}.png".format(i)
                    pygame.image.save(v_window,"Capture_For_Video\{}".format(v_title))
                end = time.time()
                print("total time: {}".format(end-start))
                encode('.\Capture_For_Video\*.png', '.\Videos\project.avi', 10)
        # refresh display
        pygame.display.flip()

    pygame.quit()
    EraseFile('.\Capture_For_Video')