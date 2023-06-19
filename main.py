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
from tkinter import ttk
from pathlib import Path

v_targ = "julia"
v_targ_temp = v_targ
v_fonct = 1
v_fonct_temp = 1
fonctions_frac = ["z² + w", "cos(z) + w"]
is_saved = True


#create the directories for the captures if they doesn't exist
Path(".\Capture_For_Video").mkdir(parents=True, exist_ok=True)
Path(".\Capture").mkdir(parents=True, exist_ok=True)


def fractal_change(name):
    global v_targ_temp, is_saved
    v_targ_temp = name
    if is_saved:
        is_saved = False
    print("targ_temp : ", v_targ_temp)
    text_info_tosave.set("Fractal choosen : {} {}\n"
                         "Fonction choosen : {}".format(v_targ_temp.capitalize(), "" if is_saved else "*",
                                                        fonctions_frac[v_fonct_temp - 1]))

def action_fonct(event):
    global v_fonct_temp, is_saved
    choice = liste_fonc_fract.get()
    print("Fonc_temp : ", choice)
    if choice == "z² + w":
        v_fonct_temp = 1
        is_saved = False
    elif choice == "cos(z) + w":
        v_fonct_temp = 2
        is_saved = False
    print("is_saved : ", is_saved)
    text_info_tosave.set("Fractal choosen : {} {}\n"
                         "Fonction choosen : {}".format(v_targ_temp.capitalize(), "" if is_saved else "*",
                                                        fonctions_frac[v_fonct_temp - 1]))


def save_fonct():
    global v_targ, v_fonct, is_saved
    v_targ = v_targ_temp
    v_fonct = v_fonct_temp
    is_saved = True
    text_info_current.set("Current fractal : {}\n"
                  "Current fonction : {}".format(v_targ.capitalize(), fonctions_frac[v_fonct - 1]))
    text_info_tosave.set("Fractal choosen : {} {}\n"
                         "Fonction choosen : {}".format(v_targ_temp.capitalize(), "" if is_saved else "*",
                                                        fonctions_frac[v_fonct_temp - 1]))
    print("Current fractal : {}".format(v_targ))
    print("Current fonction : {}".format(v_fonct))
    print("is_saved : ", is_saved)


def fractal():
    pygame.init()
    # collect screen's information
    v_screen_size = pygame.display.Info()
    v_screen_width = v_screen_size.current_w
    v_screen_height = v_screen_size.current_h
    print(v_screen_width, v_screen_height)

    v_w = Complex(-1, 0)
    v_width = int(v_screen_width // 2)
    v_height = int(v_screen_height // 2)
    v_zoom_initial = 150
    v_spreadX = cpu_count() * 2
    v_spreadY = cpu_count() * 2

    background = "white"

    v_window = pygame.display.set_mode((v_width, v_height), pygame.RESIZABLE)
    v_cont = True
    v_zoom = v_zoom_initial
    v_window.fill(background)

    t_mouseX = [0.0] * 50
    t_mouseY = [0.0] * 50
    v_k = 0

    start = time.time()
    multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX[v_k], t_mouseY[v_k], v_zoom, v_targ,
                   v_w, v_fonct)
    end = time.time()
    print(end - start)

    # main loop
    while v_cont:
        # gather inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v_cont = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    v_cont = False
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
                multithreading(v_window, v_width, v_height, v_spreadX, v_spreadY, t_mouseX[v_k], t_mouseY[v_k], v_zoom,
                               v_targ, v_w, v_fonct)
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
                               v_targ, v_w, v_fonct)
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
                                   v_zoom, v_targ, v_w, v_fonct)
                    print(i)
                    v_title = "cap{}.png".format(i)
                    pygame.image.save(v_window, "Capture_For_Video\{}".format(v_title))

                end = time.time()
                print("total time: {}".format(end - start))
                encode('.\Capture_For_Video\*.png', '.\Videos\project.avi', 10)

def window_settings():
    global liste_fonc_fract, text_info_current, text_info_tosave, is_saved

    v_windows_settings = tk.Tk()
    v_windows_settings.title("Settings")
    text_info_current = tk.StringVar(v_windows_settings)
    text_info_tosave = tk.StringVar(v_windows_settings)

    screen_width = v_windows_settings.winfo_screenwidth()
    screen_height = v_windows_settings.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    v_windows_settings.geometry(f"{window_width}x{window_height}+{x}+{y}")

    title_label = tk.Label(v_windows_settings, text="Settings", font=("Arial", 24, "bold"))

    julia_fract = tk.Button(v_windows_settings, text="Julia",
                            command=lambda: fractal_change("julia"), font=("Arial", 16, "bold"))
    mandel_fract = tk.Button(v_windows_settings, text="Mandelbrot",
                             command=lambda: fractal_change("mandelbrot"), font=("Arial", 16, "bold"))

    liste_fonc_fract = ttk.Combobox(v_windows_settings, values=fonctions_frac, justify='center',
                                    font=("Arial", 12, "bold"))
    liste_fonc_fract.current(0)
    liste_fonc_fract.bind("<<ComboboxSelected>>", action_fonct)

    save_button = tk.Button(v_windows_settings, text="Save", command=save_fonct, font=("Arial", 16, "bold"))
    close_button = tk.Button(v_windows_settings, text="Close", command=v_windows_settings.destroy,
                             font=("Arial", 16, "bold"))

    text_info_current.set("Current fractal : {}\n"
                  "Current fonction : {}".format(v_targ.capitalize(), fonctions_frac[v_fonct - 1]))
    text_info_current_print = tk.Label(v_windows_settings, textvariable=text_info_current, font=("Arial", 14))

    text_info_tosave.set("Fractal choosen : {} {}\n"
                         "Fonction choosen : {}".format(v_targ_temp.capitalize(), "" if is_saved else "*",
                                                        fonctions_frac[v_fonct_temp - 1]))

    text_info_tosave_print = tk.Label(v_windows_settings, textvariable=text_info_tosave, font=("Arial", 14))

    title_label.pack(pady=20, side=tk.TOP)
    julia_fract.pack(pady=5)
    mandel_fract.pack(pady=5)
    liste_fonc_fract.pack(pady=5)
    text_info_current_print.pack(pady=10, side=tk.RIGHT)
    text_info_tosave_print.pack(pady=10, side=tk.LEFT)
    close_button.pack(pady=10, side=tk.BOTTOM)
    save_button.pack(pady=10, side=tk.BOTTOM)


def windows_menu():
    v_windows_menu = tk.Tk()
    v_windows_menu.title("Menu")

    screen_width = v_windows_menu.winfo_screenwidth()
    screen_height = v_windows_menu.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    v_windows_menu.geometry(f"{window_width}x{window_height}+{x}+{y}")

    title_label = tk.Label(v_windows_menu, text="Fractal", font=("Arial", 24, "bold"))

    play_button = tk.Button(v_windows_menu, text="Play", command=fractal, font=("Arial", 16, "bold"))

    fonct_button = tk.Button(v_windows_menu, text="Change Function", command=window_settings,
                             font=("Arial", 16, "bold"))

    quit_button = tk.Button(v_windows_menu, text="Quit", command=v_windows_menu.destroy, font=("Arial", 16, "bold"))

    title_label.pack(pady=20, side=tk.TOP)
    play_button.pack(pady=10)
    fonct_button.pack(pady=10)
    quit_button.pack(pady=10, side=tk.BOTTOM)

    v_windows_menu.mainloop()


if __name__ == "__main__":
    windows_menu()
    pygame.quit()
