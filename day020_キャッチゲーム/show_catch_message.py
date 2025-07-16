# show_catch_message.py
### LUGACY MODULE ###
import pygame

def show_catch_message(font, screen, text_color, width, height):
    msg_surface = font.render("Catch!", True, text_color)
    msg_rect = msg_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(msg_surface, msg_rect)
    pygame.display.flip()
    pygame.time.delay(500)

def show_miss_message(font, screen, text_color, width, height):
    msg_surface = font.render("Miss!", True, text_color)
    msg_rect = msg_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(msg_surface, msg_rect)
    pygame.display.flip()
    pygame.time.delay(500)