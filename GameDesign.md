# PotionWorld: Game Design Documentation

Welcome to the PotionWorld game design documentation. This guide is organized into four interconnected documents covering different aspects of the game.

---

## Documentation Structure

### 📖 [GameDesign_Overview.md](GameDesign_Overview.md)
**Core vision, pillars, and game structure**
- Game format and Godot engine rationale
- Four core pillars (Meaningful Crafting, Reactive World, Life Journey, Ethical Alchemy)
- Five season structure (Apprentice → Inheritor → Competitor → Investigator → Master)
- Design philosophy and success metrics

**Start here** for the high-level vision and what makes PotionWorld unique.

---

### ⚙️ [GameDesign_Mechanics.md](GameDesign_Mechanics.md)
**All game systems and mechanical design**
- Character Systems (attributes, progression, specializations)
- Inventory Systems (ingredients, potions, equipment, recipes)
- Crafting Systems (ESENS-based brewing, experimentation, quality)
- Combat & Dueling (turn-based potion combat, AI personality system)
- Economy & Trading (pricing, shop management, merchants)
- Progression Systems (experience, reputation, achievements, season transitions)

**Go here** for detailed mechanical specifications and formulas.

---

### 📚 [GameDesign_Narrative.md](GameDesign_Narrative.md)
**Story, characters, world-building, and quests**
- NPC Relationship Systems (Big 5 personality, affinity mechanics, key NPCs)
- World & Environment (season-based regions, time system, world reactivity)
- Quest & Event Systems (quest types, events, moral choice framework)
- Dialogue System (node-based, personality decorators)

**Go here** for narrative design and character development.

---

### 🎨 [GameDesign_Technical.md](GameDesign_Technical.md)
**UI/UX, accessibility, and implementation details**
- UI/UX Design Philosophy (core principles, key screens)
- Godot-Specific Implementation (control nodes, UI theme)
- Accessibility Features (colorblind modes, text scaling, screen readers)
- Quality of Life Features (fast travel, batch crafting, tutorials)
- Design Priorities & Success Metrics

**Go here** for implementation guidance and technical specifications.

---

## Quick Reference

### The Five Seasons
1. **Apprentice (14-18)**: Learn at the Royal Academy
2. **Inheritor (19-24)**: Run grandmother's village shop
3. **Competitor (25-30)**: Join the professional dueling circuit
4. **Investigator (31-40)**: Solve mysteries for the royal court
5. **Master (41+)**: Establish your legacy and mentor others

### Core Systems at a Glance
- **ESENS Notation**: Specialized language for describing potion effects (Effect Syntax for Encoded Notation of Substances)
- **6 Core Attributes**: Alchemical Knowledge, Precision, Intuition, Reputation, Business Acumen, Combat Instinct
- **Big 5 Personalities**: NPCs react based on Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- **Affinity System**: NPC relationships range from -5 (Nemesis) to +5 (Devoted)
- **17 Ingredient Types**: Each with unique properties and rarity levels
- **5 Specializations**: Choose one per season to create unique character builds

### Platform & Technology
- **Engine**: Godot Engine (free, open-source, GDScript)
- **Genre**: 2D Narrative RPG
- **Visual Style**: Pixel art recommended (Stardew Valley, Moonlighter style)
- **Target Platforms**: Windows, Mac, Linux (with potential web/mobile exports)

---

## Design Philosophy

PotionWorld is built on interconnected systems where:
- **Crafting** is strategic and meaningful, not just resource combination
- **NPCs** are believable individuals with distinct personalities and memories
- **Choices** have visible consequences that echo across seasons
- **Complexity** is balanced with accessibility through clear design
- **The world** reacts to and remembers player actions

Every potion tells a story. Every relationship matters. Every choice shapes your legacy.

---

## Getting Started

**New to the project?** Start with [GameDesign_Overview.md](GameDesign_Overview.md) to understand the vision.

**Implementing a feature?** Jump to the relevant specialized document:
- Building crafting/combat → [Mechanics](GameDesign_Mechanics.md)
- Creating NPCs/quests → [Narrative](GameDesign_Narrative.md)
- Designing UI/accessibility → [Technical](GameDesign_Technical.md)

**Looking for something specific?** Each document has its own table of contents for easy navigation.
