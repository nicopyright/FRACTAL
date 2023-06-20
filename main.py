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
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path

"""
v_ : variable
l_ : list
b_ : bool
arg_ : function argument
tkd_ : tkinter window
tkl_ : tkinter label
tkb_ : tkinter button
tksv_ : tkinter StringVar()
tkcb_ : tkinter combobox
"""

# Global variables
v_targ = "julia"
v_targ_temp = v_targ
v_fonct = 1
v_fonct_temp = v_fonct
l_sequence = ["z² + w", "cos(z) + w"]
b_is_saved = True

# Create the directories for the captures if they don't exist
Path(".\Capture_For_Video").mkdir(parents=True, exist_ok=True)
Path(".\Capture").mkdir(parents=True, exist_ok=True)


def f_fractal_change(arg_name: str):
    """
    Choose the fractal to use between 'julia' or 'mandelbrot'
    :param arg_name: fractal name
    """
    global v_targ_temp, b_is_saved
    b_is_saved = False if arg_name != v_targ else True
    v_targ_temp = arg_name
    print("targ_temp : ", v_targ_temp)
    tksv_text_info_tosave.set("Fractal choosen : {} {}\n"
                              "Sequence choosen : {}".format(v_targ_temp.capitalize(), "" if b_is_saved else "*",
                                                             l_sequence[v_fonct_temp - 1]))


def f_action_sequence(event):
    """
    Change sequence
    :param event:
    :return:
    """
    global v_fonct_temp, b_is_saved
    v_choice = tkcb_sequence_list.get()
    print("Fonc_temp : ", v_choice)
    if v_choice == "z² + w":
        v_fonct_temp = 1
        b_is_saved = False if v_fonct_temp != v_fonct else True
    elif v_choice == "cos(z) + w":
        v_fonct_temp = 2
        b_is_saved = False if v_fonct_temp != v_fonct else True
    print("is_saved : ", b_is_saved)
    tksv_text_info_tosave.set("Fractal choosen : {} {}\n"
                              "Sequence choosen : {}".format(v_targ_temp.capitalize(), "" if b_is_saved else "*",
                                                             l_sequence[v_fonct_temp - 1]))


def f_save():
    """
    Save new settings
    """
    global v_targ, v_fonct, b_is_saved
    v_targ = v_targ_temp
    v_fonct = v_fonct_temp
    b_is_saved = True
    tksv_text_info_current.set("Current fractal : {}\n"
                               "Current fonction : {}".format(v_targ.capitalize(), l_sequence[v_fonct - 1]))
    tksv_text_info_tosave.set("Fractal choosen : {} {}\n"
                              "Sequence choosen : {}".format(v_targ_temp.capitalize(), "" if b_is_saved else "*",
                                                             l_sequence[v_fonct_temp - 1]))
    print("Current fractal : {}".format(v_targ))
    print("Current fonction : {}".format(v_fonct))
    print("is_saved : ", b_is_saved)


def f_fractal():
    """
    Fonction who starts fractal's window
    """
    pygame.init()
    # collect screen's information
    v_screen_size = pygame.display.Info()
    v_screen_width = v_screen_size.current_w
    v_screen_height = v_screen_size.current_h
    print(v_screen_width, v_screen_height)

    v_w = Complex(-1, 0)
    v_width = int(v_screen_width // 2)
    v_height = int(v_screen_height // 2)
    v_zoom_initial = 50
    v_spreadX = cpu_count() * 2
    v_spreadY = cpu_count() * 2

    v_background = "white"

    tkw_window = pygame.display.set_mode((v_width, v_height), pygame.RESIZABLE)
    b_cont = True
    v_zoom = v_zoom_initial
    tkw_window.fill(v_background)

    l_mouse_x = [0.0] * 500
    l_mouse_y = [0.0] * 500
    v_k = 0

    v_start = time.time()
    f_multithreading(tkw_window, v_width, v_height, v_spreadX, v_spreadY, l_mouse_x[v_k], l_mouse_y[v_k], v_zoom, v_targ,
                     v_w, v_fonct)
    v_end = time.time()
    print(v_end - v_start)

    # main loop
    while b_cont:
        # gather inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                b_cont = False
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    b_cont = False
                    pygame.quit()
                # if s key is pressed it takes a screenshot and stock it into Capture file
                if event.key == pygame.K_s:
                    path = new_path(".png", "Capture")
                    pygame.image.save(tkw_window, path)

                if event.key == pygame.K_e:
                    encode('.\Capture_For_Video\*.png', '.\Videos\project.avi', 3)

            elif event.type == pygame.VIDEORESIZE:
                v_height = event.h
                v_width = event.w
                tkw_window.fill(v_background)
                v_start = time.time()
                f_multithreading(tkw_window, v_width, v_height, v_spreadX, v_spreadY, l_mouse_x[v_k], l_mouse_y[v_k],
                                 v_zoom,
                                 v_targ, v_w, v_fonct)
                v_end = time.time()
                print(v_end - v_start)

            elif pygame.mouse.get_pressed()[0]:
                tkw_window.fill("white")
                v_screen_position = f_screen_to_complex_plan(pygame.mouse.get_pos())
                v_k += 1
                l_mouse_x[v_k] = l_mouse_x[v_k - 1] + v_screen_position[0] / v_zoom
                l_mouse_y[v_k] = l_mouse_y[v_k - 1] + v_screen_position[1] / v_zoom
                v_zoom *= 1.5
                v_start = time.time()
                f_multithreading(tkw_window, v_width, v_height, v_spreadX, v_spreadY, l_mouse_x[v_k], l_mouse_y[v_k],
                                 v_zoom,
                                 v_targ, v_w, v_fonct)
                v_end = time.time()
                print(v_end - v_start)
                pygame.display.flip()
                v_title = "cap{}.png".format(v_k)
                pygame.image.save(tkw_window, "Capture_For_Video\{}".format(v_title))

            # if right click is pressed a video is recorded
            elif pygame.mouse.get_pressed()[2]:
                tkw_window.fill("white")
                v_screen_position = f_screen_to_complex_plan(pygame.mouse.get_pos())
                v_start = time.time()
                for i in range(0, 100):
                    v_zoom *= 1.05
                    f_multithreading(tkw_window, v_width, v_height, v_spreadX, v_spreadY,
                                     (v_screen_position[0]) / v_zoom_initial, (v_screen_position[1]) / v_zoom_initial,
                                     v_zoom, v_targ, v_w, v_fonct)
                    print(i)
                    v_title = "cap{}.png".format(i)
                    pygame.image.save(tkw_window, "Capture_For_Video\{}".format(v_title))

                v_end = time.time()
                print("total time: {}".format(v_end - v_start))
                encode('.\Capture_For_Video\*.png', '.\Videos\project.avi', 10)


def f_window_settings():
    """
    Fonction who starts setting's windows
    """
    global tkcb_sequence_list, tksv_text_info_current, tksv_text_info_tosave, b_is_saved

    v_windows_settings = tk.Tk()

    v_windows_settings.title("Settings")
    tksv_text_info_current = tk.StringVar(v_windows_settings)
    tksv_text_info_tosave = tk.StringVar(v_windows_settings)
    screen_width = v_windows_settings.winfo_screenwidth()

    screen_height = v_windows_settings.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    v_x = (screen_width - window_width) // 2
    v_y = (screen_height - window_height) // 2
    v_windows_settings.geometry(f"{window_width}x{window_height}+{v_x}+{v_y}")

    tkl_title_label = tk.Label(v_windows_settings, text="Settings", font=("Arial", 24, "bold"))

    tkb_julia_fract = tk.Button(v_windows_settings, text="Julia",
                                command=lambda: f_fractal_change("julia"), font=("Arial", 16, "bold"))
    tkb_mandel_fract = tk.Button(v_windows_settings, text="Mandelbrot",
                                 command=lambda: f_fractal_change("mandelbrot"), font=("Arial", 16, "bold"))

    tkcb_sequence_list = ttk.Combobox(v_windows_settings, values=l_sequence, justify='center',
                                      font=("Arial", 12, "bold"))
    tkcb_sequence_list.current(0)
    tkcb_sequence_list.bind("<<ComboboxSelected>>", f_action_sequence)

    tkb_save_button = tk.Button(v_windows_settings, text="Save", command=f_save, font=("Arial", 16, "bold"))
    tkb_close_button = tk.Button(v_windows_settings, text="Close",
                                 command=v_windows_settings.destroy, font=("Arial", 16, "bold"))

    tksv_text_info_current.set("Current fractal : {}\n"
                               "Current fonction : {}".format(v_targ.capitalize(), l_sequence[v_fonct - 1]))
    tkl_text_info_current_print = tk.Label(v_windows_settings, textvariable=tksv_text_info_current, font=("Arial", 14))

    tksv_text_info_tosave.set("Fractal choosen : {} {}\n"
                              "Sequence choosen : {}".format(v_targ_temp.capitalize(), "" if b_is_saved else "*",
                                                             l_sequence[v_fonct_temp - 1]))

    tkl_text_info_tosave_print = tk.Label(v_windows_settings, textvariable=tksv_text_info_tosave, font=("Arial", 14))

    tkl_title_label.pack(pady=20, side=tk.TOP)
    tkb_julia_fract.pack(pady=5)
    tkb_mandel_fract.pack(pady=5)
    tkcb_sequence_list.pack(pady=5)
    tkl_text_info_current_print.pack(pady=10, side=tk.RIGHT)
    tkl_text_info_tosave_print.pack(pady=10, side=tk.LEFT)
    tkb_close_button.pack(pady=10, side=tk.BOTTOM)
    tkb_save_button.pack(pady=10, side=tk.BOTTOM)


def f_windows_menu():
    """
    Fonction who starts menu's window
    """
    v_windows_menu = tk.Tk()
    v_windows_menu.title("Menu")

    screen_width = v_windows_menu.winfo_screenwidth()
    screen_height = v_windows_menu.winfo_screenheight()
    window_width = screen_width // 2
    window_height = screen_height // 2
    v_x = (screen_width - window_width) // 2
    v_y = (screen_height - window_height) // 2
    v_windows_menu.geometry(f"{window_width}x{window_height}+{v_x}+{v_y}")

    tkl_title = tk.Label(v_windows_menu, text="Fractal", font=("Arial", 24, "bold"))

    tkb_play = tk.Button(v_windows_menu, text="Play", command=f_fractal, font=("Arial", 16, "bold"))

    tkb_sequence = tk.Button(v_windows_menu, text="Change sequence", command=f_window_settings,
                             font=("Arial", 16, "bold"))

    tkb_quit = tk.Button(v_windows_menu, text="Quit", command=v_windows_menu.destroy, font=("Arial", 16, "bold"))

    tkl_title.pack(pady=20, side=tk.TOP)
    tkb_play.pack(pady=10)
    tkb_sequence.pack(pady=10)
    tkb_quit.pack(pady=10, side=tk.BOTTOM)

    v_windows_menu.mainloop()


if __name__ == "__main__":
    f_windows_menu()
    pygame.quit()
