# ============================================================
#  GLADIATOR ARENA - Sound Manager
# ============================================================
import os, pygame, math, random, numpy as np


def _make_sound(samples, rate=22050):
    """Convert numpy array to pygame Sound."""
    arr = np.clip(samples, -32767, 32767).astype(np.int16)
    # Stereo
    stereo = np.column_stack([arr, arr])
    return pygame.sndarray.make_sound(stereo)


def _gen_sword_slash(rate=22050):
    n   = int(rate * 0.18)
    t   = np.linspace(0, 0.18, n)
    env = np.exp(-t * 18)
    # Noise burst + whistle
    noise = np.random.uniform(-1, 1, n)
    tone  = np.sin(2*math.pi*800*t) * 0.3
    sig   = (noise * 0.7 + tone) * env * 28000
    return _make_sound(sig, rate)


def _gen_sword_hit(rate=22050):
    n = int(rate * 0.22)
    t = np.linspace(0, 0.22, n)
    env = np.exp(-t * 12)
    noise = np.random.uniform(-1, 1, n)
    thud  = np.sin(2*math.pi*120*t) * 0.5
    sig   = (noise*0.4 + thud) * env * 30000
    return _make_sound(sig, rate)


def _gen_heavy_hit(rate=22050):
    n = int(rate * 0.35)
    t = np.linspace(0, 0.35, n)
    env = np.exp(-t * 8)
    thud  = np.sin(2*math.pi*60*t)
    crack = np.random.uniform(-1,1,n) * np.exp(-t*25)
    sig   = (thud*0.6 + crack*0.4) * env * 32000
    return _make_sound(sig, rate)


def _gen_critical(rate=22050):
    n = int(rate * 0.4)
    t = np.linspace(0, 0.4, n)
    # Rising sweep + impact
    freq = 200 + t * 2000
    sweep= np.sin(2*math.pi*np.cumsum(freq)/rate)
    env  = np.exp(-t * 6)
    noise= np.random.uniform(-1,1,n) * np.exp(-t*15)
    sig  = (sweep*0.5 + noise*0.5) * env * 30000
    return _make_sound(sig, rate)


def _gen_button_click(rate=22050):
    n = int(rate * 0.06)
    t = np.linspace(0, 0.06, n)
    env = np.exp(-t * 50)
    tone= np.sin(2*math.pi*600*t)
    sig = tone * env * 20000
    return _make_sound(sig, rate)


def _gen_gold_coin(rate=22050):
    n = int(rate * 0.15)
    t = np.linspace(0, 0.15, n)
    env = np.exp(-t * 20)
    tones = (np.sin(2*math.pi*1200*t) + np.sin(2*math.pi*1800*t)*0.5)
    sig = tones * env * 20000
    return _make_sound(sig, rate)


def _gen_crowd_cheer(rate=22050):
    n = int(rate * 1.5)
    t = np.linspace(0, 1.5, n)
    noise = np.random.uniform(-1, 1, n)
    # Low rumble
    rumble= np.sin(2*math.pi*80*t) * 0.3
    env   = np.ones(n)
    env[:int(rate*0.3)] = np.linspace(0, 1, int(rate*0.3))
    env[-int(rate*0.3):] = np.linspace(1, 0, int(rate*0.3))
    sig = (noise*0.6 + rumble) * env * 18000
    return _make_sound(sig, rate)


def _gen_miss(rate=22050):
    n = int(rate * 0.12)
    t = np.linspace(0, 0.12, n)
    env = np.exp(-t * 20)
    tone= np.sin(2*math.pi*300*t) * np.exp(-t*8)
    sig = tone * env * 15000
    return _make_sound(sig, rate)


def _gen_victory(rate=22050):
    n = int(rate * 1.2)
    t = np.linspace(0, 1.2, n)
    # Fanfare: C E G C  
    freqs = [261, 329, 392, 523]
    notes = []
    seg = n // 4
    for i, f in enumerate(freqs):
        tt = np.linspace(0, seg/rate, seg)
        env2 = np.exp(-tt*2)
        notes.append(np.sin(2*math.pi*f*tt)*env2)
    sig = np.concatenate(notes[:4]) * 22000
    if len(sig) < n:
        sig = np.pad(sig, (0, n-len(sig)))
    return _make_sound(sig[:n], rate)


def _gen_defeat(rate=22050):
    n = int(rate * 1.5)
    t = np.linspace(0, 1.5, n)
    # Descending tone
    freq = 400 - t * 200
    sig  = np.sin(2*math.pi*np.cumsum(freq)/rate)
    env  = np.exp(-t * 1.5)
    return _make_sound(sig * env * 20000, rate)


def _gen_potion(rate=22050):
    n = int(rate * 0.4)
    t = np.linspace(0, 0.4, n)
    # Bubble sounds
    sig = np.zeros(n)
    for _ in range(8):
        pos   = random.randint(0, n-1000)
        blen  = random.randint(500, 2000)
        tt    = np.linspace(0, blen/rate, blen)
        f     = random.uniform(400, 1200)
        bub   = np.sin(2*math.pi*f*tt) * np.exp(-tt*30)
        end   = min(pos+blen, n)
        sig[pos:end] += bub[:end-pos]
    env = np.exp(-t*2)
    return _make_sound(sig * env * 20000, rate)


class SoundManager:
    def __init__(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sounds   = {}
        self.music_on = True
        self.sfx_vol  = 0.7
        self.mus_vol  = 0.4
        self._loaded  = False
        self._current_music = None
        self.music_tracks = {
            'background': os.path.join(root, 'assets', 'background_sound.mp3'),
            'fight_arena': os.path.join(root, 'assets', 'fight_arena.mp3'),
        }

    def load(self):
        if self._loaded:
            return
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            # Generate all sounds procedurally
            self.sounds = {
                'sword_slash':  _gen_sword_slash(),
                'sword_hit':    _gen_sword_hit(),
                'heavy_hit':    _gen_heavy_hit(),
                'critical':     _gen_critical(),
                'button_click': _gen_button_click(),
                'gold_coin':    _gen_gold_coin(),
                'crowd_cheer':  _gen_crowd_cheer(),
                'miss':         _gen_miss(),
                'victory':      _gen_victory(),
                'defeat':       _gen_defeat(),
                'potion':       _gen_potion(),
            }
            for s in self.sounds.values():
                s.set_volume(self.sfx_vol)
            pygame.mixer.music.set_volume(self.mus_vol)
            self._loaded = True
        except Exception as e:
            print(f"[SoundManager] Warning: {e}")

    def play_music(self, name, loops=-1):
        if not self._loaded or not self.music_on:
            return
        if self._current_music == name:
            return
        path = self.music_tracks.get(name)
        if not path:
            return
        if not os.path.isfile(path):
            print(f"[SoundManager] Warning: music file not found: {path}")
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.mus_vol)
            pygame.mixer.music.play(loops=loops)
            self._current_music = name
        except Exception as e:
            print(f"[SoundManager] Warning: failed to play music '{name}': {e}")

    def stop_music(self):
        if not self._loaded:
            return
        pygame.mixer.music.stop()
        self._current_music = None

    def play(self, name, vol_scale=1.0):
        if not self._loaded:
            return
        s = self.sounds.get(name)
        if s:
            s.set_volume(self.sfx_vol * vol_scale)
            s.play()

    def set_sfx_vol(self, v):
        self.sfx_vol = max(0.0, min(1.0, v))
        for s in self.sounds.values():
            s.set_volume(self.sfx_vol)

    def set_mus_vol(self, v):
        self.mus_vol = max(0.0, min(1.0, v))
        pygame.mixer.music.set_volume(self.mus_vol)


# Singleton
sounds = SoundManager()
