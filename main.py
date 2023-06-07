# Import  libraries
from Class.Complex import *
from Functions.algorithm import *
from Functions.conversion import *
from Functions.video_encoding import *
from Functions.display import *
import pygame
from multiprocessing import cpu_count
import time
import tkinter as tk
from pathlib import Path

v_targ = "julia"

#crete the directories for the captures if they doesn't exist
Path(".\Capture_For_Video").mkdir(parents=True, exist_ok=True)
Path(".\Capture").mkdir(parents=True, exist_ok=True)

def fractal_change():
    """
    Fonction to change button Julia or Mandelbrot
    """
    global v_targ, sv
    if v_targ == "julia":
        v_targ = "mandelbrot"

    elif v_targ == "mandelbrot":
        v_targ = "julia"
    sv.set(v_targ.capitalize())

def fractal():
    pygame.init()
    # collect screen's information
    v_screen_size = pygame.display.Info()
    v_screen_width = v_screen_size.current_w
    v_screen_height = v_screen_size.current_h
    print(v_screen_width, v_screen_height)

    # define the center of the screen
    v_center = (v_screen_width // 2, v_screen_height // 2)

    v_w = Complex(-1, 0)
    v_width = int(v_screen_width // 2)
    v_height = int(v_screen_height // 2)
    v_zoom_initial = 200
    v_zoom = v_zoom_initial
    v_spreadX = cpu_count() * 2
    v_spreadY = cpu_count() * 2

    background = "white"

    v_window = pygame.display.set_mode((v_width, v_height), pygame.RESIZABLE)
    v_cont = True
    v_zoom = 100
    v_window.fill(background)

    t_mouseX = [0.0] * 50
    t_mouseY = [0.0] * 50
    v_k = 0

    start = time.time()
    multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX[v_k], t_mouseY[v_k], v_zoom, v_targ, v_w)
    end = time.time()
    print(end - start)

    # main loop
    while v_cont:
        # gather inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                # if s key is pressed it takes a screenshot and stock it into Capture file
                if event.key == pygame.K_s:
                    path = new_path(".png", "Capture")
                    pygame.image.save(v_window, path)

                if event.key == pygame.K_e:
                    encode('.\Capture_For_Video\*.png', '.\Videos\project.avi', 3)

            elif event.type == pygame.VIDEORESIZE:
                v_height = event.h
                v_width = event.w
                v_window.fill(background)
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
                v_zoom *= 1.5
                start = time.time()
                multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX[v_k], t_mouseY[v_k], v_zoom,
                               v_targ, v_w)
                end = time.time()
                print(end - start)
                pygame.display.flip()
                v_title = "cap{}.png".format(v_k)
                pygame.image.save(v_window, "Capture_For_Video\{}".format(v_title))

            # if right click is pressed a video is recorded
            elif pygame.mouse.get_pressed()[2]:
                v_window.fill("white")
                v_screen_position = screen_to_complex_plan(pygame.mouse.get_pos())
                start = time.time()
                for i in range(0, 100):
                    v_zoom *= 1.05
                    multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY,
                                   (v_screen_position[0]) / v_zoom_initial, (v_screen_position[1]) / v_zoom_initial,
                                   v_zoom, v_targ, v_w)
                    print(i)
                    v_title = "cap{}.png".format(i)
                    pygame.image.save(v_window, "Capture_For_Video\{}".format(v_title))

                end = time.time()
                print("total time: {}".format(end - start))
                encode('.\Capture_For_Video\*.png', '.\Videos\project.avi', 10)

        # refresh display
        pygame.display.flip()


def menu():
    global sv

    v_windows_menu = tk.Tk()
    v_windows_menu.title("Menu")


    # Détermination de la position de la fenêtre au centre de l'écran
    screen_width = v_windows_menu.winfo_screenwidth()
    screen_height = v_windows_menu.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    v_windows_menu.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Titre en gros
    title_label = tk.Label(v_windows_menu, text="Fractal", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    # Bouton Play
    play_button = tk.Button(v_windows_menu, text="Play", command=fractal, font=("Arial", 16, "bold"))
    play_button.pack(pady=10)

    # Bouton fract
    sv = tk.StringVar()
    sv.set(v_targ.capitalize())
    fract_button = tk.Button(v_windows_menu, textvariable=sv, command=fractal_change, font=("Arial", 16, "bold"))
    fract_button.pack(pady=10)

    # Bouton Quit
    quit_button = tk.Button(v_windows_menu, text="Quit", command=v_windows_menu.destroy, font=("Arial", 16, "bold"))
    quit_button.pack(pady=10)

    # Lancement de la boucle principale de la fenêtre
    v_windows_menu.mainloop()


if __name__ == "__main__":
    menu()
    pygame.display.flip()