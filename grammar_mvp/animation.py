"""Reusable animations for sprites, panels, or any positioned drawable."""

import math


class HitAnimation:
    """Damped triangle-wave horizontal shake.

    Parameters
    ----------
    duration : float
        Total animation time in seconds (default 0.7).
    amplitude : float
        Peak displacement in pixels at the start (default 20.0).
    period : float
        Time for one full oscillation cycle in seconds (default 0.1).

    Usage
    -----
    Call :meth:`start` to begin the animation, then call :meth:`update`
    every frame with *delta_time*.  Read :attr:`offset` to get the current
    horizontal displacement to apply to whatever you're drawing.
    """

    def __init__(self, duration: float = 0.7, amplitude: float = 20.0,
                 period: float = 0.1):
        self.duration = duration
        self.amplitude = amplitude
        self.period = period
        self.elapsed: float = 0.0
        self.active: bool = False
        self.offset: float = 0.0

    def start(self):
        """(Re)start the shake from the beginning."""
        self.elapsed = 0.0
        self.active = True
        self.offset = 0.0

    def update(self, dt: float):
        """Advance the animation by *dt* seconds and recompute offset."""
        if not self.active:
            return

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False
            self.offset = 0.0
            return

        # Linear decay envelope: 1.0 → 0.0 over the duration
        envelope = 1.0 - (self.elapsed / self.duration)

        # Triangle wave that starts at +1, passes through 0 at 1/4 period,
        # reaches -1 at 1/2 period, back through 0 at 3/4, and +1 at period.
        phase = (self.elapsed % self.period) / self.period
        if phase < 0.5:
            wave = 1.0 - 4.0 * phase       # +1 → -1
        else:
            wave = -3.0 + 4.0 * phase       # -1 → +1

        self.offset = wave * envelope * self.amplitude


class DamageFloat:
    """Floating damage number that rises, wobbles, and fades out.

    Parameters
    ----------
    duration : float
        Total animation time in seconds (default 1.5).
    rise : float
        Total upward travel in pixels (default 32.0).
    wobble_amp : float
        Half-width of the sine wobble in pixels (default 4.0).
    wobble_period : float
        Time for one full sine cycle in seconds (default 0.2).
    """

    def __init__(self, duration: float = 1.5, rise: float = 32.0,
                 wobble_amp: float = 4.0, wobble_period: float = 0.2):
        self.duration = duration
        self.rise = rise
        self.wobble_amp = wobble_amp
        self.wobble_period = wobble_period
        self.elapsed: float = 0.0
        self.active: bool = False
        self.x_offset: float = 0.0
        self.y_offset: float = 0.0
        self.alpha: int = 255
        self.label: str = ""

    def start(self, label: str):
        """Begin the float animation with the given text (e.g. ``'-5'``)."""
        self.label = label
        self.elapsed = 0.0
        self.active = True
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.alpha = 255

    def update(self, dt: float):
        """Advance the animation by *dt* seconds."""
        if not self.active:
            return

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False
            self.alpha = 0
            return

        t = self.elapsed / self.duration  # 0 → 1

        # Rise linearly
        self.y_offset = t * self.rise

        # Sine wobble
        self.x_offset = math.sin(
            self.elapsed * 2.0 * math.pi / self.wobble_period
        ) * self.wobble_amp

        # Linear fade-out
        self.alpha = int(255 * (1.0 - t))


class BurnAnimation:
    """Card burns away: tints orange, shrinks, and fades out.

    Parameters
    ----------
    duration : float
        Total burn time in seconds (default 0.6).

    Usage
    -----
    Call :meth:`start` to begin, :meth:`update` every frame.
    Read :attr:`scale`, :attr:`alpha`, and :attr:`tint` to apply
    to whatever sprite you're drawing.  ``tint`` goes 0→1 (original
    colour → burn orange).
    """

    def __init__(self, duration: float = 0.6):
        self.duration = duration
        self.elapsed: float = 0.0
        self.active: bool = False
        self.scale: float = 1.0
        self.alpha: int = 255
        self.tint: float = 0.0  # 0 = original, 1 = full orange

    def start(self):
        """(Re)start the burn from the beginning."""
        self.elapsed = 0.0
        self.active = True
        self.scale = 1.0
        self.alpha = 255
        self.tint = 0.0

    def update(self, dt: float):
        """Advance the animation by *dt* seconds."""
        if not self.active:
            return

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False
            self.scale = 0.0
            self.alpha = 0
            return

        t = self.elapsed / self.duration  # 0 → 1

        # Shrink: 1.0 → 0.3
        self.scale = 1.0 - 0.7 * t

        # Fade out
        self.alpha = int(255 * (1.0 - t))

        # Tint toward orange: ramps up fast in the first half, then holds
        self.tint = min(1.0, t * 2.0)
