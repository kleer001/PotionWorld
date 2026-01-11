# Enhanced Status Effect Notation System (ESENS)

A parser and validator for a compact notation system used to describe status effects in games.

## Overview

ESENS is a powerful notation system that allows game designers and developers to concisely define complex status effects. This Python implementation provides:

- **Syntax validation**: Strict checking of ESENS notation against the formal grammar
- **Object representation**: Converts notations into structured data objects
- **Human-readable explanations**: Translates the compact notation into clear English descriptions

## Installation

Clone this repository or download the source files.

```bash
git clone https://github.com/yourusername/esens-parser.git
cd esens-parser
```

## Quick Start

### Command-line Interface

```bash
# Parse a notation with explanation
python esens_cli.py "P+S10%3T"

# Validate multiple notations from a file
python esens_cli.py -v -f my_notations.txt

# Interactive mode
python esens_cli.py -i

# Output as JSON
python esens_cli.py -j "P+S10%3T.F"
```

### Python API

```python
from esens_parser import parse_esens, validate_esens, ESENSParseError

# Parse a notation with explanation
result = parse_esens("P+S10%3T")
print(result["explanation"])  # "Player gains strength by 10% for 3 turns"
print(result["dict"])         # Dictionary representation

# Validate syntax without parsing
try:
    is_valid = validate_esens("E-D15C")
    print("Valid notation")
except ESENSParseError as e:
    print(f"Invalid notation: {e}")
```

## ESENS Notation Examples

Basic examples:

- `P+S10%3T` - Player gains 10% strength for 3 turns
- `E-D15C` - Enemy loses 15 defense for combat duration
- `P#Stun1T` - Player stunned for 1 turn
- `X-H5` - All enemies take 5 damage

With extended components:

- `P+S10%3T.ST` - Player gains 10% strength for 3 turns, stacking allowed
- `P+S10%3T>A.F` - Player gains 10% Fire strength for 3 turns when attacking
- `E#Burn3T^S.DOT` - Enemy burned for 3 damage at start of turn, damage over time
- `P+S30%2T>A.F.S3.~P.?HP<30%` - Player gains +30% Fire strength for 2 turns when attacking, stacks up to 3 times, linked to player, only activates when player's HP is below 30%

## Notation System Reference

### Core Structure

`[Target][Effect][Stat][Magnitude][Duration][Trigger][Element][Special...]`

### Components

1. **Target**: Who receives the effect 
   - `P`: Player
   - `E`: Enemy
   - `A`: All allies
   - `X`: All enemies
   - `G`: Global (affects everyone)

2. **Effect Type**: What happens
   - `+`: Increase
   - `-`: Decrease
   - `=`: Set to exact value
   - `*`: Multiply (percentage modifier)
   - `!`: Nullify/Prevent
   - `#`: Special condition (stun, burn, etc.)

3. **Stat Affected**: What changes
   - `S`: Strength/Attack
   - `D`: Defense
   - `E`: Element
   - `L`: Luck
   - `G`: Gold
   - `H`: Health
   - `M`: Movement
   - `I`: Initiative/Speed
   - `C`: Critical hit chance
   - `R`: Resistance

4. **Magnitude**: How much
   - Number: Flat value (10)
   - `%`: Percentage (25%)
   - `F`: Full/Max value

5. **Duration**: How long
   - `nT`: n Turns (3T = 3 turns)
   - `n-mT`: Random duration between n and m turns (3-5T)
   - `C`: Combat duration
   - `P`: Permanent
   - `A`: Single action/instant

6. **Trigger Condition**: When activated
   - `>A`: On attack
   - `<D`: On being hit/defending
   - `^S`: Start of turn
   - `vE`: End of turn
   - `?n%`: n% chance each turn
   - `K`: On kill

7. **Element Specificity**: What element it relates to
   - `F`: Fire
   - `W`: Water
   - `E`: Earth
   - `S`: Sky
   - `D`: Death

8. **Special Flags**:
   - `ST`: Stacking allowed
   - `AR`: Area effect
   - `DOT`: Damage over time

(See full documentation for details on all extended components)

## Development Status

This is an early implementation that supports:
- Core component parsing
- Basic extended component recognition
- Strict syntax validation
- Human-readable translations

Future enhancements:
- Complete parsing of all extended components
- Support for complex conditional expressions
- Multi-effect chaining
- Performance optimizations

## License

[MIT License](LICENSE)
