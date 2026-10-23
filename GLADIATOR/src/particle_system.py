# ============================================================
#  GLADIATOR ARENA - Particle System
# ============================================================
import pygame, random, math


class Particle:
    __slots__ = ['x','y','vx','vy','life','max_life','size','color',
                 'gravity','fade','shrink','glow']
    def __init__(self, x, y, vx, vy, life, size, color,
                 gravity=200, fade=True, shrink=True, glow=False):
        self.x=x; self.y=y; self.vx=vx; self.vy=vy
        self.life=life; self.max_life=life
        self.size=size; self.color=color
        self.gravity=gravity; self.fade=fade
        self.shrink=shrink; self.glow=glow


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def update(self, dt):
        alive = []
        for p in self.particles:
            p.life -= dt
            if p.life <= 0:
                continue
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.vy += p.gravity * dt
            alive.append(p)
        self.particles = alive

    def draw(self, surface):
        for p in self.particles:
            t = p.life / p.max_life
            alpha = int(255 * t) if p.fade else 255
            size  = max(1, int(p.size * t)) if p.shrink else max(1, int(p.size))
            r, g, b = p.color
            if p.glow:
                # Draw glow ring
                glow_surf = pygame.Surface((size*4, size*4), pygame.SRCALPHA)
                ga = int(alpha * 0.3)
                pygame.draw.circle(glow_surf, (r, g, b, ga),
                                   (size*2, size*2), size*2)
                surface.blit(glow_surf, (int(p.x)-size*2, int(p.y)-size*2),
                             special_flags=pygame.BLEND_RGBA_ADD)
            col = (min(r,255), min(g,255), min(b,255), alpha)
            try:
                s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(s, col, (size, size), size)
                surface.blit(s, (int(p.x)-size, int(p.y)-size),
                             special_flags=pygame.BLEND_RGBA_ADD)
            except Exception:
                pass

    # --- Emitters ---

    def emit_blood(self, x, y, count=12, direction=0):
        for _ in range(count):
            angle = direction + random.uniform(-0.8, 0.8)
            spd   = random.uniform(80, 280)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd - random.uniform(20, 100)
            life  = random.uniform(0.4, 1.0)
            size  = random.randint(3, 9)
            r = random.randint(140, 200)
            self.particles.append(Particle(
                x + random.uniform(-10,10),
                y + random.uniform(-5,5),
                vx, vy, life, size,
                (r, random.randint(0,30), random.randint(0,20)),
                gravity=350, fade=True, shrink=True))

    def emit_sparks(self, x, y, count=16):
        for _ in range(count):
            angle = random.uniform(0, math.pi*2)
            spd   = random.uniform(60, 300)
            life  = random.uniform(0.2, 0.7)
            size  = random.randint(2, 5)
            c = random.choice([(255,200,50),(255,160,30),(255,240,120)])
            self.particles.append(Particle(
                x, y,
                math.cos(angle)*spd, math.sin(angle)*spd - 60,
                life, size, c, gravity=400, glow=True))

    def emit_dust(self, x, y, count=8):
        for _ in range(count):
            vx = random.uniform(-40, 40)
            vy = random.uniform(-60, -10)
            life = random.uniform(0.5, 1.2)
            size = random.randint(4, 12)
            g = random.randint(160, 210)
            self.particles.append(Particle(
                x + random.uniform(-20,20), y,
                vx, vy, life, size,
                (g, int(g*0.9), int(g*0.7)), gravity=-20, fade=True, shrink=False))

    def emit_fire(self, x, y, count=6):
        for _ in range(count):
            vx = random.uniform(-30, 30)
            vy = random.uniform(-120, -60)
            life = random.uniform(0.3, 0.8)
            size = random.randint(4, 10)
            phase = random.random()
            if phase < 0.4:
                c = (255, 80, 10)
            elif phase < 0.7:
                c = (255, 160, 20)
            else:
                c = (255, 220, 60)
            self.particles.append(Particle(
                x + random.uniform(-8,8), y,
                vx, vy, life, size, c, gravity=-30, glow=True))

    def emit_smoke(self, x, y, count=4):
        for _ in range(count):
            vx = random.uniform(-20, 20)
            vy = random.uniform(-50, -15)
            life = random.uniform(1.0, 2.5)
            size = random.randint(8, 20)
            g = random.randint(80, 140)
            self.particles.append(Particle(
                x + random.uniform(-5,5), y,
                vx, vy, life, size,
                (g, g, g), gravity=-15, fade=True, shrink=False))

    def emit_magic(self, x, y, count=20, color=(160, 40, 220)):
        r, g, b = color
        for _ in range(count):
            angle = random.uniform(0, math.pi*2)
            spd   = random.uniform(40, 180)
            life  = random.uniform(0.4, 1.0)
            size  = random.randint(3, 8)
            self.particles.append(Particle(
                x + random.uniform(-20,20),
                y + random.uniform(-20,20),
                math.cos(angle)*spd, math.sin(angle)*spd,
                life, size,
                (min(r+40,255), min(g+40,255), min(b+60,255)),
                gravity=-60, glow=True))

    def emit_impact(self, x, y, color=(200,200,200)):
        self.emit_sparks(x, y, 10)
        self.emit_dust(x, y, 6)

    def emit_critical(self, x, y):
        self.emit_sparks(x, y, 30)
        self.emit_blood(x, y, 20)
        for _ in range(8):
            angle = random.uniform(0, math.pi*2)
            spd   = random.uniform(100, 400)
            self.particles.append(Particle(
                x, y,
                math.cos(angle)*spd, math.sin(angle)*spd,
                0.6, 7, (255,220,60), gravity=200, glow=True))


# Singleton
particles = ParticleSystem()
