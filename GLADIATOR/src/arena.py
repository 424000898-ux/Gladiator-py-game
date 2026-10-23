# ============================================================
#  GLADIATOR ARENA - Arena System
# ============================================================
import pygame, math, random
from settings import *
from src.ui import draw_panel, draw_text, Button


class Arena:
    def __init__(self, screen_w, screen_h):
        self.sw = screen_w
        self.sh = screen_h
        self.t  = 0.0
        self.current_tier = 0
        self.wins_in_tier  = 0
        self.wins_needed   = 3
        self.btn_fight  = Button(screen_w//2-120, screen_h-80, 240, 50,
                                  'ENTER THE ARENA!', 24,
                                  color=(150,30,30), hover_color=(220,50,50))
        self.btn_back   = Button(20, screen_h-70, 130, 44, 'BACK', 20,
                                  color=BRONZE_DK, hover_color=BRONZE)

    def update(self, dt, mouse_pos):
        self.t += dt
        self.btn_fight.update(dt, mouse_pos)
        self.btn_back.update(dt, mouse_pos)

    def handle_event(self, event):
        if self.btn_back.is_clicked(event):
            return 'back'
        if self.btn_fight.is_clicked(event):
            return 'fight'
        return None

    def get_current_tier(self, player):
        tier = 0
        for i, t in enumerate(ARENA_TIERS):
            if player.arena_rank >= t['min_rank']:
                tier = i
        return tier

    def pick_enemy_type(self, player):
        tier = self.get_current_tier(player)
        pool = ARENA_TIERS[tier]['enemy_pool']
        return random.choice(pool)

    def draw(self, surface, player):
        # Draw arena background
        self._draw_arena_banner(surface, player)

        pw, ph = 700, 420
        panel_r = pygame.Rect(self.sw//2-pw//2, self.sh//2-ph//2-20, pw, ph)
        draw_panel(surface, panel_r, color=STONE, border=GOLD)

        draw_text(surface, 'COLOSSEUM RANKINGS', self.sw//2,
                  panel_r.y+14, 32, GOLD, bold=True, center=True)

        # Tier ladder
        for i, tier in enumerate(ARENA_TIERS):
            ty = panel_r.y + 70 + i * 70
            current = (i == self.get_current_tier(player))
            unlocked= (player.arena_rank >= tier['min_rank'])

            col = GOLD if current else (PARCHMENT if unlocked else GRAY)
            marker = '► ' if current else ('  ' if unlocked else '🔒 ')
            bg = BRONZE_DK if current else STONE

            tr = pygame.Rect(panel_r.x+20, ty, pw-40, 55)
            draw_panel(surface, tr, color=bg, border=GOLD if current else BRONZE)

            draw_text(surface, f'{marker}{tier["name"]}',
                      tr.x+15, tr.y+8, 20, col, bold=current)
            draw_text(surface, f'Min Rank: {tier["min_rank"]}',
                      tr.x+15, tr.y+28, 14, STONE_LT)
            draw_text(surface, f'Crowd: {tier["crowd_size"]:,}',
                      tr.right-160, tr.y+8, 14, PARCHMENT)
            draw_text(surface, f'Enemies: {", ".join(set(tier["enemy_pool"]))}',
                      tr.right-160, tr.y+28, 13, STONE_LT)

        # Player stats
        sx = panel_r.x + 20
        sy = panel_r.bottom - 50
        draw_text(surface, f'Rank: #{player.arena_rank}', sx, sy, 17, GOLD, bold=True)
        draw_text(surface, f'Wins: {player.wins}', sx+130, sy, 17, GREEN, bold=True)
        draw_text(surface, f'Losses: {player.losses}', sx+250, sy, 17, RED, bold=True)
        draw_text(surface, f'Kills: {player.kills}', sx+380, sy, 17, ORANGE, bold=True)

        self.btn_fight.draw(surface)
        self.btn_back.draw(surface)

    def _draw_arena_banner(self, surface, player):
        t = self.t
        w, h = self.sw, self.sh
        # Dark overlay
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0,0,0,140))
        surface.blit(overlay, (0,0))
        # Title banner
        bw, bh = 600, 80
        bx = w//2 - bw//2
        by = 10
        # Animated shine
        shine = int((math.sin(t*2)+1)*0.5 * 40)
        draw_panel(surface, pygame.Rect(bx, by, bw, bh), color=BRONZE_DK, border=GOLD)
        draw_text(surface, 'GLADIATOR ARENA', w//2, by+12, 38, GOLD, bold=True, center=True)
        draw_text(surface, '— Choose your destiny —', w//2, by+50, 18, PARCHMENT, center=True)
