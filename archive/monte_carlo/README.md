# Monte Carlo Battle Simulator (mothballed)

Archived — not deleted. This is a working balance tool for the autobattler.
We'll need it when playtesting begins.

## What's here

| File | Purpose |
|---|---|
| `monte_carlo.py` | Simulator: party combat, LD50, adaptive difficulty API |
| `FINDINGS.md` | Preliminary balance analysis (7 scenarios, observations) |
| `MANUAL.md` | Full CLI reference + runtime API docs |

## To revive

Move it back and it just works:

```bash
mv archive/monte_carlo/monte_carlo.py grammar_mvp/monte_carlo.py
python -m grammar_mvp.monte_carlo --help
```

Depends on `grammar_mvp.battle` (resolve_turn, tick_effects) and
`grammar_mvp.game_state` (Character). If those APIs changed while
this was archived, update the imports.

## Key features when we return

- `--check 0.65` — quick "is this fight fair?" verdict
- `--auto-scale 0.65` — binary-search enemy HP to hit a target win rate
- `difficulty_check()` / `suggest_scaling()` — importable for game backend
