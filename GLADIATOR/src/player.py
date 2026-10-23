# ============================================================
#  GLADIATOR ARENA - Player
# ============================================================
import os, pygame, math, random
from settings import *
from src.items import Item, Equipment, Inventory
from src.animation import AnimationStateMachine, AnimationState, Tween


class GladiatorRenderer:
    """
    Draws a cartoon gladiator in the Swords & Sandals style:
    large torso, small legs, chunky armor, oversized weapons.
    Pure pygame drawing – no sprite files needed.
    """

    # --- Anatomy scale ---
    TORSO_W  = 54
    TORSO_H  = 60
    HEAD_R   = 22
    LEG_W    = 18
    LEG_H    = 38
    ARM_W    = 16
    ARM_H    = 44
    FOOT_W   = 22
    FOOT_H   = 10

    def __init__(self, x, y, facing=1, scale=1.0,
                 skin=(210,170,120), armor_color=(100,60,20),
                 weapon_name='Sword', class_name='Warrior'):
        self.x = x
        self.y = y
        self.facing      = facing   # 1=right, -1=left
        self.scale       = scale
        self.skin        = skin
        self.armor_color = armor_color
        self.weapon_name = weapon_name
        self.class_name  = class_name
        self.debug = False
        self.offset_tuning = {
            'pelvis_chest': 8.0,
            'chest_head': 18.0,
            'shoulder_y': 22.0,
            'shoulder_x': 0.28,
            'pelvis_hip_x': 0.24,
            'thigh_y': 24.0,
            'chest_width_factor': 0.32,
        }

        # Animation state
        self.anim_timer   = 0.0
        self.state        = 'idle'
        self.attack_timer = 0.0
        self.hurt_timer   = 0.0
        self.block_timer  = 0.0
        self.death_timer  = 0.0
        self.victory_timer= 0.0

        # Per-frame offsets (set by state machine)
        self.torso_sway  = 0.0   # horizontal sway
        self.bob         = 0.0   # vertical bob
        self.arm_raise   = 0.0   # right arm raise (0=down, 1=up)
        self.leg_stride  = 0.0   # leg stride phase
        self.lean        = 0.0   # body lean angle
        self.blink       = False
        self.blink_timer = 0.0
        self.alpha        = 255

        self.weapon_angle   = 0.0
        self.shield_offset  = 0.0

    def set_state(self, state):
        if self.state != state:
            self.state = state

    def update(self, dt):
        self.anim_timer += dt

        # Blink logic
        self.blink_timer -= dt
        if self.blink_timer <= 0:
            self.blink = True
            self.blink_timer = random.uniform(2.5, 5.0)
        elif self.blink:
            self.blink = False

        t = self.anim_timer

        if self.state == 'idle':
            self.bob      = math.sin(t * 1.8) * 3
            self.torso_sway = math.sin(t * 0.9) * 2
            self.arm_raise  = 0.05 + math.sin(t * 1.8) * 0.05
            self.leg_stride = 0.0
            self.lean       = 0.0
            self.weapon_angle = math.sin(t * 1.5) * 5

        elif self.state == 'walk':
            self.bob        = abs(math.sin(t * 6)) * -5
            self.leg_stride = math.sin(t * 6)
            self.arm_raise  = 0.1
            self.lean       = self.facing * 5
            self.weapon_angle = 20

        elif self.state == 'run':
            self.bob        = abs(math.sin(t * 10)) * -8
            self.leg_stride = math.sin(t * 10)
            self.arm_raise  = 0.2
            self.lean       = self.facing * 12
            self.weapon_angle = 40

        elif self.state == 'attack':
            self.attack_timer += dt
            phase = min(self.attack_timer / 0.25, 1.0)
            if phase < 0.4:
                p = phase / 0.4
                self.arm_raise    = p * 1.0
                self.weapon_angle = -60 + p * 30
                self.lean         = -self.facing * 8
            elif phase < 0.7:
                p = (phase - 0.4) / 0.3
                self.arm_raise    = 1.0 - p * 0.3
                self.weapon_angle = -30 + p * 120
                self.lean         = self.facing * 15
            else:
                p = (phase - 0.7) / 0.3
                self.arm_raise    = 0.7 - p * 0.6
                self.weapon_angle = 90 - p * 80
                self.lean         = self.facing * (15 - p*15)
            if self.attack_timer > 0.5:
                self.attack_timer = 0.0
                self.state = 'idle'

        elif self.state == 'heavy_attack':
            self.attack_timer += dt
            phase = min(self.attack_timer / 0.6, 1.0)
            if phase < 0.3:
                p = phase / 0.3
                self.arm_raise    = p
                self.weapon_angle = -90 + p * 30
                self.lean         = -self.facing * 15
                self.bob          = -p * 10
            elif phase < 0.6:
                p = (phase-0.3)/0.3
                self.arm_raise    = 1.0
                self.weapon_angle = -60 + p * 180
                self.lean         = self.facing * 20
                self.bob          = -10 + p * 10
            else:
                p = (phase-0.6)/0.4
                self.arm_raise    = 1.0 - p
                self.weapon_angle = 120 - p * 100
                self.lean         = self.facing * (20-p*20)
            if self.attack_timer > 0.8:
                self.attack_timer = 0.0
                self.state = 'idle'

        elif self.state == 'block':
            self.block_timer += dt
            self.arm_raise    = 0.5
            self.shield_offset = 20
            self.lean         = -self.facing * 5
            self.weapon_angle  = 30

        elif self.state == 'hurt':
            self.hurt_timer += dt
            p = min(self.hurt_timer / 0.3, 1.0)
            self.lean        = -self.facing * 20 * (1-p)
            self.arm_raise   = 0.3
            self.weapon_angle = 60
            if self.hurt_timer > 0.35:
                self.hurt_timer = 0.0
                self.state = 'idle'

        elif self.state == 'death':
            self.death_timer += dt
            p = min(self.death_timer / 1.0, 1.0)
            self.lean   = -self.facing * 90 * p
            self.bob    = 20 * p
            self.alpha  = int(255 * (1 - max(p - 0.6, 0) / 0.4))

        elif self.state == 'victory':
            self.victory_timer += dt
            t2 = self.victory_timer
            self.arm_raise  = 0.7 + math.sin(t2 * 5) * 0.3
            self.bob        = -10 + math.sin(t2 * 4) * 6
            self.weapon_angle= -90

        elif self.state == 'taunt':
            self.bob         = math.sin(t * 3) * 6
            self.arm_raise   = abs(math.sin(t * 3)) * 0.8
            self.lean        = math.sin(t * 1.5) * 10
            self.weapon_angle= math.sin(t * 2) * 30

        # No-block resets
        if self.state != 'block':
            self.shield_offset = max(self.shield_offset - dt * 60, 0)
            self.block_timer   = 0.0

    def draw(self, surface, equipment=None):
        s = self.scale
        x = int(self.x)
        y = int(self.y + self.bob * s)
        tx = x + int(self.torso_sway * s)
        ty = y

        self._draw_body_fallback(surface, equipment)


    def _draw_part(self, surface, image, pos, pivot, angle, scale, mirror=False, alpha=255):
        if image is None:
            return None
        if mirror:
            image = pygame.transform.flip(image, True, False)
        width = max(1, int(image.get_width() * scale))
        height = max(1, int(image.get_height() * scale))
        scaled = pygame.transform.smoothscale(image, (width, height))
        if alpha != 255:
            scaled = scaled.copy()
            scaled.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        pivot_vec = pygame.math.Vector2(pivot) * scale
        size = max(width, height) * 2
        temp = pygame.Surface((size, size), pygame.SRCALPHA)
        temp.blit(scaled, (size // 2 - pivot_vec.x, size // 2 - pivot_vec.y))
        rotated = pygame.transform.rotate(temp, -math.degrees(angle))
        rect = rotated.get_rect(center=pos)
        surface.blit(rotated, rect)
        if self.debug:
            pygame.draw.circle(surface, (255, 80, 80), pos, 3)
            pygame.draw.line(surface, (180, 180, 255), pos, (pos[0] + 20, pos[1]), 1)
            pygame.draw.line(surface, (180, 255, 180), pos, (pos[0], pos[1] + 20), 1)
        return rect

    def _dir_vector(self, angle, length):
        return pygame.math.Vector2(0, 1).rotate_rad(angle) * length

    def _draw_leg_side(self, surface, side, pelvis_top_y, chest_width, s):
        thigh = self.parts['thigh']
        lower_leg = self.parts['lower_leg']
        foot = self.parts['foot']
        thigh_pivot = self.pivots['thigh']
        lower_leg_pivot = self.pivots['lower_leg']
        foot_pivot = self.pivots['foot']
        hip_x = int(self.x + side * chest_width * self.offset_tuning['pelvis_hip_x'])
        hip_pos = (hip_x, pelvis_top_y + int(self.offset_tuning['thigh_y'] * s))
        thigh_len = max(1, int((thigh.get_height() - thigh_pivot[1]) * s))
        lower_len = max(1, int((lower_leg.get_height() - lower_leg_pivot[1]) * s))
        thigh_angle = math.radians(-self.leg_stride * 25 * side)
        knee_angle = thigh_angle + math.radians(30 + abs(self.leg_stride) * 10)
        ankle_angle = knee_angle * 0.35
        knee_pos = hip_pos + self._dir_vector(thigh_angle, thigh_len)
        ankle_pos = knee_pos + self._dir_vector(knee_angle, lower_len)
        self._draw_part(surface, thigh, hip_pos, thigh_pivot, thigh_angle, s, mirror=(side > 0))
        self._draw_part(surface, lower_leg, knee_pos, lower_leg_pivot, knee_angle, s, mirror=(side > 0))
        self._draw_part(surface, foot, ankle_pos, foot_pivot, ankle_angle, s, mirror=(side > 0))

    def _draw_arm_side(self, surface, side, shoulder_pos, equipment, s):
        shoulder = self.parts['shoulder']
        upper_arm = self.parts['upper_arm']
        forearm = self.parts['forearm']
        shoulder_pivot = self.pivots['shoulder']
        upper_pivot = self.pivots['upper_arm']
        forearm_pivot = self.pivots['forearm']
        arm_raise_target = self.arm_raise
        upper_angle = math.radians(-arm_raise_target * 75 + side * 5)
        forearm_angle = upper_angle + math.radians(15 + abs(arm_raise_target) * 22)
        upper_len = max(1, int((upper_arm.get_height() - upper_pivot[1]) * s))
        forearm_len = max(1, int((forearm.get_height() - forearm_pivot[1]) * s))
        elbow_pos = shoulder_pos + self._dir_vector(upper_angle, upper_len)
        wrist_pos = elbow_pos + self._dir_vector(forearm_angle, forearm_len)
        self._draw_part(surface, shoulder, shoulder_pos, shoulder_pivot, upper_angle * 0.2, s, mirror=(side > 0))
        self._draw_part(surface, upper_arm, shoulder_pos, upper_pivot, upper_angle, s, mirror=(side > 0))
        self._draw_part(surface, forearm, elbow_pos, forearm_pivot, forearm_angle, s, mirror=(side > 0))
        if side == self.facing:
            self._draw_weapon(surface, int(wrist_pos.x), int(wrist_pos.y), side, s, equipment)

    def _draw_body_fallback(self, surface, equipment=None):
        # Use the original procedural body draw if sprites are unavailable.
        s = self.scale
        f = self.facing
        x = int(self.x)
        y = int(self.y + self.bob * s)
        tx = x
        ty = y
        left_ang = math.radians(self.leg_stride * 25)
        right_ang = math.radians(-self.leg_stride * 25)
        lw = int(self.LEG_W * s)
        lh = int(self.LEG_H * s)
        lx = int(tx - lw // 2 - 4 * s)
        ly = ty
        self._draw_leg(surface, lx, ly, lh, lw, left_ang, f, s, equipment)
        rx = int(tx + lw // 2 - 4 * s)
        self._draw_leg(surface, rx, ly, lh, lw, right_ang, f, s, equipment)
        lean_r = math.radians(self.lean)
        tw = int(self.TORSO_W * s)
        th = int(self.TORSO_H * s)
        torso_top_y = ty - th
        ac = equipment.slots['chest'].color if (equipment and equipment.slots.get('chest')) else self.armor_color
        torso_pts = [
            (tx - tw // 2 + int(math.sin(lean_r) * th // 2), torso_top_y),
            (tx + tw // 2 + int(math.sin(lean_r) * th // 2), torso_top_y),
            (tx + tw // 2 - 4, ty),
            (tx - tw // 2 + 4, ty),
        ]
        pygame.draw.polygon(surface, ac, torso_pts)
        pygame.draw.polygon(surface, DARK_BROWN, torso_pts, 2)
        belt_y = ty - int(10 * s)
        pygame.draw.rect(surface, BRONZE_DK, (tx - tw // 2, belt_y, tw, int(8 * s)))
        bk = int(10 * s)
        pygame.draw.rect(surface, GOLD, (tx - bk // 2, belt_y, bk, int(8 * s)))
        if equipment and equipment.slots.get('shield'):
            sh_x = int(tx - f * (tw // 2 + 28 * s + self.shield_offset))
            sh_y = torso_top_y + int(15 * s)
            self._draw_shield(surface, sh_x, sh_y, s, equipment.slots['shield'])
        hx = int(tx + int(math.sin(lean_r) * th * 0.5) + int(self.torso_sway * s))
        hy = torso_top_y - int(self.HEAD_R * s)
        hr = int(self.HEAD_R * s)
        pygame.draw.rect(surface, self.skin,
                         (hx - int(7*s), torso_top_y - int(6*s), int(14*s), int(8*s)))
        pygame.draw.circle(surface, self.skin, (hx, hy), hr)
        self._draw_face(surface, hx, hy, hr, self.facing)
        if equipment and equipment.slots.get('helmet'):
            self._draw_helmet(surface, hx, hy, hr, s, equipment.slots['helmet'])
        else:
            pygame.draw.arc(surface, DARK_BROWN,
                            (hx - hr, hy - hr, hr * 2, hr * 2),
                            math.pi * 0.1, math.pi * 0.9, int(6 * s))
        self._draw_arm_with_weapon(surface, tx, torso_top_y, self.facing, s, self.arm_raise,
                                    equipment, lean_r)
        if not (equipment and equipment.slots.get('shield')):
            self._draw_bare_arm(surface, tx, torso_top_y, -self.facing, s,
                                 -self.arm_raise * 0.5, equipment)

    def _draw_leg(self, surface, lx, ly, lh, lw, angle, f, s, equip):
        # Thigh
        thigh_pts = self._rotated_rect(lx, ly, lw, lh//2, angle, pivot_y=0)
        pygame.draw.polygon(surface, self.armor_color, thigh_pts)
        pygame.draw.polygon(surface, DARK_BROWN, thigh_pts, 1)
        # Shin
        shin_off_x = int(math.sin(angle) * lh//2)
        shin_pts = self._rotated_rect(lx + shin_off_x, ly + lh//2,
                                       lw-2, lh//2, -angle*0.5, pivot_y=0)
        pygame.draw.polygon(surface, self.skin, shin_pts)
        pygame.draw.polygon(surface, DARK_BROWN, shin_pts, 1)
        # Boot
        foot_y = ly + lh + int(math.sin(angle)*4)
        boot_c = DARK_BROWN
        if equip and equip.slots.get('boots'):
            boot_c = (50, 40, 20)
        pygame.draw.ellipse(surface, boot_c,
                            (lx - int(self.FOOT_W*s)//2 + shin_off_x,
                             foot_y - int(self.FOOT_H*s)//2,
                             int(self.FOOT_W*s), int(self.FOOT_H*s)))

    def _rotated_rect(self, cx, cy, w, h, angle, pivot_y=0):
        hw, hh = w//2, h//2
        corners = [(-hw, pivot_y), (hw, pivot_y), (hw, h), (-hw, h)]
        pts = []
        ca, sa = math.cos(angle), math.sin(angle)
        for dx, dy in corners:
            rx = cx + dx*ca - dy*sa
            ry = cy + dx*sa + dy*ca
            pts.append((int(rx), int(ry)))
        return pts

    def _draw_face(self, surface, hx, hy, hr, f):
        # Eyes
        eo = int(hr * 0.35)
        ey = hy - int(hr * 0.1)
        eye_x = hx + f * eo
        if self.blink:
            pygame.draw.line(surface, (30,20,10),
                             (eye_x - int(hr*0.18), ey), (eye_x + int(hr*0.18), ey), 2)
        else:
            pygame.draw.circle(surface, (30,20,10), (eye_x, ey), int(hr*0.2))
            pygame.draw.circle(surface, WHITE, (eye_x + f, ey - 1), int(hr*0.08))
        # Nose
        pygame.draw.circle(surface, (self.skin[0]-20, self.skin[1]-20, self.skin[2]-20),
                           (hx + f*int(hr*0.15), hy + int(hr*0.15)), int(hr*0.1))
        # Mouth (grimace)
        mouth_x = hx + f * int(hr * 0.1)
        mouth_y = hy + int(hr * 0.42)
        pygame.draw.arc(surface, (100,50,30),
                        (mouth_x - int(hr*0.35), mouth_y - int(hr*0.1),
                         int(hr*0.7), int(hr*0.25)),
                        0, math.pi, 2)

    def _draw_helmet(self, surface, hx, hy, hr, s, helm_item):
        c = helm_item.color
        dc = tuple(max(0,v-40) for v in c)
        # Bowl
        pygame.draw.arc(surface, c,
                        (hx - hr, hy - hr, hr*2, hr*2),
                        math.pi*0.05, math.pi*0.95, hr)
        # Nose guard
        pygame.draw.rect(surface, dc,
                         (hx - int(4*s), hy - int(4*s), int(8*s), int(hr*0.8)))
        # Cheek guards
        for side in [-1, 1]:
            pygame.draw.rect(surface, dc,
                             (hx + side*int(hr*0.6) - int(4*s),
                              hy + int(hr*0.1),
                              int(10*s), int(hr*0.7)), 0, 3)
        # Plume
        plume_pts = [
            (hx, hy - hr - int(18*s)),
            (hx - int(6*s), hy - hr - int(8*s)),
            (hx + int(6*s), hy - hr - int(8*s)),
        ]
        pygame.draw.polygon(surface, (200, 30, 30), plume_pts)

    def _draw_shield(self, surface, sx, sy, s, shield_item):
        c = shield_item.color
        dc = tuple(max(0,v-30) for v in c)
        w, h = int(28*s), int(40*s)
        # Shield body
        pts = [
            (sx - w//2, sy),
            (sx + w//2, sy),
            (sx + w//2, sy + int(h*0.7)),
            (sx,        sy + h),
            (sx - w//2, sy + int(h*0.7)),
        ]
        pygame.draw.polygon(surface, c, pts)
        pygame.draw.polygon(surface, dc, pts, 3)
        # Boss
        pygame.draw.circle(surface, BRONZE, (sx, sy + h//2), int(7*s))
        pygame.draw.circle(surface, BRONZE_DK, (sx, sy + h//2), int(7*s), 2)

    def _draw_arm_with_weapon(self, surface, tx, torso_top_y, f, s, arm_raise, equip, lean_r):
        # Shoulder
        sx = int(tx + f * self.TORSO_W//2 * s + math.sin(lean_r)*self.TORSO_H*s*0.4)
        sy = torso_top_y + int(8*s)
        aw = int(self.ARM_W * s)
        # Upper arm angle
        base_ang = math.radians(-90 * arm_raise * f)
        # Forearm
        ua_len = int(22 * s)
        fa_len = int(20 * s)
        elbow_x = sx + int(math.cos(base_ang) * ua_len * f)
        elbow_y = sy + int(math.sin(base_ang) * ua_len + ua_len * 0.3)
        # Upper arm
        pygame.draw.line(surface, self.skin, (sx, sy), (elbow_x, elbow_y), aw)
        # Forearm
        wrist_ang = base_ang + math.radians(self.weapon_angle * f * 0.3)
        wrist_x = elbow_x + int(math.cos(wrist_ang) * fa_len * f)
        wrist_y = elbow_y + int(math.sin(wrist_ang) * fa_len)
        pygame.draw.line(surface, self.skin, (elbow_x, elbow_y), (wrist_x, wrist_y), aw-2)
        # Gauntlet
        if equip and equip.slots.get('boots'):  # reuse boot for gloves color hack
            gc = (50,40,20)
        else:
            gc = BRONZE_DK
        pygame.draw.circle(surface, gc, (wrist_x, wrist_y), int(8*s))
        # Weapon
        self._draw_weapon(surface, wrist_x, wrist_y, f, s, equip)

    def _draw_bare_arm(self, surface, tx, torso_top_y, f, s, arm_raise, equip):
        sx = int(tx + f * self.TORSO_W//2 * s)
        sy = torso_top_y + int(8*s)
        aw = int((self.ARM_W - 2) * s)
        ang = math.radians(-40 * arm_raise * f)
        ua = int(20*s)
        ex = sx + int(math.cos(ang)*ua*f)
        ey = sy + int(math.sin(ang)*ua + ua*0.3)
        pygame.draw.line(surface, self.skin, (sx, sy), (ex, ey), aw)
        pygame.draw.line(surface, self.skin, (ex, ey),
                         (ex + int(f*8*s), ey + int(10*s)), aw-2)

    def _draw_body_sprite(self, surface, tx, ty, f, s):
        img = self.body_sprite
        if img is None:
            return

        if f < 0:
            img = pygame.transform.flip(img, True, False)
        if s != 1.0:
            img = pygame.transform.rotozoom(img, 0, s)

        img_rect = img.get_rect(midbottom=(tx, ty))
        surface.blit(img, img_rect)

    def _draw_weapon(self, surface, wx, wy, f, s, equip):
        wname = 'Sword'
        if equip and equip.slots.get('weapon'):
            wname = equip.slots['weapon'].name
        elif self.weapon_name:
            wname = self.weapon_name

        ang = math.radians(self.weapon_angle * f)
        weapon_color = (180, 180, 200)
        handle_color = DARK_BROWN

        if 'Sword' in wname or 'Blade' in wname or 'Gladius' in wname or 'Excalibur' in wname:
            self._draw_sword(surface, wx, wy, f, s, ang, weapon_color)
        elif 'Axe' in wname:
            self._draw_axe(surface, wx, wy, f, s, ang)
        elif 'Hammer' in wname or 'Mace' in wname:
            self._draw_hammer(surface, wx, wy, f, s, ang)
        elif 'Spear' in wname:
            self._draw_spear(surface, wx, wy, f, s, ang)
        elif 'Dual' in wname:
            self._draw_sword(surface, wx, wy, f, s, ang, (160,220,160))
            self._draw_sword(surface, wx+int(f*8*s), wy+int(8*s), f, s,
                              ang+0.5, (200,160,200))
        else:
            self._draw_sword(surface, wx, wy, f, s, ang, weapon_color)

    def _draw_sword(self, surface, wx, wy, f, s, ang, color):
        blen = int(55 * s)
        blade_end_x = wx + int(math.cos(ang) * blen * f)
        blade_end_y = wy + int(math.sin(ang) * blen)
        # Blade
        pygame.draw.line(surface, color, (wx, wy), (blade_end_x, blade_end_y), int(5*s))
        # Edge gleam
        pygame.draw.line(surface, WHITE, (wx, wy), (blade_end_x, blade_end_y), int(2*s))
        # Cross-guard
        gx = wx + int(math.cos(ang) * 10 * f)
        gy = wy + int(math.sin(ang) * 10)
        perp = ang + math.pi/2
        g1x = gx + int(math.cos(perp) * 12 * f)
        g1y = gy + int(math.sin(perp) * 12)
        g2x = gx - int(math.cos(perp) * 12 * f)
        g2y = gy - int(math.sin(perp) * 12)
        pygame.draw.line(surface, BRONZE, (g1x, g1y), (g2x, g2y), int(4*s))
        # Handle
        hx2 = wx - int(math.cos(ang) * 16 * f)
        hy2 = wy - int(math.sin(ang) * 16)
        pygame.draw.line(surface, DARK_BROWN, (wx, wy), (hx2, hy2), int(5*s))

    def _draw_axe(self, surface, wx, wy, f, s, ang):
        # Handle
        hlen = int(45 * s)
        hx2 = wx + int(math.cos(ang) * hlen * f)
        hy2 = wy + int(math.sin(ang) * hlen)
        pygame.draw.line(surface, DARK_BROWN, (wx, wy), (hx2, hy2), int(5*s))
        # Axe head
        head_x = wx + int(math.cos(ang) * (hlen-5) * f)
        head_y = wy + int(math.sin(ang) * (hlen-5))
        perp = ang + math.pi/2
        p1 = (head_x + int(math.cos(perp)*18*f), head_y + int(math.sin(perp)*18))
        p2 = (head_x - int(math.cos(perp)*10*f), head_y - int(math.sin(perp)*10))
        p3 = (head_x + int(math.cos(ang)*22*f),  head_y + int(math.sin(ang)*22))
        pygame.draw.polygon(surface, (160,160,180), [p1, p2, p3])
        pygame.draw.polygon(surface, (100,100,120), [p1, p2, p3], 2)

    def _draw_hammer(self, surface, wx, wy, f, s, ang):
        hlen = int(45 * s)
        hx2 = wx + int(math.cos(ang) * hlen * f)
        hy2 = wy + int(math.sin(ang) * hlen)
        pygame.draw.line(surface, DARK_BROWN, (wx, wy), (hx2, hy2), int(5*s))
        # Head block
        head_x = wx + int(math.cos(ang) * (hlen) * f)
        head_y = wy + int(math.sin(ang) * hlen)
        perp = ang + math.pi/2
        hw = int(12*s); hh = int(20*s)
        pts = [
            (head_x + int(math.cos(perp)*hw), head_y + int(math.sin(perp)*hw)),
            (head_x - int(math.cos(perp)*hw), head_y - int(math.sin(perp)*hw)),
            (head_x - int(math.cos(perp)*hw) + int(math.cos(ang)*hh*f),
             head_y - int(math.sin(perp)*hw) + int(math.sin(ang)*hh)),
            (head_x + int(math.cos(perp)*hw) + int(math.cos(ang)*hh*f),
             head_y + int(math.sin(perp)*hw) + int(math.sin(ang)*hh)),
        ]
        pygame.draw.polygon(surface, (130,130,150), pts)
        pygame.draw.polygon(surface, (80,80,100), pts, 3)

    def _draw_spear(self, surface, wx, wy, f, s, ang):
        slen = int(70 * s)
        sx2 = wx + int(math.cos(ang) * slen * f)
        sy2 = wy + int(math.sin(ang) * slen)
        pygame.draw.line(surface, DARK_BROWN, (wx, wy), (sx2, sy2), int(4*s))
        # Tip
        tip_x = wx + int(math.cos(ang) * slen * f)
        tip_y = wy + int(math.sin(ang) * slen)
        perp = ang + math.pi/2
        p1 = (tip_x, tip_y)
        p2 = (tip_x - int(math.cos(perp)*6*f) - int(math.cos(ang)*16*f),
              tip_y - int(math.sin(perp)*6)   - int(math.sin(ang)*16))
        p3 = (tip_x + int(math.cos(perp)*6*f) - int(math.cos(ang)*16*f),
              tip_y + int(math.sin(perp)*6)   - int(math.sin(ang)*16))
        pygame.draw.polygon(surface, (180,180,200), [p1, p2, p3])


class Player:
    def __init__(self, name='Hero', class_name='Warrior',
                 skin=(210,170,120), armor_color=None, gender='Male'):
        self.name       = name
        self.class_name = class_name
        self.gender     = gender
        stats = CLASSES[class_name].copy()
        self.base_max_hp      = stats['hp']
        self.hp               = stats['hp']
        self.base_max_mp      = stats['mp']
        self.mp               = stats['mp']
        self.base_max_stamina = stats['stamina']
        self.stamina          = stats['stamina']
        self.strength         = stats['strength']
        self.defense          = stats['defense']
        self.agility          = stats['agility']
        self.intelligence     = stats['intelligence']
        self.crit_chance      = stats['crit']
        self.dodge_chance     = stats['dodge']
        self.accuracy         = stats['accuracy']
        self.block_chance     = stats['block']
        self.level      = 1
        self.xp         = 0
        self.xp_next    = XP_PER_LEVEL[1]
        self.arena_rank  = 1
        self.wins        = 0
        self.losses      = 0
        self.kills       = 0
        self.gold        = 150

        self.equipment   = Equipment()
        self.inventory   = Inventory()
        self.inventory.gold = self.gold

        # Add starter weapon
        starter_name = stats['weapon']
        self.equipment.equip(Item(starter_name))

        # Status effects
        self.stunned      = False
        self.raged        = False
        self.rage_turns   = 0
        self.dodge_next   = False
        self.str_boost    = 0
        self.status_effects = []

        # Visual
        self.skin        = skin
        self.armor_color = armor_color or stats['color']
        self.renderer    = GladiatorRenderer(
            0, 0, facing=1, scale=1.2,
            skin=skin, armor_color=self.armor_color,
            weapon_name=starter_name, class_name=class_name)
        self.skin = skin

        # Achievements
        self.achievements = []

    @property
    def alive(self):
        return self.hp > 0

    @property
    def max_hp(self):
        return self.base_max_hp + self.equipment.total_health

    @property
    def max_mp(self):
        return self.base_max_mp + self.equipment.total_mana

    @property
    def max_stamina(self):
        return self.base_max_stamina + self.equipment.total_stamina

    def get_crit_chance(self):
        weapon_bonus = self.equipment.weapon.crit_chance if self.equipment.weapon else 0
        return self.crit_chance + self.equipment.total_crit + weapon_bonus

    def get_dodge_chance(self):
        return self.dodge_chance + self.equipment.total_dodge

    def get_attack_speed(self):
        weapon_speed = self.equipment.weapon.attack_speed if self.equipment.weapon else 1.0
        return round(max(0.3, weapon_speed + self.equipment.total_move_speed), 2)

    def get_accuracy(self):
        return max(40, self.accuracy)

    def get_resistance(self):
        return self.equipment.total_resistance

    def level_up(self):
        self.level += 1
        # Stat gains per level
        # increase base stats (properties compute max values)
        self.base_max_hp += 10
        self.hp = self.max_hp
        self.base_max_mp += 5
        self.mp = self.max_mp
        self.strength  += 2
        self.defense   += 1
        self.agility   += 1
        self.intelligence += 1
        if self.level < len(XP_PER_LEVEL):
            self.xp_next = XP_PER_LEVEL[self.level]
        else:
            self.xp_next = self.xp + 99999

    def add_xp(self, amount):
        self.xp += amount
        leveled = []
        while self.xp >= self.xp_next:
            self.level_up()
            leveled.append(self.level)
        return leveled

    def get_attack_damage(self):
        weapon = self.equipment.weapon
        base = weapon.dmg if weapon else 5
        raw = base + self.strength * 1.3
        if weapon:
            raw += weapon.elemental
        raw += int(self.equipment.total_crit * 0.2)
        if self.raged:
            raw *= 1.75
        if self.str_boost:
            raw += self.str_boost
        return max(1, int(raw))

    def get_defense(self):
        return self.defense + self.equipment.total_defense

    def get_block(self):
        return self.block_chance + self.equipment.total_block

    def take_damage(self, dmg):
        mitigation = self.get_defense() // 3
        actual = max(0, dmg - mitigation)
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount):
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old

    def restore_mp(self, amount):
        old = self.mp
        self.mp = min(self.max_mp, self.mp + amount)
        return self.mp - old

    def use_item(self, item: Item):
        result = {}
        if item.type == 'consumable':
            if item.heal:
                result['heal'] = self.heal(item.heal)
            if item.mp:
                result['mp'] = self.restore_mp(item.mp)
            if item.buff == 'rage':
                self.raged = True
                self.rage_turns = 2
                self.status_effects.append('Rage')
                result['buff'] = 'rage'
            if item.buff == 'shield':
                self.status_effects.append('Shielded')
            # Handle stacks: decrement count or remove
            if getattr(item, 'count', 1) > 1:
                item.count -= 1
            else:
                self.inventory.remove(item)
        return result

    def tick_status(self):
        if self.raged:
            self.rage_turns -= 1
            if self.rage_turns <= 0:
                self.raged = False
                if 'Rage' in self.status_effects:
                    self.status_effects.remove('Rage')
        self.stunned = False
        self.dodge_next = False
        self.str_boost = 0

    def to_dict(self):
        return {
            'name': self.name, 'class': self.class_name, 'gender': self.gender,
            'level': self.level, 'xp': self.xp, 'xp_next': self.xp_next,
            'hp': self.hp, 'base_max_hp': self.base_max_hp,
            'mp': self.mp, 'base_max_mp': self.base_max_mp,
            'stamina': self.stamina, 'base_max_stamina': self.base_max_stamina,
            'strength': self.strength, 'defense': self.defense,
            'agility': self.agility, 'intelligence': self.intelligence,
            'crit_chance': self.crit_chance, 'dodge_chance': self.dodge_chance,
            'accuracy': self.accuracy, 'block_chance': self.block_chance,
            'arena_rank': self.arena_rank, 'wins': self.wins,
            'losses': self.losses, 'kills': self.kills,
            'gold': self.inventory.gold,
            'equipment': self.equipment.to_dict(),
            'inventory': self.inventory.to_dict(),
            'achievements': self.achievements,
            'skin': list(self.skin),
            'armor_color': list(self.armor_color),
            'status_effects': self.status_effects,
        }

    @classmethod
    def from_dict(cls, d):
        skin = tuple(d.get('skin', [210,170,120]))
        ac = tuple(d.get('armor_color', [100,60,20]))
        p = cls(d['name'], d['class'], skin=skin, armor_color=ac, gender=d.get('gender','Male'))
        for key in ['level','xp','xp_next','hp','base_max_hp','mp','base_max_mp',
                    'stamina','base_max_stamina','strength','defense','agility',
                    'intelligence','crit_chance','dodge_chance','accuracy',
                    'block_chance','arena_rank','wins','losses','kills','achievements']:
            if key in d:
                setattr(p, key, d[key])
        p.inventory = Inventory.from_dict(d.get('inventory', {}))
        p.equipment = Equipment.from_dict(d.get('equipment', {}))
        p.status_effects = d.get('status_effects', [])
        p.renderer.skin        = skin
        p.renderer.armor_color = ac
        return p
