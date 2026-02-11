"""Reusable animations for sprites, panels, or any positioned drawable."""


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
