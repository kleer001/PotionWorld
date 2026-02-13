#!/usr/bin/env python3
"""
Hand Playability Analysis for PotionWorld
==========================================

For each level (and proposed level-2 scenarios), answer:
  "What fraction of randomly drawn hands can compose at least one valid
   ESENS potion?"

Method
------
1. Build the deck for each level (grammar + action + curse cards).
2. For N_SIMS random hands, check every permutation of grammar cards
   from that hand into the available lock slots.  If ANY arrangement
   produces a string the ESENS parser accepts, the hand is "playable".
3. Report P(playable) for the default hand_size and for sizes 4-7.
"""

import sys
import random
import itertools
from pathlib import Path
from collections import Counter

# ---------------------------------------------------------------------------
# Path setup — make project importable
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "grammar_mvp"))

from ESENS_Parser import parse_esens, ESENSParseError
from grammar_mvp.levels import load_levels, build_level_deck
from grammar_mvp.cards import load_cards

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
N_SIMS = 50_000
RNG = random.Random(42)  # reproducible

# ---------------------------------------------------------------------------
# Core analysis logic
# ---------------------------------------------------------------------------


def grammar_tokens_from_hand(hand):
    """Return a list of ESENS token strings from grammar cards in hand."""
    return [c["token"] for c in hand if c.get("type") == "grammar"]


def can_make_valid_potion(grammar_tokens, open_slot_count, implied_prefix):
    """
    Check if any subset+ordering of *grammar_tokens* placed into
    *open_slot_count* slots (appended after *implied_prefix*) yields
    a valid ESENS string.

    We try every k-permutation for k = 1..open_slot_count.
    Because open_slot_count is small (typically 2-5) and tokens may
    repeat, we de-duplicate by working on the set of distinct
    permutations.
    """
    n_open = open_slot_count
    if n_open <= 0:
        # No open slots — only the implied prefix itself
        if implied_prefix:
            try:
                parse_esens(implied_prefix, explain=False)
                return True
            except ESENSParseError:
                return False
        return False

    # Try filling 1..n_open slots with grammar tokens from hand
    for k in range(1, n_open + 1):
        # Use set to avoid re-testing duplicate permutations
        seen = set()
        for perm in itertools.permutations(grammar_tokens, k):
            if perm in seen:
                continue
            seen.add(perm)
            notation = implied_prefix + "".join(perm)
            try:
                parse_esens(notation, explain=False)
                return True
            except ESENSParseError:
                continue
    return False


def simulate_level(deck, hand_size, slot_count, implied_cards, n_sims=N_SIMS):
    """
    Run *n_sims* random hands drawn from *deck* and return the fraction
    that can produce at least one valid ESENS potion.

    Parameters
    ----------
    deck : list[dict]
        Full deck of card dicts (grammar + action + curse).
    hand_size : int
        Number of cards drawn per hand.
    slot_count : int
        Total lock slots.
    implied_cards : list[tuple[str, int]]
        Pre-filled tokens as (token, slot_index).
    """
    # Build the implied prefix — tokens ordered by slot index
    implied_sorted = sorted(implied_cards, key=lambda x: x[1])
    implied_prefix = "".join(tok for tok, _ in implied_sorted)
    n_implied = len(implied_cards)
    open_slots = slot_count - n_implied

    playable = 0
    for _ in range(n_sims):
        # Draw a hand
        if hand_size >= len(deck):
            hand = list(deck)
        else:
            hand = RNG.sample(deck, hand_size)

        g_tokens = grammar_tokens_from_hand(hand)
        if can_make_valid_potion(g_tokens, open_slots, implied_prefix):
            playable += 1

    return playable / n_sims


# ---------------------------------------------------------------------------
# Level 2 proposed decks
# ---------------------------------------------------------------------------

def build_synthetic_deck(card_db, grammar_spec, n_curses=0, n_actions=0):
    """
    Build a deck from a grammar_spec = [(token, count), ...] plus
    optional curse and action filler cards.
    """
    token_to_card = {}
    for cid, cdata in card_db.items():
        if cdata.get("type") == "grammar":
            tok = cdata["token"]
            if tok not in token_to_card:
                token_to_card[tok] = cdata

    deck = []
    for token, count in grammar_spec:
        if token in token_to_card:
            for _ in range(count):
                deck.append(dict(token_to_card[token]))

    # Add curse cards (Dead Weight — occupies hand slot, not grammar)
    curse = card_db.get("curse_dead_weight")
    if curse:
        for _ in range(n_curses):
            deck.append(dict(curse))

    # Add action cards (Redraw — occupies hand slot, not grammar)
    action = card_db.get("action_redraw")
    if action:
        for _ in range(n_actions):
            deck.append(dict(action))

    return deck


LEVEL2_BASE_GRAMMAR = [
    ("P", 3), ("E", 3), ("+", 3), ("-", 3),
    ("H", 3), ("S", 2), ("D", 2), ("5", 3), ("10", 2),
]

LEVEL2_SCENARIOS = [
    {
        "id": "2-1",
        "title": "Mana pressure",
        "grammar": LEVEL2_BASE_GRAMMAR,
        "n_curses": 0,
        "n_actions": 0,
        "slot_count": 5,
        "implied_cards": [],
        "hand_sizes": [5, 6, 7],
    },
    {
        "id": "2-2",
        "title": "Dead Weight",
        "grammar": LEVEL2_BASE_GRAMMAR,
        "n_curses": 3,
        "n_actions": 0,
        "slot_count": 5,
        "implied_cards": [],
        "hand_sizes": [5, 6, 7],
    },
    {
        "id": "2-3",
        "title": "Redraw available",
        "grammar": LEVEL2_BASE_GRAMMAR,
        "n_curses": 3,
        "n_actions": 2,
        "slot_count": 5,
        "implied_cards": [],
        "hand_sizes": [5, 6, 7],
    },
    {
        "id": "2-7",
        "title": "Boss",
        "grammar": LEVEL2_BASE_GRAMMAR,
        "n_curses": 4,
        "n_actions": 2,
        "slot_count": 5,
        "implied_cards": [],
        "hand_sizes": [5, 6, 7],
    },
]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def fmt_pct(p):
    """Format probability as a percentage string."""
    return f"{p * 100:6.1f}%"


def threshold_hand_size(results_by_hs, target=0.333):
    """Return the smallest hand_size where P(playable) >= target, or '> max'."""
    for hs in sorted(results_by_hs):
        if results_by_hs[hs] >= target:
            return str(hs)
    return f"> {max(results_by_hs)}"


def print_table(rows, col_headers, row_label_width=32):
    """Pretty-print a results table."""
    col_w = 9
    header = " " * row_label_width
    for h in col_headers:
        header += f"{h:>{col_w}}"
    print(header)
    print("-" * len(header))
    for label, vals in rows:
        line = f"{label:<{row_label_width}}"
        for v in vals:
            line += f"{v:>{col_w}}"
        print(line)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    card_db = load_cards()
    levels = load_levels()

    print("=" * 78)
    print(" PotionWorld — Hand Playability Analysis")
    print(f" Simulations per scenario: {N_SIMS:,}")
    print("=" * 78)

    # ------------------------------------------------------------------
    # Part 1: Existing levels 1-1 through 1-4, hand sizes 4-7
    # ------------------------------------------------------------------
    print("\n")
    print("PART 1: Existing Levels (1-1 through 1-4)")
    print("=" * 78)

    level1_hand_sizes = [4, 5, 6, 7]
    col_headers = [f"HS={hs}" for hs in level1_hand_sizes] + [">=33% @"]

    rows = []
    for level in levels:
        lid = level["id"]
        title = level["title"]
        deck = build_level_deck(level, card_db)
        implied = level["implied_cards"]
        slot_count = level["slot_count"]
        default_hs = level["hand_size"]

        # Describe the deck composition
        grammar_cards = [c for c in deck if c.get("type") == "grammar"]
        non_grammar = [c for c in deck if c.get("type") != "grammar"]
        token_counts = Counter(c["token"] for c in grammar_cards)
        token_summary = ", ".join(
            f"{tok}x{cnt}" for tok, cnt in sorted(token_counts.items())
        )
        implied_str = (
            "+".join(tok for tok, _ in sorted(implied, key=lambda x: x[1]))
            if implied else "(none)"
        )

        print(f"\n  Level {lid}: {title}")
        print(f"    Slots: {slot_count}  |  Implied: {implied_str}  |  Default HS: {default_hs}")
        print(f"    Deck ({len(deck)} cards): {token_summary}", end="")
        if non_grammar:
            ng_summary = ", ".join(
                f"{c['token']}" for c in non_grammar
            )
            print(f" + [{ng_summary}]")
        else:
            print()

        results = {}
        for hs in level1_hand_sizes:
            RNG.seed(42)  # reset seed for comparability
            p = simulate_level(deck, hs, slot_count, implied, N_SIMS)
            results[hs] = p

        vals = [fmt_pct(results[hs]) for hs in level1_hand_sizes]
        vals.append(threshold_hand_size(results))
        label = f"  {lid} {title}"
        rows.append((label, vals))

    print()
    print_table(rows, col_headers)

    # ------------------------------------------------------------------
    # Part 2: Proposed Level 2 scenarios
    # ------------------------------------------------------------------
    print("\n\n")
    print("PART 2: Proposed Level 2 Scenarios (no implied cards, slot_count=5)")
    print("=" * 78)

    l2_hand_sizes_all = sorted(
        set(hs for s in LEVEL2_SCENARIOS for hs in s["hand_sizes"])
    )
    col_headers2 = [f"HS={hs}" for hs in l2_hand_sizes_all] + [">=33% @"]

    rows2 = []
    for scenario in LEVEL2_SCENARIOS:
        sid = scenario["id"]
        title = scenario["title"]
        deck = build_synthetic_deck(
            card_db, scenario["grammar"],
            scenario["n_curses"], scenario["n_actions"],
        )
        implied = scenario["implied_cards"]
        slot_count = scenario["slot_count"]

        grammar_cards = [c for c in deck if c.get("type") == "grammar"]
        non_grammar = [c for c in deck if c.get("type") != "grammar"]
        token_counts = Counter(c["token"] for c in grammar_cards)
        token_summary = ", ".join(
            f"{tok}x{cnt}" for tok, cnt in sorted(token_counts.items())
        )

        print(f"\n  {sid}: {title}")
        print(f"    Slots: {slot_count}  |  Implied: (none)  |  Deck: {len(deck)} cards")
        print(f"    Grammar: {token_summary}")
        if non_grammar:
            ng_types = Counter(c["type"] for c in non_grammar)
            ng_str = ", ".join(f"{cnt} {t}" for t, cnt in ng_types.items())
            print(f"    Non-grammar: {ng_str}")

        results = {}
        for hs in l2_hand_sizes_all:
            RNG.seed(42)
            p = simulate_level(deck, hs, slot_count, implied, N_SIMS)
            results[hs] = p

        vals = [fmt_pct(results[hs]) for hs in l2_hand_sizes_all]
        vals.append(threshold_hand_size(results))
        label = f"  {sid} {title}"
        rows2.append((label, vals))

    print()
    print_table(rows2, col_headers2)

    # ------------------------------------------------------------------
    # Summary: the 33% threshold table
    # ------------------------------------------------------------------
    print("\n\n")
    print("SUMMARY: Minimum hand size for >= 33% playable-hand probability")
    print("=" * 78)
    # Re-collect all results into a nice summary
    # (We already computed them above, so just print the threshold column)
    print(f"  {'Scenario':<30s}  {'Threshold HS':>14s}")
    print(f"  {'-'*30}  {'-'*14}")

    # Re-run thresholds (already in rows)
    for label, vals in rows:
        th = vals[-1]
        print(f"  {label.strip():<30s}  {th:>14s}")
    for label, vals in rows2:
        th = vals[-1]
        print(f"  {label.strip():<30s}  {th:>14s}")

    print()
    print("=" * 78)
    print(" Analysis complete.")
    print("=" * 78)


if __name__ == "__main__":
    main()
