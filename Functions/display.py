import pygame

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