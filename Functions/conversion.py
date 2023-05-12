def tuples_add(A: tuple, B: tuple) -> tuple:
    """
    :return: A tuple as a result of the addition of tuples A and B coordinates by coordinates
    """
    return A[0] + B[0], A[1] + B[1]


def complex_plane_to_screen(coord: tuple) -> tuple:
    """
    :param coord: Coordinates on a plane to display on the screen
    :return: Coordinates of the screen for pygame
    """
    screen_size = pygame.display.Info()
    screen_width = screen_size.current_w
    screen_height = screen_size.current_h
    center = (screen_width // 2, screen_height // 2)
    return tuples_add(center, coord)


def screen_to_complex_plane(coord: tuple) -> tuple:
    """
    :param coord: Coordinates of the screen to convert to the plane
    :return: coordinates of the plane for calculus
    """
    screen_size = pygame.display.Info()
    screen_width = screen_size.current_w
    screen_height = screen_size.current_h
    center = (-screen_width // 2, -screen_height // 2)
    return tuples_add(center, coord)

