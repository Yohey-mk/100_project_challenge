# game_over.py
import pygame

def game_over(font, screen, text_color, width):


    waiting = True
    while waiting:
        msg_surface = font.render("GAME OVER", True, text_color)
        msg_rect = msg_surface.get_rect(center=(width // 2, 100))
        screen.blit(msg_surface, msg_rect)
        
        sub_msg1 = font.render("Press Space to retry", True, text_color)
        sub_rect1 = sub_msg1.get_rect(center=(width // 2, 150))
        sub_msg2 = font.render("Any key to quit", True, text_color)
        sub_rect2 = sub_msg2.get_rect(center=(width // 2, 190))

        screen.blit(sub_msg1, sub_rect1)
        screen.blit(sub_msg2, sub_rect2)
        
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                else:
                    return False
            elif event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return False #ここでゲーム再開orQUITを選べるようにしたい
