# ============================================================
#  GLADIATOR ARENA - Main Entry Point
# ============================================================
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from settings import SCREEN_W, SCREEN_H, FPS, TITLE


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(TITLE)

    # Try to set icon color (no external file needed)
    icon = pygame.Surface((32, 32))
    icon.fill((180, 110, 40))
    pygame.draw.circle(icon, (212, 175, 55), (16, 16), 14)
    pygame.display.set_icon(icon)

    try:
        from game import Game
        game = Game(screen)
        game.run()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print('Unhandled exception:\n', tb)
        try:
            with open('error.log', 'w', encoding='utf-8') as f:
                f.write(tb)
        except Exception:
            pass
        raise


if __name__ == '__main__':
    main()
