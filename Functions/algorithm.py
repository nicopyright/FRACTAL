import pygame
from Class.Complex import *
from Functions.conversion import *

v_color_mod = 50

def divergence(z: Complex(), w: Complex) -> [bool, int]:
    """
    Verify if the coordinates diverge with the equation z² + w
    :param z: complex for each coordinates
    :param w: complex number for the Julia set
    :return: [bool, int]
    """
    # Create 2 lists to compare
    t_reel = []
    t_imaginary = []

    # Initial conditions
    velocity = 2  # Divergence velocity to put colors
    z = z * z + w
    t_reel.append(z.re)
    t_imaginary.append(z.im)
    z = z * z + w
    t_reel.append(z.re)
    t_imaginary.append(z.im)

    # Verify if the coordonate diverge
    for i in range(2, 50):
        velocity += 1
        z = z * z + w
        t_reel.append(z.re)
        t_imaginary.append(z.im)

        # Verify if the equation diverge
        if t_reel[i] >= 10 or t_imaginary[i] >= 10 or t_reel[i] <= -10 or t_imaginary[i] <= -10:
            return [False, velocity]

        # Verify if the equation loop
        elif t_reel[i - 2] == t_reel[i] and t_imaginary[i - 2] == t_imaginary[i]:
            return [True, velocity]

    return [True, velocity]


def julia(surface: [pygame.Surface, pygame.SurfaceType],
          x0: int, y0: int, x1: int, y1: int,
          w: Complex = Complex(-1.0, 0.0),
          offset_x: float = 0., offset_y: float = 0.,
          zoom: float = 300.) -> None:
    """
    Display the Julia set linked to w on a rectangle with (x0,y0) on the top left coordinates
    and (x1,y1) on the bottom right coordinates

    :param surface: Pygame surface on which to display the fractal
    :param x0: x of the top left coordinates
    :param y0: y of the top left coordinates
    :param x1: x of the bottom right coordinates
    :param y1: y of the bottom right coordinates
    :param w: complex number for the Julia set
    :param offset_x: offset on x-axis
    :param offset_y: offset on y-axis
    :param zoom: value of the zoom
    """
    inversion_i = False
    inversion_j = False

    # maintains the integrity of the for i loop no matter if x0>x1
    if x0 > x1:
        inversion_i = True
        x0, x1 = x1, x0

    # maintains the integrity of the for j loop no matter if y0>y1
    if y0 > y1:
        inversion_j = True
        y0, y1 = y1, y0

    # Two for loops to display the fractal
    for i in range(x0, x1 + 1):

        # also maintains the integrity of the for i loop
        if inversion_i:
            i = x1 - i + x0

        for j in range(y0, y1 + 1):

            # also maintains the integrity of the for j loop
            if inversion_j:
                j = y1 - j + y0

            # place the fractal according to the zoom and the offsets
            z = Complex(i / zoom + offset_x, j / zoom + offset_y)

            # Use the function divergence() to display the right color one the screen
            div = divergence(z, w)
            if div[0]:

                pygame.draw.line(surface,
                                 (((v_color_mod-div[1])*255/v_color_mod, (v_color_mod-div[1])*128/v_color_mod, 255)),
                                 complex_plan_to_screen((i, j)), complex_plan_to_screen((i, j)))
            else:
                pygame.draw.line(surface,
                                 ((255-div[1]**2)%255, (255-div[1]**2)%255, (255-div[1]**2)%255),
                                 complex_plan_to_screen((i, j)), complex_plan_to_screen((i, j)))

            pygame.display.flip()


def mandelbrot(surface, x0, y0, x1, y1, offset_x: float = 0., offset_y: float = 0., zoom: float = 300.):
    """
        Display the Mandelbrot set linked to w on a rectangle with (x0,y0) on the top left coordinates
        and (x1,y1) on the bottom right coordinates

        :param surface: Pygame surface on which to display the fractal
        :param x0: x of the top left coordinates
        :param y0: y of the top left coordinates
        :param x1: x of the bottom right coordinates
        :param y1: y of the bottom right coordinates
        :param offset_x: offset on x-axis
        :param offset_y: offset on y-axis
        :param zoom: value of the zoom
        """
    zero = Complex(0.0, 0.0)
    invi = False
    invj = False
    if x0 > x1:
        invi = True
        x0,x1 = x1,x0
    if y0 > y1:
        invj = True
        y0,y1 = y1,y0
    for i in range(x0, x1 + 1):
        if invi:
            i = x1 - i + x0

        for j in range(y0, y1 + 1):
            if invj:
                j = y1 - j + y0
            z = Complex(i / zoom + offset_x, j / zoom + offset_y)
            div = divergence(zero, z)

            if divergence(zero,z)[0]:
                pygame.draw.line(
                    surface,
                    (((v_color_mod-div[1])*255/v_color_mod, (v_color_mod-div[1])*128/v_color_mod, 255)),
                    complex_plan_to_screen((i, j)), complex_plan_to_screen((i, j)))

            elif not divergence(zero,z)[0]:
                pygame.draw.line(
                    surface,
                    ((255-div[1]**2)%255, (255-div[1]**2)%255, (255-div[1]**2)%255),
                    complex_plan_to_screen((i, j)), complex_plan_to_screen((i, j)))

            pygame.display.flip()




