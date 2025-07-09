# show_goal_message.py
import pygame

def show_goal_message(font, screen, text_color, width, height):
    msg_surface = font.render("Congratulations!", True, text_color)
    msg_rect = msg_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(msg_surface, msg_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False