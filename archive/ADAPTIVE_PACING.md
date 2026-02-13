# Adaptive Pacing — Design Notes

Status: **speculative / not yet implemented**

## Problem

Enemy turns fire on a fixed timer (`turn_delay` in `levels.toml`).
A flat delay is wrong for two audiences:

- **Slow learners** — still reading the hint, still figuring out which
  cards compose `P+D5`. The enemy attacking every 3 s feels punishing.
- **Fast players** — already fluent in ESENS from earlier levels. Waiting
  3 s between attacks is dead air.

We want the game to *feel* like it matches the player's tempo without the
player ever noticing it's doing so.

---

## 1. Per-Level Static Bounds

The cheapest useful step. Already half-built.

### TOML schema

```toml
# Global default
turn_delay     = 3.0

[[levels]]
id = "1-1"
turn_delay     = 4.0   # override: beginners get more breathing room
turn_delay_min = 2.5   # fastest the adaptive system will go
turn_delay_max = 5.0   # slowest it'll back off to
```

`load_levels()` already reads a global `turn_delay`. Adding per-level
override + min/max is trivial:

```python
# in load_levels(), inside the per-level loop:
global_delay = data.get("turn_delay", 3.0)
level["turn_delay"]     = raw.get("turn_delay", global_delay)
level["turn_delay_min"] = raw.get("turn_delay_min", level["turn_delay"] - 0.5)
level["turn_delay_max"] = raw.get("turn_delay_max", level["turn_delay"] + 2.0)
```

`views.py` would read `self.level_mgr.current_level["turn_delay"]`
instead of the module global.

---

## 2. Signals — What to Measure

| Signal | Where to capture | What it tells us |
|---|---|---|
| **Cast latency** | `BattleView._on_cast()` — time from phase entering `"build"` (or last cast) to the cast button press | How fast the player thinks in ESENS |
| **Invalid cast rate** | `_on_cast()` when `validate_esens()` raises | Grammar confusion — slow down |
| **Redraw usage** | `dispatch_action("redraw", ...)` | Bad hand, not necessarily slow — neutral signal |
| **HP at battle end** | `check_battle_end()` returning `"win"` | Close fight → maybe ease off next time |
| **Retries on same level** | `LevelManager.restart_level()` count | Struggling — widen the delay range upward |

### Sketch: capturing signals in GameState

```python
@dataclass
class GameState:
    # ... existing fields ...

    # Adaptive pacing telemetry (not saved to disk)
    cast_timestamps: list[float] = field(default_factory=list)
    invalid_casts: int = 0
    build_phase_entered_at: float = 0.0
```

```python
# in BattleView, when entering build phase:
self.state.build_phase_entered_at = time.monotonic()

# in BattleView._on_cast(), on successful cast:
now = time.monotonic()
self.state.cast_timestamps.append(now - self.state.build_phase_entered_at)
self.state.build_phase_entered_at = now  # reset for next cast window

# on invalid cast:
self.state.invalid_casts += 1
```

---

## 3. The Pace Controller

A simple object that lives on `BattleView` and adjusts the effective
`turn_delay` each tick.

```python
class PaceController:
    """Rubber-bands turn_delay toward the player's observed tempo."""

    def __init__(self, base: float, lo: float, hi: float):
        self.base = base
        self.lo = lo
        self.hi = hi
        self.effective = base
        self._nudge_rate = 0.1   # seconds per adjustment step

    def on_cast(self, latency: float):
        """Player cast a potion — adjust based on how fast they were."""
        if latency < self.base * 0.6:
            # Fast cast → tighten
            self.effective = max(self.lo, self.effective - self._nudge_rate)
        elif latency > self.base * 1.5:
            # Slow cast → loosen
            self.effective = min(self.hi, self.effective + self._nudge_rate)
        # In the middle → drift back toward base
        else:
            self.effective += (self.base - self.effective) * 0.05

    def on_invalid_cast(self):
        """Bad grammar → give them more time."""
        self.effective = min(self.hi, self.effective + self._nudge_rate * 2)

    def on_battle_end(self, hp_ratio: float):
        """hp_ratio = hero.hp / hero.max_hp at victory.
        Close call → nudge base up for next battle."""
        if hp_ratio < 0.25:
            self.base = min(self.hi, self.base + 0.2)
        elif hp_ratio > 0.75:
            self.base = max(self.lo, self.base - 0.1)
```

### Wiring it into BattleView

```python
# in _start_level():
lv = self.level_mgr.current_level
self.pacer = PaceController(
    base=lv["turn_delay"],
    lo=lv["turn_delay_min"],
    hi=lv["turn_delay_max"],
)

# in on_update(), replace the current timer check:
if self.turn_timer >= self.pacer.effective:
    self.turn_timer -= self.pacer.effective
    self._play_one_turn()
```

---

## 4. Persistence — Session vs Saved

Two options, not mutually exclusive:

**Session-only (recommended first):**
`PaceController` resets each battle. Player skill estimate is ephemeral.
Pro: no save-file complexity. Re-calibrates naturally.

**Persisted:**
Add a `player_pace` float to `save.json` alongside `level_index`.
`LevelManager` loads it and seeds `PaceController.base` for the first
battle of a session.

```python
# save.json
{"level_index": 4, "player_pace": 2.7}
```

Start session-only. Add persistence later if playtesting shows that
returning players get punished by re-calibration.

---

## 5. Beyond Timing — Other Adaptive Levers

The same signal pipeline can drive other knobs:

### 5a. Hint Escalation

If `invalid_casts` exceeds a threshold, swap the hint for a more
explicit one. Each level could carry a `hints` array:

```toml
[[levels]]
id = "1-3"
hints = [
    "Now YOU place the +. Drag + then D to buff Defense!",
    "Try this: drag + into slot 2, then D into slot 3.",
    "The potion P+D5 adds 5 Defense to your hero.",
]
```

`PaceController` (or a sibling `HintEscalator`) tracks which tier
the player has been bumped to.

### 5b. Smooth Draw Budget

Struggling players could get extra smooth draws. Currently
`smooth_draws` is static per level. An adaptive version:

```python
if retries_on_level > 1:
    state.smooth_draws_left += 1  # mercy draw
```

### 5c. Mana Forgiveness

On retry, grant +1 max mana. Doesn't change the level definition,
just gives a small cushion:

```python
# in _start_level(), if retrying:
if self._retry_count > 0:
    state.mana = min(state.mana + 1, state.max_mana + 1)
    state.max_mana = state.mana
```

### 5d. Enemy AI Hesitation

Instead of the enemy always attacking on the timer, give the enemy
a random chance to "hesitate" (skip a turn) when the player is
struggling. Visible in the battle log: "Goblin hesitates..."
Feels diegetic, not like the game is going easy on you.

```python
def _play_one_turn(self):
    if not self.hero_attacks_next and self.pacer.effective > self.pacer.base:
        if random.random() < 0.2:
            self.state.battle_log.append(f"{self.state.enemy.name} hesitates...")
            self.hero_attacks_next = not self.hero_attacks_next
            return
    # ... normal turn resolution ...
```

### 5e. Deck Thinning on Retry

If a player retries a level, remove one curse card from the deck.
Makes the retry objectively easier without changing the level's
identity. Resets if they leave and come back.

---

## 6. Design Principles

1. **Bias slow.** Grammar learning is the point. A player composing
   `P+D5` for the first time should never feel rushed.

2. **Invisible adjustments.** The player should feel like they're
   getting better, not like the game is getting easier. Never surface
   numbers. Enemy hesitation is the gold standard — it's diegetic.

3. **Designer keeps control.** `turn_delay_min` / `turn_delay_max`
   are hard limits. The adaptive system nudges within bounds, never
   outside them. If a level is meant to be frantic, set a high `lo`.

4. **Session-first.** Don't persist until playtesting proves it's
   needed. Re-calibration each session is a feature — it accounts for
   rust, different moods, playing tired.

5. **One lever at a time.** Ship timing adaptation alone. Validate it.
   Then layer hint escalation. Then mana forgiveness. Never stack
   multiple untested adaptations.

---

## 7. Implementation Order (when the time comes)

1. Per-level `turn_delay` / `turn_delay_min` / `turn_delay_max` in TOML
2. `PaceController` with cast-latency signal only
3. Wire into `BattleView.on_update`
4. Playtest. Tune `_nudge_rate` and thresholds.
5. Add `on_invalid_cast` signal
6. Add `on_battle_end` signal
7. Hint escalation
8. Everything else
