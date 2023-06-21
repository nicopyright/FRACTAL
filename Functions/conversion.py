import pygame

def f_tuples_add(A: tuple, B: tuple) -> tuple:
    """
    :return: A tuple as a result of the addition of tuples A and B coordinates by coordinates
    """
    return A[0] + B[0], A[1] + B[1]


def f_complex_plan_to_screen(coord: tuple) -> tuple:
    """
    :param coord: Coordinates on a plane to display on the screen
    :return: Coordinates of the screen for pygame
    """
    screen_size = pygame.display.Info()
    screen_width = screen_size.current_w
    screen_height = screen_size.current_h
    center = (screen_width // 2, screen_height // 2)
    return f_tuples_add(center, coord)


def f_screen_to_complex_plan(coord: tuple) -> tuple:
    """
    :param coord: Coordinates of the screen to convert to the plan
    :return: coordinates of the plan for calculus
    """
    screen_size = pygame.display.Info()
    screen_width = screen_size.current_w
    screen_height = screen_size.current_h
    center = (-screen_width // 2, -screen_height // 2)
    return f_tuples_add(center, coord)
