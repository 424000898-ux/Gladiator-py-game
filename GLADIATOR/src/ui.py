# ============================================================
#  GLADIATOR ARENA - UI System
# ============================================================
import pygame, math, random, os
from settings import *


# ── Fonts ────────────────────────────────────────────────────
_fonts = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        try:
            _fonts[key] = pygame.font.Font(None, size)
        except Exception:
            _fonts[key] = pygame.font.SysFont('arial', size, bold=bold)
    return _fonts[key]


# ── Item icon loader ───────────────────────────────────────
_icon_cache = {}
def load_icon(name, size=None):
    """Load and cache an item icon by item name. Size is (w,h) or int for max dimension.
    Returns a pygame.Surface or None."""
    if not name:
        return None
    key = (name, size)
    if key in _icon_cache:
        return _icon_cache[key]
    # sanitize name to filename
    fn = name.lower().replace(' ', '_').replace("'", '').replace('-', '_') + '.png'
    base = os.path.join(os.path.dirname(__file__), '..', 'assets')
    path = os.path.normpath(os.path.join(base, fn))
    img = None
    try:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            if size:
                iw, ih = img.get_size()
                if isinstance(size, int):
                    maxd = max(1, size)
                    scale = maxd / max(iw, ih)
                    img = pygame.transform.smoothscale(img, (int(iw*scale), int(ih*scale)))
                else:
                    sw, sh = size
                    # scale to fit within box
                    scale = min(sw / max(1, iw), sh / max(1, ih))
                    img = pygame.transform.smoothscale(img, (max(1,int(iw*scale)), max(1,int(ih*scale))))
    except Exception:
        img = None
    _icon_cache[key] = img
    return img


# ── Drawing Helpers ──────────────────────────────────────────

def draw_text(surface, text, x, y, size=20, color=WHITE, bold=False,
              center=False, shadow=True):
    font = get_font(size, bold)
    if shadow:
        s = font.render(str(text), True, (0,0,0,180))
        if center:
            surface.blit(s, (x - s.get_width()//2 + 2, y+2))
        else:
            surface.blit(s, (x+2, y+2))
    s = font.render(str(text), True, color)
    if center:
        surface.blit(s, (x - s.get_width()//2, y))
    else:
        surface.blit(s, (x, y))
    return s.get_width()


def draw_panel(surface, rect, color=STONE, border=BRONZE, radius=8, alpha=220):
    """Rounded stone panel with bronze border."""
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0,0,rect.width,rect.height), border_radius=radius)
    pygame.draw.rect(s, (*border, 255), (0,0,rect.width,rect.height), 3, border_radius=radius)
    # Inner highlight
    pygame.draw.rect(s, (*STONE_LT, 60), (2,2,rect.width-4,rect.height-4), 1, border_radius=radius-1)
    surface.blit(s, rect.topleft)


def draw_bar(surface, x, y, w, h, value, max_val, color, bg=(30,10,10), label='', border=BRONZE):
    ratio = max(0, min(1, value/max(max_val,1)))
    # Background
    pygame.draw.rect(surface, bg, (x, y, w, h), border_radius=4)
    # Fill
    fw = int(w * ratio)
    if fw > 0:
        # Gradient effect
        pygame.draw.rect(surface, color, (x, y, fw, h), border_radius=4)
        # Shine
        shine = (min(color[0]+60,255), min(color[1]+60,255), min(color[2]+60,255))
        pygame.draw.rect(surface, shine, (x, y, fw, h//3), border_radius=4)
    # Border
    pygame.draw.rect(surface, border, (x, y, w, h), 2, border_radius=4)
    # Label
    if label:
        draw_text(surface, label, x + w//2, y + h//2 - 7, 14, WHITE, center=True, shadow=True)

def draw_damage_number(surface, text, x, y, color=WHITE, size=28):
    draw_text(surface, str(text), x, y, size, color, bold=True, center=True)


# ── Button ───────────────────────────────────────────────────

class Button:
    def __init__(self, x, y, w, h, text, font_size=22,
                 color=BRONZE, hover_color=GOLD, text_color=WHITE,
                 border_color=GOLD, icon=None, icon_size=None):
        self.rect        = pygame.Rect(x, y, w, h)
        self.text        = text
        self.font_size   = font_size
        self.color       = color
        self.hover_color = hover_color
        self.text_color  = text_color
        self.border_color= border_color
        self.icon        = icon
        self.icon_size   = icon_size
        self._hovered    = False
        self._hover_t    = 0.0
        self.enabled     = True
        self.pulse_t     = 0.0

    def update(self, dt, mouse_pos):
        was = self._hovered
        self._hovered = self.rect.collidepoint(mouse_pos) and self.enabled
        if self._hovered:
            self._hover_t = min(self._hover_t + dt * 6, 1.0)
        else:
            self._hover_t = max(self._hover_t - dt * 6, 0.0)
        self.pulse_t += dt

    def draw(self, surface):
        t = self._hover_t
        # Color blend
        cr = int(self.color[0] + (self.hover_color[0]-self.color[0])*t)
        cg = int(self.color[1] + (self.hover_color[1]-self.color[1])*t)
        cb = int(self.color[2] + (self.hover_color[2]-self.color[2])*t)
        pulse = math.sin(self.pulse_t * 3) * 0.05 * t
        w = int(self.rect.width  * (1 + pulse))
        h = int(self.rect.height * (1 + pulse))
        cx = self.rect.centerx
        cy = self.rect.centery
        r = pygame.Rect(cx-w//2, cy-h//2, w, h)

        # Shadow
        sr = r.move(4,4)
        s = pygame.Surface((sr.width, sr.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0,0,0,100), (0,0,sr.width,sr.height), border_radius=8)
        surface.blit(s, sr.topleft)

        # Body
        s2 = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        pygame.draw.rect(s2, (*((cr,cg,cb)), 255), (0,0,r.width,r.height), border_radius=8)
        surface.blit(s2, r.topleft)

        # Inner shading band for depth
        shade_color = (max(0, cr-24), max(0, cg-24), max(0, cb-24), 180)
        pygame.draw.rect(surface, shade_color, (r.x+4, r.y+4, r.width-8, r.height//3), border_radius=6)

        # Border outline
        bc = self.border_color if not self._hovered else GOLD_LT
        pygame.draw.rect(surface, bc, r, 3, border_radius=8)
        pygame.draw.rect(surface, BLACK, r, 1, border_radius=8)

        # Text + icon
        col = WHITE if self._hovered else self.text_color
        if self.icon:
            icon = self.icon
            if self.icon_size:
                icon = pygame.transform.smoothscale(icon, self.icon_size)
            iw, ih = icon.get_size()
            text_surface = get_font(self.font_size, True).render(self.text, True, col)
            total_w = iw + 8 + text_surface.get_width()
            icon_x = r.centerx - total_w//2
            icon_y = r.centery - ih//2
            surface.blit(icon, (icon_x, icon_y))
            surface.blit(text_surface, (icon_x + iw + 8, r.centery - text_surface.get_height()//2))
        else:
            draw_text(surface, self.text, r.centerx, r.centery - self.font_size//2,
                      self.font_size, col, bold=True, center=True)

    def is_clicked(self, event):
        if not self.enabled:
            return False
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


# ── Floating Damage Numbers ──────────────────────────────────

class FloatingText:
    def __init__(self, text, x, y, color=WHITE, size=28, duration=1.5):
        self.text     = str(text)
        self.x        = float(x)
        self.y        = float(y)
        self.vy       = -80.0
        self.color    = color
        self.size     = size
        self.life     = duration
        self.max_life = duration
        self.alpha    = 255

    def update(self, dt):
        self.life -= dt
        self.y    += self.vy * dt
        self.vy   += 40 * dt  # slow down
        self.alpha = int(255 * max(0, self.life / self.max_life))

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface):
        font = get_font(self.size, True)
        s    = font.render(self.text, True, self.color)
        s.set_alpha(self.alpha)
        # Shadow
        sh = font.render(self.text, True, BLACK)
        sh.set_alpha(self.alpha // 2)
        surface.blit(sh, (int(self.x) - s.get_width()//2 + 2, int(self.y)+2))
        surface.blit(s,  (int(self.x) - s.get_width()//2, int(self.y)))


class FloatingTextManager:
    def __init__(self):
        self.texts = []

    def add(self, text, x, y, color=WHITE, size=28, duration=1.5):
        self.texts.append(FloatingText(text, x, y, color, size, duration))

    def update(self, dt):
        for t in self.texts:
            t.update(dt)
        self.texts = [t for t in self.texts if t.alive]

    def draw(self, surface):
        for t in self.texts:
            t.draw(surface)


# ── Screen Effects ───────────────────────────────────────────

class ScreenEffects:
    def __init__(self):
        self.shake_x     = 0.0
        self.shake_y     = 0.0
        self.shake_timer = 0.0
        self.shake_mag   = 0.0
        self.flash_alpha = 0.0
        self.flash_color = WHITE
        self.freeze_timer= 0.0
        self.slowmo_timer= 0.0
        self.slowmo_scale= 1.0
        self.vignette_alpha = 0.0

    def shake(self, magnitude=10, duration=0.25):
        self.shake_mag   = magnitude
        self.shake_timer = duration

    def flash(self, color=WHITE, duration=0.15):
        self.flash_alpha = 255
        self.flash_color = color
        self.flash_dur   = duration
        self.flash_timer = 0.0

    def freeze(self, duration=0.08):
        self.freeze_timer = duration

    def slowmo(self, duration=0.5, scale=0.3):
        self.slowmo_timer = duration
        self.slowmo_scale = scale

    def vignette(self, alpha=180):
        self.vignette_alpha = alpha

    def update(self, dt):
        # Shake
        if self.shake_timer > 0:
            self.shake_timer -= dt
            import random
            t = self.shake_timer / max(self.shake_mag * 0.025, 0.001)
            self.shake_x = random.uniform(-self.shake_mag, self.shake_mag)
            self.shake_y = random.uniform(-self.shake_mag, self.shake_mag)
        else:
            self.shake_x = 0; self.shake_y = 0

        # Flash
        if hasattr(self, 'flash_timer'):
            self.flash_timer = getattr(self, 'flash_timer', 0) + dt
            dur = getattr(self, 'flash_dur', 0.15)
            self.flash_alpha = max(0, 255 * (1 - self.flash_timer / dur))

        # Freeze
        self.freeze_timer = max(0, self.freeze_timer - dt)

        # Slowmo
        if self.slowmo_timer > 0:
            self.slowmo_timer -= dt
        else:
            self.slowmo_scale = 1.0

        # Vignette fade
        self.vignette_alpha = max(0, self.vignette_alpha - dt * 80)

    @property
    def frozen(self):
        return self.freeze_timer > 0

    @property
    def time_scale(self):
        if self.slowmo_timer > 0:
            return self.slowmo_scale
        return 1.0

    def draw_overlay(self, surface):
        w, h = surface.get_size()
        # Flash
        if self.flash_alpha > 0:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((*self.flash_color, int(self.flash_alpha)))
            surface.blit(s, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Vignette
        if self.vignette_alpha > 0:
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            # Draw dark edges
            for i in range(40):
                alpha = int(self.vignette_alpha * (1 - i/40) * 0.06)
                pygame.draw.rect(s, (0,0,0,alpha), (i, i, w-i*2, h-i*2), 1)
            surface.blit(s, (0, 0))


# ── HUD ─────────────────────────────────────────────────────

class HUD:
    def __init__(self, screen_w, screen_h):
        self.sw = screen_w
        self.sh = screen_h
        self.combat_log  = []
        self.log_timer   = 0.0
        self.ftm         = FloatingTextManager()
        # display interpolation for smooth bars
        self._disp_hp = None
        self._disp_mp = None
        self._disp_enemy_hp = None
        self._delay_player_hp = None
        self._delay_enemy_hp = None

    def add_log(self, text, color=PARCHMENT):
        self.combat_log.insert(0, (text, color, 4.0))
        if len(self.combat_log) > 6:
            self.combat_log.pop()

    def update(self, dt):
        self.ftm.update(dt)
        self.combat_log = [(t, c, l-dt) for t,c,l in self.combat_log if l > 0]

    def draw_player_hud(self, surface, player):
        pw = 340; ph = 130
        panel_r = pygame.Rect(10, 10, pw, ph)
        draw_panel(surface, panel_r, color=STONE, border=BRONZE)
        draw_text(surface, f'{player.name}  Lv.{player.level}',
                  panel_r.x+12, panel_r.y+10, 18, GOLD, bold=True)
        draw_text(surface, player.class_name,
                  panel_r.x+12, panel_r.y+30, 14, PARCHMENT)

        if self._disp_hp is None:
            self._disp_hp = player.hp
        if self._disp_mp is None:
            self._disp_mp = player.mp
        if self._delay_player_hp is None:
            self._delay_player_hp = player.hp

        self._disp_hp += (player.hp - self._disp_hp) * 0.12
        self._disp_mp += (player.mp - self._disp_mp) * 0.12
        self._delay_player_hp += (player.hp - self._delay_player_hp) * 0.06

        def draw_health_bar(x, y, w, h, value, max_value, delay_value, color):
            bg = (30, 14, 14)
            pygame.draw.rect(surface, bg, (x, y, w, h), border_radius=6)
            delay_width = int(w * max(0, min(1, delay_value / max(max_value, 1))))
            if delay_width > 0:
                pygame.draw.rect(surface, (120, 20, 20), (x, y, delay_width, h), border_radius=6)
            fill_width = int(w * max(0, min(1, value / max(max_value, 1))))
            if fill_width > 0:
                pygame.draw.rect(surface, color, (x, y, fill_width, h), border_radius=6)
                shine = (min(color[0]+70,255), min(color[1]+70,255), min(color[2]+70,255))
                pygame.draw.rect(surface, shine, (x, y, fill_width, h//3), border_radius=6)
            pygame.draw.rect(surface, BRONZE, (x, y, w, h), 2, border_radius=6)

        draw_health_bar(panel_r.x+10, panel_r.y+54, pw-20, 20,
                        self._disp_hp, player.max_hp, self._delay_player_hp, (220, 40, 40))
        draw_text(surface, f'HP  {player.hp}/{player.max_hp}',
                  panel_r.x+16, panel_r.y+56, 14, WHITE)

        draw_health_bar(panel_r.x+10, panel_r.y+80, pw-20, 18,
                        self._disp_mp, player.max_mp, player.max_mp, (40, 80, 220))
        draw_text(surface, f'MP  {player.mp}/{player.max_mp}',
                  panel_r.x+16, panel_r.y+82, 14, WHITE)

        draw_bar(surface, panel_r.x+10, panel_r.y+104, pw-20, 14,
                 player.xp, player.xp_next, (60,200,60),
                 label=f'XP  {player.xp}/{player.xp_next}', border=DARK_GREEN)

        draw_text(surface, f'⚙ {player.inventory.gold}g',
                  panel_r.x + pw - 12, panel_r.y + 12, 16, GOLD,
                  bold=True, shadow=True)
        draw_text(surface, f'Rank #{player.arena_rank}',
                  panel_r.x + pw - 12, panel_r.y + 34, 14, BRONZE)

        status = []
        if player.raged:
            status.append(('Rage', (255, 120, 60)))
        if player.stunned:
            status.append(('Stun', (120, 180, 255)))
        for i, (label, color) in enumerate(status):
            icon_x = panel_r.x + 12 + i * 72
            icon_y = panel_r.y + ph - 26
            pygame.draw.circle(surface, color, (icon_x, icon_y), 8)
            draw_text(surface, label, icon_x + 16, icon_y - 8, 12, PARCHMENT, shadow=False)

    def draw_enemy_hud(self, surface, enemy):
        pw = 320; ph = 100
        panel_r = pygame.Rect(self.sw - pw - 10, 10, pw, ph)
        border_color = BLOOD if getattr(enemy, 'ai_type', '') == 'boss' else BRONZE
        panel_color = (90, 50, 50) if getattr(enemy, 'ai_type', '') == 'boss' else STONE
        draw_panel(surface, panel_r, color=panel_color, border=border_color)
        draw_text(surface, enemy.name,
                  panel_r.x+12, panel_r.y+10, 18, (220,80,80), bold=True)
        draw_text(surface, f'Level {enemy.level}',
                  panel_r.x+12, panel_r.y+30, 14, PARCHMENT)

        if self._disp_enemy_hp is None:
            self._disp_enemy_hp = enemy.hp
        if self._delay_enemy_hp is None:
            self._delay_enemy_hp = enemy.hp
        self._disp_enemy_hp += (enemy.hp - self._disp_enemy_hp) * 0.12
        self._delay_enemy_hp += (enemy.hp - self._delay_enemy_hp) * 0.05

        bg = (30, 14, 14)
        bar_x = panel_r.x + 10
        bar_y = panel_r.y + 48
        bar_w = pw - 20
        bar_h = 22
        pygame.draw.rect(surface, bg, (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        delay_width = int(bar_w * max(0, min(1, self._delay_enemy_hp / max(enemy.max_hp, 1))))
        if delay_width > 0:
            pygame.draw.rect(surface, (120, 20, 20), (bar_x, bar_y, delay_width, bar_h), border_radius=6)
        fill_width = int(bar_w * max(0, min(1, self._disp_enemy_hp / max(enemy.max_hp, 1))))
        if fill_width > 0:
            pygame.draw.rect(surface, (200, 30, 30), (bar_x, bar_y, fill_width, bar_h), border_radius=6)
            pygame.draw.rect(surface, (255, 120, 80), (bar_x, bar_y, fill_width, bar_h//3), border_radius=6)
        pygame.draw.rect(surface, border_color, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=6)
        draw_text(surface, f'HP  {enemy.hp}/{enemy.max_hp}',
                  bar_x+10, bar_y+2, 14, WHITE)

        status_text = 'BOSS' if getattr(enemy, 'ai_type', '') == 'boss' else 'ENEMY'
        draw_text(surface, status_text, panel_r.right-68, panel_r.y+10, 14, GOLD, bold=True)
        status_icons = []
        if getattr(enemy, 'stunned', False):
            status_icons.append(('STUN', (120, 180, 255)))
        if getattr(enemy, 'dodge_next', False):
            status_icons.append(('DODGE', (100, 255, 180)))
        for i, (label, color) in enumerate(status_icons):
            icon_x = panel_r.x + 12 + i * 72
            icon_y = panel_r.y + ph - 24
            pygame.draw.circle(surface, color, (icon_x, icon_y), 8)
            draw_text(surface, label, icon_x + 16, icon_y - 8, 12, PARCHMENT, shadow=False)

    def draw_combat_log(self, surface):
        lx = self.sw//2 - 220
        ly = self.sh - 200
        for i, (text, color, life) in enumerate(self.combat_log):
            alpha = min(255, int(255 * life / 1.5))
            font = get_font(16)
            s = font.render(text, True, color)
            s.set_alpha(alpha)
            surface.blit(s, (lx - s.get_width()//2 + self.sw//2, ly - i*20))

    def draw(self, surface, player, enemy=None):
        self.draw_player_hud(surface, player)
        if enemy:
            self.draw_enemy_hud(surface, enemy)
        self.draw_combat_log(surface)
        self.ftm.draw(surface)

    def float_damage(self, dmg, x, y, is_crit=False, is_miss=False,
                     is_heal=False, is_magic=False):
        if is_miss:
            self.ftm.add('MISS!', x, y, (180,180,180), 22)
        elif is_heal:
            self.ftm.add(f'+{dmg}', x, y, (60,220,60), 26)
        elif is_crit:
            self.ftm.add(f'CRIT! {dmg}', x, y, (255,220,0), 36, 2.0)
        elif is_magic:
            self.ftm.add(str(dmg), x, y, (180,80,255), 28)
        else:
            self.ftm.add(str(dmg), x, y, (255,100,100), 26)


# ── Arena Background ──────────────────────────────────────────

class ArenaBackground:
    """Draws animated arena with crowd, torches, sand floor."""
    def __init__(self, w, h):
        self.w = w; self.h = h
        self.t = 0.0
        # Crowd members (precomputed)
        self.crowd = []
        for i in range(80):
            self.crowd.append({
                'x': random.randint(0, w),
                'y': random.randint(int(h*0.05), int(h*0.22)),
                'wave': random.uniform(0, math.pi*2),
                'spd':  random.uniform(1.5, 3.5),
                'color': (random.randint(150,230), random.randint(100,180),
                          random.randint(80,140)),
                'size': random.randint(8, 16),
            })
        # Torches
        self.torches = [
            (int(w*0.05), int(h*0.28)),
            (int(w*0.95), int(h*0.28)),
            (int(w*0.18), int(h*0.22)),
            (int(w*0.82), int(h*0.22)),
        ]
        # Flags
        self.flags = [
            {'x': int(w*0.1), 'y': int(h*0.15), 'color': (200,30,30)},
            {'x': int(w*0.9), 'y': int(h*0.15), 'color': (30,80,200)},
            {'x': int(w*0.3), 'y': int(h*0.1),  'color': (200,160,30)},
            {'x': int(w*0.7), 'y': int(h*0.1),  'color': (200,160,30)},
        ]

    def update(self, dt):
        self.t += dt

    def draw(self, surface):
        t = self.t
        w, h = self.w, self.h

        # Sky gradient
        for y in range(int(h*0.3)):
            ratio = y / (h*0.3)
            r = int(40 + ratio * 60)
            g = int(30 + ratio * 40)
            b = int(20 + ratio * 30)
            pygame.draw.line(surface, (r,g,b), (0,y), (w,y))

        # Stands / bleachers
        bleacher_pts = [
            (0, int(h*0.3)), (w, int(h*0.3)),
            (w, int(h*0.08)), (int(w*0.85), int(h*0.08)),
            (int(w*0.75), int(h*0.04)), (int(w*0.25), int(h*0.04)),
            (int(w*0.15), int(h*0.08)), (0, int(h*0.08)),
        ]
        pygame.draw.polygon(surface, (80,65,50), bleacher_pts)

        # Bleacher rows
        for row in range(6):
            ry = int(h*0.08 + row * (h*0.22/6))
            pygame.draw.line(surface, (70,55,40), (0, ry), (w, ry), 2)

        # Arch frame
        pygame.draw.arc(surface, (60,48,35),
                        (int(w*0.1), int(h*0.01), int(w*0.8), int(h*0.22)),
                        0, math.pi, int(h*0.04))

        # Crowd
        for c in self.crowd:
            wave = math.sin(t * c['spd'] + c['wave']) * 4
            head_y = int(c['y'] + wave)
            # Body
            pygame.draw.circle(surface, c['color'], (c['x'], head_y + c['size']), c['size']//2 + 2)
            # Head
            pygame.draw.circle(surface, (c['color'][0]+20, c['color'][1]+15, c['color'][2]+10),
                               (c['x'], head_y), c['size']//2)
            # Arms waving
            arm_angle = math.sin(t * c['spd'] * 1.3 + c['wave']) * 0.6
            ax1 = int(c['x'] - c['size']*0.8 * math.cos(arm_angle))
            ay1 = int(head_y + c['size'] + c['size']*0.5 * math.sin(arm_angle))
            ax2 = int(c['x'] + c['size']*0.8 * math.cos(arm_angle))
            ay2 = int(head_y + c['size'] - c['size']*0.5 * math.sin(arm_angle))
            pygame.draw.line(surface, c['color'], (c['x'], head_y+c['size']//2), (ax1,ay1), 2)
            pygame.draw.line(surface, c['color'], (c['x'], head_y+c['size']//2), (ax2,ay2), 2)

        # Flags
        for flag in self.flags:
            fx, fy = flag['x'], flag['y']
            # Pole
            pygame.draw.line(surface, (100,80,40), (fx, fy), (fx, fy+40), 3)
            # Flag waving
            wave = math.sin(t*3 + fx*0.01) * 8
            pts = [
                (fx, fy),
                (fx + 30, fy + wave),
                (fx + 30, fy + 18 + wave),
                (fx, fy + 18),
            ]
            pygame.draw.polygon(surface, flag['color'], pts)
            pygame.draw.polygon(surface, (0,0,0), pts, 1)

        # Torches
        from src.particle_system import particles
        for tx, ty in self.torches:
            # Torch pole
            pygame.draw.rect(surface, DARK_BROWN, (tx-4, ty, 8, 30))
            # Flame
            if random.random() < 0.3:
                particles.emit_fire(tx, ty, 3)
                particles.emit_smoke(tx, ty-10, 1)
            # Glow
            glow_r = int(30 + math.sin(t*7 + tx) * 10)
            glow_surf = pygame.Surface((glow_r*4, glow_r*4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 150, 30, 40),
                               (glow_r*2, glow_r*2), glow_r*2)
            surface.blit(glow_surf, (tx - glow_r*2, ty - glow_r*2),
                         special_flags=pygame.BLEND_RGBA_ADD)
            # Flame visual
            flame_h = int(20 + math.sin(t*8 + tx)*6)
            for fi in range(4):
                fw2 = 8 - fi*2
                fy2 = ty - fi * flame_h//4
                alpha = 200 - fi*40
                colors = [(255,80,10),(255,140,20),(255,210,50),(255,240,120)]
                if fw2 > 0:
                    flame_s = pygame.Surface((fw2*2, flame_h//4), pygame.SRCALPHA)
                    flame_s.fill((*colors[fi], alpha))
                    surface.blit(flame_s, (tx-fw2, fy2))

        # Arena wall
        wall_y = int(h * 0.3)
        pygame.draw.rect(surface, (90,70,50), (0, wall_y, w, int(h*0.08)))
        pygame.draw.line(surface, BRONZE, (0, wall_y), (w, wall_y), 3)
        # Pillars
        for px in [int(w*0.05), int(w*0.15), int(w*0.85), int(w*0.95)]:
            pygame.draw.rect(surface, (100,80,55), (px-10, wall_y-20, 20, int(h*0.08)+20))
            pygame.draw.rect(surface, BRONZE, (px-10, wall_y-20, 20, int(h*0.08)+20), 2)
            pygame.draw.ellipse(surface, (120,95,65), (px-14, wall_y-30, 28, 18))

        # Sand floor
        floor_y = wall_y + int(h*0.08)
        sand_pts = [(0, floor_y), (w, floor_y), (w, h), (0, h)]
        pygame.draw.polygon(surface, SAND_DK, sand_pts)
        # Sand texture (lines)
        for y in range(floor_y, h, 12):
            alpha = int(30 + 20 * math.sin(y * 0.1 + t * 0.5))
            pygame.draw.line(surface, (160,140,80), (0,y), (w,y), 1)
        # Sand dust
        if random.random() < 0.08:
            dx = random.randint(100, w-100)
            from src.particle_system import particles
            particles.emit_dust(dx, floor_y + random.randint(20,80), 2)

        # Blood stains on sand
        blood_spots = [(int(w*0.35), floor_y+60), (int(w*0.6), floor_y+90),
                        (int(w*0.5), floor_y+140)]
        for bx, by in blood_spots:
            bs = pygame.Surface((30, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(bs, (80,10,10,120), (0,0,30,20))
            surface.blit(bs, (bx-15, by-10))


# ── Tooltip ──────────────────────────────────────────────────

def draw_tooltip(surface, item, mx, my):
    lines = item.tooltip_lines() if hasattr(item, 'tooltip_lines') else [item.name]
    if getattr(item, 'count', 1) > 1:
        lines.insert(1, f'Count: {item.count}')
    fw = max(len(l) for l in lines) * 9 + 20
    fh = len(lines) * 20 + 14
    tx = min(mx + 14, surface.get_width() - fw - 4)
    ty = min(my,      surface.get_height() - fh - 4)

    r = pygame.Rect(tx, ty, fw, fh)
    draw_panel(surface, r, color=DARK_GRAY, border=item.color)
    draw_text(surface, lines[0], tx+8, ty+6, 16, item.color, bold=True, shadow=True)
    for i, ln in enumerate(lines[1:], 1):
        draw_text(surface, ln, tx+8, ty+6+i*18, 14, PARCHMENT, shadow=False)
