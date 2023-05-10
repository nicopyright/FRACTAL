# Import  libraries
import pygame

pygame.init()


# collect screen's informations
v_screen_size = pygame.display.Info()
v_screen_width = v_screen_size.current_w
v_screen_height = v_screen_size.current_h

# define the center of the screen
v_center = (v_screen_width // 2, v_screen_height // 2)


def main():
    """
    main fonction
    """

    v_window = pygame.display.set_mode((v_screen_width // 2, v_screen_height // 2), pygame.RESIZABLE)
    v_window.fill("white")

    v_cont = True

    # main loop
    while v_cont:

        # gather inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                v_cont = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    v_cont = False


        # refresh display
        pygame.display.flip()

    pygame.quit()


main()
