#!/usr/bin/env python3
"""
Combinatorial analysis of hand draw probabilities for PotionWorld.

For each level configuration and hand size, uses Monte Carlo simulation
(50,000 trials) to estimate:
  - Probability that a random hand contains at least one valid potion
  - Average number of valid potions per hand

A "valid potion" means: take grammar cards from the hand, try placing them
into open slots (those not already filled by implied cards), concatenate
all tokens left-to-right, and parse_esens() succeeds on that string.
"""

import sys
import random
import time
from itertools import permutations
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from ESENS_Parser import parse_esens, ESENSParseError
from grammar_mvp.cards import load_cards
from grammar_mvp.levels import load_levels, build_level_deck

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NUM_TRIALS = 50_000
HAND_SIZES_TO_TEST = [4, 5, 6, 7]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_open_slots(level):
    """Return indices of slots NOT filled by implied cards."""
    implied_slot_indices = {slot_idx for _, slot_idx in level["implied_cards"]}
    return [i for i in range(level["slot_count"]) if i not in implied_slot_indices]


def build_slot_template(level):
    """Build a list of length slot_count with implied tokens pre-filled.

    Non-implied slots are None.
    """
    slots = [None] * level["slot_count"]
    for token, slot_idx in level["implied_cards"]:
        if slot_idx < len(slots):
            slots[slot_idx] = token
    return slots


def check_hand_for_valid_potions(hand_cards, slot_template, open_slot_indices):
    """Given a hand of card dicts, check how many valid potions can be formed.

    We extract grammar tokens from the hand, then try every way of placing
    a subset of them into the open slots. For each arrangement, concatenate
    all slot tokens left-to-right and try parse_esens().

    To keep it tractable, we limit permutations:
    - We only try subsets of size exactly equal to len(open_slot_indices)
      (filling all open slots) because ESENS requires a complete notation.
    - If there are more grammar cards than open slots, we try all
      combinations of choosing len(open_slots) cards and all their
      permutations.
    - We cap the number of permutations we actually test to avoid
      combinatorial explosion (shouldn't be an issue for slot counts <= 7).

    Returns: count of distinct valid potions found.
    """
    # Extract grammar tokens from hand
    grammar_tokens = []
    for card in hand_cards:
        if card.get("type") == "grammar":
            grammar_tokens.append(card["token"])

    num_open = len(open_slot_indices)
    if num_open == 0:
        # All slots are implied — just check if the implied string parses
        notation = "".join(t for t in slot_template if t is not None)
        if notation:
            try:
                parse_esens(notation, explain=False)
                return 1
            except ESENSParseError:
                return 0
        return 0

    if len(grammar_tokens) < num_open:
        # Not enough grammar cards to fill all open slots — but partial
        # fills might still be valid if the resulting string parses.
        # Try placing cards into subsets of open slots.
        # For simplicity and because the ESENS grammar needs Target+Effect+Stat
        # at minimum (3 tokens), partial fills of fewer tokens are unlikely
        # to produce valid results. We'll still try them.
        return _try_partial_fills(grammar_tokens, slot_template, open_slot_indices)

    # Enough grammar cards to fill all open slots
    valid_count = 0
    seen = set()

    # If we have exactly the right number, just try all permutations
    if len(grammar_tokens) == num_open:
        for perm in permutations(grammar_tokens):
            key = perm
            if key in seen:
                continue
            seen.add(key)
            notation = _build_notation(slot_template, open_slot_indices, perm)
            if _is_valid(notation):
                valid_count += 1
    else:
        # More grammar cards than open slots — choose subsets
        # Use itertools.combinations for choosing, then permutations for ordering
        from itertools import combinations
        for combo in combinations(range(len(grammar_tokens)), num_open):
            chosen = tuple(grammar_tokens[i] for i in combo)
            for perm in permutations(chosen):
                key = perm
                if key in seen:
                    continue
                seen.add(key)
                notation = _build_notation(slot_template, open_slot_indices, perm)
                if _is_valid(notation):
                    valid_count += 1

    return valid_count


def _try_partial_fills(grammar_tokens, slot_template, open_slot_indices):
    """Try placing grammar tokens into subsets of open slots."""
    from itertools import combinations
    valid_count = 0
    seen = set()
    num_tokens = len(grammar_tokens)

    # Try filling subsets of open slots of size num_tokens
    for slot_combo in combinations(range(len(open_slot_indices)), num_tokens):
        chosen_open = [open_slot_indices[i] for i in slot_combo]
        for perm in permutations(grammar_tokens):
            # Build a partial slot template
            slots = list(slot_template)
            for idx, token in zip(chosen_open, perm):
                slots[idx] = token
            # Concatenate only the filled slots
            notation = "".join(t for t in slots if t is not None)
            key = (tuple(chosen_open), perm)
            if key in seen:
                continue
            seen.add(key)
            if notation and _is_valid(notation):
                valid_count += 1

    return valid_count


def _build_notation(slot_template, open_slot_indices, tokens_for_open):
    """Place tokens into open slots and concatenate all slots."""
    slots = list(slot_template)
    for idx, token in zip(open_slot_indices, tokens_for_open):
        slots[idx] = token
    return "".join(t for t in slots if t is not None)


def _is_valid(notation):
    """Return True if notation is a valid ESENS string."""
    try:
        parse_esens(notation, explain=False)
        return True
    except (ESENSParseError, Exception):
        return False


# ---------------------------------------------------------------------------
# Monte Carlo simulation
# ---------------------------------------------------------------------------

def run_simulation(deck_cards, level, hand_size, num_trials=NUM_TRIALS):
    """Run Monte Carlo simulation for a given deck/level/hand_size.

    Returns (prob_at_least_one, avg_valid_count).
    """
    slot_template = build_slot_template(level)
    open_slots = get_open_slots(level)

    hands_with_valid = 0
    total_valid = 0

    for _ in range(num_trials):
        # Draw a random hand
        if hand_size >= len(deck_cards):
            hand = list(deck_cards)
        else:
            hand = random.sample(deck_cards, hand_size)

        count = check_hand_for_valid_potions(hand, slot_template, open_slots)
        if count > 0:
            hands_with_valid += 1
        total_valid += count

    prob = hands_with_valid / num_trials
    avg = total_valid / num_trials
    return prob, avg


# ---------------------------------------------------------------------------
# Scenario builders
# ---------------------------------------------------------------------------

def build_proposed_level2_deck(card_db):
    """Proposed level 2: no implied cards, 5 open slots.

    Deck: P x3, E x3, + x3, - x3, H x3, S x2, D x2, 5 x3, 10 x2
    plus action_redraw and action_grace.
    """
    token_to_card = {}
    for cid, cdata in card_db.items():
        if cdata.get("type") == "grammar":
            tok = cdata["token"]
            if tok not in token_to_card:
                token_to_card[tok] = cdata

    deck = []
    composition = [
        ("P", 3), ("E", 3), ("+", 3), ("-", 3),
        ("H", 3), ("S", 2), ("D", 2), ("5", 3), ("10", 2),
    ]
    for token, count in composition:
        if token in token_to_card:
            for _ in range(count):
                deck.append(dict(token_to_card[token]))

    # Add action cards
    for aid in ["action_redraw", "action_grace"]:
        if aid in card_db:
            deck.append(dict(card_db[aid]))

    return deck


def build_proposed_level2_level():
    """Level definition for proposed level 2."""
    return {
        "id": "proposed-2",
        "title": "Proposed Level 2",
        "implied_cards": [],
        "symbols": [],
        "slot_count": 5,
        "hand_size": 5,
        "deck_extras": [],
        "mana": 10,
    }


def build_cursed_level2_deck(card_db):
    """Same as proposed level 2 but add 3 dead_weight curse cards."""
    deck = build_proposed_level2_deck(card_db)
    # Add 3 curse_dead_weight cards
    if "curse_dead_weight" in card_db:
        for _ in range(3):
            deck.append(dict(card_db["curse_dead_weight"]))
    return deck


def build_cursed_level2_level():
    """Level definition for cursed level 2."""
    return {
        "id": "cursed-2",
        "title": "Cursed Level 2",
        "implied_cards": [],
        "symbols": [],
        "slot_count": 5,
        "hand_size": 5,
        "deck_extras": [],
        "mana": 10,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 90)
    print("PotionWorld — Hand Draw Probability Analysis (Monte Carlo)")
    print(f"Trials per configuration: {NUM_TRIALS:,}")
    print("=" * 90)

    card_db = load_cards()
    levels = load_levels()

    # Collect all (label, deck, level_def, hand_size) configs to run
    configs = []

    # --- Part 1 & 2: Existing levels at their native hand size + test sizes ---
    for level in levels:
        deck = build_level_deck(level, card_db)
        native_hs = level["hand_size"]

        # Native hand size
        configs.append((level["id"], deck, level, native_hs, True))

        # Extra hand sizes
        for hs in HAND_SIZES_TO_TEST:
            if hs != native_hs:
                configs.append((level["id"], deck, level, hs, False))

    # --- Part 3: Proposed level 2 ---
    prop_deck = build_proposed_level2_deck(card_db)
    prop_level = build_proposed_level2_level()
    for hs in HAND_SIZES_TO_TEST:
        native = (hs == prop_level["hand_size"])
        configs.append((prop_level["id"], prop_deck, prop_level, hs, native))

    # --- Part 4: Cursed level 2 ---
    cursed_deck = build_cursed_level2_deck(card_db)
    cursed_level = build_cursed_level2_level()
    for hs in HAND_SIZES_TO_TEST:
        native = (hs == cursed_level["hand_size"])
        configs.append((cursed_level["id"], cursed_deck, cursed_level, hs, native))

    # Print table header
    print()
    print(f"{'Level ID':<14} {'Hand':>4} {'Deck':>4} {'Slots':>5} "
          f"{'Implied':>7} {'Open':>4}   "
          f"{'P(>=1 valid)':>13} {'Avg valid/hand':>14}  {'Note'}")
    print("-" * 90)

    start_all = time.time()
    current_section = None

    for level_id, deck, level_def, hand_size, is_native in configs:
        # Section headers
        if level_id != current_section:
            current_section = level_id
            # Describe the level briefly
            implied = level_def["implied_cards"]
            impl_str = ", ".join(f"{tok}@{si}" for tok, si in implied) if implied else "(none)"
            deck_grammar = [c for c in deck if c.get("type") == "grammar"]
            deck_action = [c for c in deck if c.get("type") == "action"]
            deck_curse = [c for c in deck if c.get("type") == "curse"]
            print()
            title = level_def.get("title", level_id)
            print(f"  --- {level_id}: {title} ---")
            print(f"      Deck: {len(deck)} cards "
                  f"({len(deck_grammar)} grammar, {len(deck_action)} action, {len(deck_curse)} curse)")
            print(f"      Slots: {level_def['slot_count']}, "
                  f"Implied: {impl_str}")
            # Show grammar token distribution
            from collections import Counter
            token_counts = Counter(c["token"] for c in deck_grammar)
            dist_str = ", ".join(f"{tok}x{cnt}" for tok, cnt in sorted(token_counts.items()))
            print(f"      Grammar tokens: {dist_str}")
            print()

        # Run simulation
        t0 = time.time()
        prob, avg = run_simulation(deck, level_def, hand_size, NUM_TRIALS)
        elapsed = time.time() - t0

        open_count = len(get_open_slots(level_def))
        implied_count = len(level_def["implied_cards"])
        note = "* native" if is_native else ""

        print(f"  {level_id:<12} {hand_size:>4} {len(deck):>4} "
              f"{level_def['slot_count']:>5} {implied_count:>7} {open_count:>4}   "
              f"{prob:>12.1%} {avg:>14.3f}  {note}"
              f"  ({elapsed:.1f}s)")

    total_time = time.time() - start_all
    print()
    print("-" * 90)
    print(f"Total time: {total_time:.1f}s")
    print()
    print("Notes:")
    print("  * native = this is the level's actual configured hand_size")
    print("  P(>=1 valid) = probability of drawing at least one valid potion")
    print("  Avg valid/hand = average number of distinct valid potions per hand")
    print("  Valid potion = grammar tokens placed in open slots such that the")
    print("    full left-to-right concatenation passes parse_esens().")
    print()


if __name__ == "__main__":
    main()
