import pygame
from Models.SliderWidget import *

def f_center_x(surface:pygame.Surface, image:pygame.Surface) -> int:
    """
    Return x coordinate to center an image on a surface
    :param surface: Pygame surface where the image is blit
    :param image: Pygame image to blit
    :return: x coordinate to center an image on a surface
    """
    return surface.get_width()//2-image.get_width()//2


def f_resize(image:pygame.Surface, mult:float):
    """

    :param image:
    :param mult:
    :return:
    """
    return (image.get_width()*mult, image.get_height()*mult)

def slider_function(arg_width: int, arg_height: int, arg_zoom_initial: int, arg_re_w: float, arg_im_w: float) \
        -> (int, int, int, float, float):
    """
    :param arg_width: width parameter to update
    :param arg_height: height parameter to update
    :param arg_zoom_initial: zoom parameter to update
    :param arg_re_w: reel part of w parameter to update
    :param arg_im_w: imaginary part of w parameter to update
    :return:
    """
    def button_pressed():
        """
        Call the confirm method for each slider to update their return values
        :return arg_width, arg_height, arg_zoom_initial, arg_re_w, arg_im_w
        """
        for slider in sliders:
            slider.confirm()
            slider.state = True

    def on_closing(state: bool):
        """
        Check if any slider's state is False and prompt a confirmation message box
        :param state: boolean
        """
        for slider in sliders:
            state *= slider.state
        if not state:
            result = messagebox.askyesno("Confirmation", "Do you want to apply the new parameters ?")
        else:
            result = True

        if result:
            button_pressed()
            parameter_window.destroy()
        else:
            parameter_window.destroy()

    parameter_window = tk.Tk()
    state = True
    sliders = [SliderWidget(parameter_window, "width", 0, 1920, 1, arg_width, 0, 0),
               SliderWidget(parameter_window, "height", 0, 1080, 1, arg_height, 1, 0),
               SliderWidget(parameter_window, arg_title="initial zoom", arg_min=0, arg_max=1000, arg_resolution=1,
                            arg_initial_value=arg_zoom_initial,
                            arg_row=2, arg_column=0),
               SliderWidget(arg_window=parameter_window, arg_title="reel part of the constant complex", arg_min=-10, arg_max=10,
                            arg_resolution=0.001, arg_initial_value=arg_re_w,
                            arg_row=3, arg_column=0),
               SliderWidget(arg_window=parameter_window, arg_title="imaginary part of the constant complex", arg_min=-10, arg_max=10,
                            arg_resolution=0.001, arg_initial_value=arg_im_w,
                            arg_row=4, arg_column=0)
               ]

    # Create SliderWidget objects for different parameters
    for slider in sliders:
        # Create the sliders in the GUI
        slider.create()

    # Create a button to apply the new parameters
    button = tk.Button(parameter_window, text="apply", command=lambda: button_pressed(), font=("Arial", 12, "bold"))
    button.grid(row=5, column=0)

    parameter_window.protocol("WM_DELETE_WINDOW", func=lambda: on_closing(state))

    parameter_window.mainloop()

    # Get the return values from the sliders
    arg_width = sliders[0].return_value
    arg_height = sliders[1].return_value
    arg_zoom_initial = sliders[2].return_value
    arg_re_w = sliders[3].return_value
    arg_im_w = sliders[4].return_value

    return arg_width, arg_height, arg_zoom_initial, arg_re_w, arg_im_w
