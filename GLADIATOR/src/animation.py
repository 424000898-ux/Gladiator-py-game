# ============================================================
#  GLADIATOR ARENA - Animation System
# ============================================================
import math, time


class Tween:
    """Smooth value interpolation (lerp, ease-in, ease-out, elastic)."""
    LINEAR   = 'linear'
    EASE_IN  = 'ease_in'
    EASE_OUT = 'ease_out'
    EASE_IO  = 'ease_io'
    ELASTIC  = 'elastic'
    BOUNCE   = 'bounce'

    def __init__(self, start, end, duration, mode=EASE_OUT, on_done=None):
        self.start    = start
        self.end      = end
        self.duration = max(duration, 0.001)
        self.mode     = mode
        self.elapsed  = 0.0
        self.done     = False
        self.on_done  = on_done

    def update(self, dt):
        if self.done:
            return self.end
        self.elapsed += dt
        t = min(self.elapsed / self.duration, 1.0)
        v = self._curve(t)
        val = self.start + (self.end - self.start) * v
        if t >= 1.0:
            self.done = True
            if self.on_done:
                self.on_done()
        return val

    def _curve(self, t):
        if self.mode == self.LINEAR:
            return t
        elif self.mode == self.EASE_IN:
            return t * t
        elif self.mode == self.EASE_OUT:
            return 1 - (1 - t) ** 2
        elif self.mode == self.EASE_IO:
            return t * t * (3 - 2 * t)
        elif self.mode == self.ELASTIC:
            if t == 0 or t == 1:
                return t
            return -(2 ** (10 * (t - 1))) * math.sin((t - 1.1) * 5 * math.pi)
        elif self.mode == self.BOUNCE:
            if t < 1 / 2.75:
                return 7.5625 * t * t
            elif t < 2 / 2.75:
                t -= 1.5 / 2.75
                return 7.5625 * t * t + 0.75
            elif t < 2.5 / 2.75:
                t -= 2.25 / 2.75
                return 7.5625 * t * t + 0.9375
            else:
                t -= 2.625 / 2.75
                return 7.5625 * t * t + 0.984375
        return t

    @property
    def value(self):
        if self.done:
            return self.end
        t = min(self.elapsed / self.duration, 1.0)
        return self.start + (self.end - self.start) * self._curve(t)


class AnimationState:
    """A single animation clip: sequence of frames with timing."""
    def __init__(self, name, frames, fps=8, loop=True, next_state=None):
        self.name       = name
        self.frames     = frames  # list of draw-command dicts or frame indices
        self.fps        = fps
        self.loop       = loop
        self.next_state = next_state  # auto-transition when done
        self.frame_dur  = 1.0 / fps
        self._timer     = 0.0
        self._idx       = 0
        self.done       = False

    def reset(self):
        self._timer = 0.0
        self._idx   = 0
        self.done   = False

    def update(self, dt):
        if self.done:
            return
        self._timer += dt
        while self._timer >= self.frame_dur:
            self._timer -= self.frame_dur
            self._idx += 1
            if self._idx >= len(self.frames):
                if self.loop:
                    self._idx = 0
                else:
                    self._idx = len(self.frames) - 1
                    self.done = True

    @property
    def current_frame(self):
        return self.frames[min(self._idx, len(self.frames) - 1)]


class AnimationStateMachine:
    """Manages transitions between named AnimationStates."""
    def __init__(self):
        self.states  = {}
        self.current = None
        self._name   = None

    def add(self, state: AnimationState):
        self.states[state.name] = state

    def play(self, name, force=False):
        if name not in self.states:
            return
        if self._name == name and not force:
            return
        self._name   = name
        self.current = self.states[name]
        self.current.reset()

    def update(self, dt):
        if not self.current:
            return
        self.current.update(dt)
        # Auto-transition
        if self.current.done and self.current.next_state:
            self.play(self.current.next_state)

    @property
    def frame(self):
        if self.current:
            return self.current.current_frame
        return None

    @property
    def state_name(self):
        return self._name


class AnimationManager:
    """Global animation manager - tracks and updates all active tweens."""
    def __init__(self):
        self._tweens = []

    def tween(self, start, end, duration, mode=Tween.EASE_OUT, on_done=None):
        t = Tween(start, end, duration, mode, on_done)
        self._tweens.append(t)
        return t

    def update(self, dt):
        self._tweens = [t for t in self._tweens if not t.done]
        for t in self._tweens:
            t.update(dt)


# Singleton
anim_manager = AnimationManager()
