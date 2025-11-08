# PotionWorld: Game Design Overview

## Game Format: 2D RPG in Godot Engine

PotionWorld is designed as a **2D narrative RPG** built in Godot Engine. This approach offers excellent flexibility for the game's needs:

### Why Godot?
- **Free & Open Source**: No licensing costs, full control
- **GDScript**: Python-like scripting language (easy integration with existing ESENS parser)
- **Excellent 2D Tools**: Built-in sprite handling, animation, UI systems
- **Cross-Platform**: Export to Windows, Mac, Linux, and even web/mobile
- **Lightweight**: Fast iteration and testing
- **Strong Community**: Great documentation and asset libraries
- **Dialogue Systems**: Easy integration with Yarn Spinner or custom dialogue
- **JSON Support**: Perfect for data-driven design (NPCs, recipes, items)

### Visual Style Options
**Option A: Pixel Art** (Recommended for scope)
- Retro aesthetic fits potion-making theme
- Smaller asset requirements
- Can be charming and expressive
- Examples: Stardew Valley, Moonlighter

**Option B: Hand-Drawn 2D**
- More artistic, storybook feel
- Higher art requirements
- Beautiful but slower production
- Examples: Spiritfarer, Gris

**Option C: Minimalist/Geometric**
- Focus on UI and systems over detailed art
- Very fast production
- Clean, modern look
- Examples: Reigns, Card Thief

### Technical Integration
- **ESENS Parser**: Python ESENS_Parser.py can be called from GDScript via OS.execute() or rewritten in GDScript
- **Alternative**: Port ESENS parser directly to GDScript for tighter integration
- **Save System**: Godot's built-in JSON and ConfigFile systems
- **UI Framework**: Godot's Control nodes for inventory, crafting screens
- **Dialogue**: Godot Dialogue Manager plugin or Yarn Spinner

---

## Core Pillars

### 1. **Meaningful Crafting**
Every potion created has purpose and impact. The ESENS notation system (Effect Syntax for Encoded Notation of Substances) provides depth while maintaining clarity—it's a specialized language for describing potion effects that captures everything from who the potion affects (Player/Enemy/Self), to what it does (buffs, debuffs, damage, healing), when effects trigger (on attack, when damaged, at start of turn), and how long they last. This notation gives players precise control over their alchemical creations while keeping the complexity manageable. Crafting is not just about combining ingredients—it's about understanding effects, timing, and consequences.

### 2. **Reactive World**
The world responds to player choices. NPCs remember actions, relationships evolve naturally, and moral decisions create visible ripples across seasons.

### 3. **Life Journey**
The game follows a complete life arc from teenager to elder. Each season introduces age-appropriate challenges, relationships, and growth opportunities.

### 4. **Ethical Alchemy**
Potion-making involves moral dimensions: ingredient sourcing, pricing decisions, knowledge sharing, and the responsibility of wielding alchemical power.

---

## The Five Seasons

PotionWorld follows the player character across five distinct life stages, each with unique challenges, mechanics, and themes:

### **Season 1: Apprentice (Ages 14-18)**
**Theme**: Learning & Foundation
- Attend the Royal Academy of Alchemical Arts
- Master basic crafting and ESENS notation
- Form early friendships and rivalries
- Build Alchemical Knowledge and Precision
- Culminates in Academy Tournament

### **Season 2: Inheritor (Ages 19-24)**
**Theme**: Independence & Responsibility
- Inherit and run grandmother's village shop
- Manage business, customers, and community relationships
- Face ethical pricing and sourcing decisions
- Develop Business Acumen alongside crafting skills
- Navigate village politics and potential plague crisis

### **Season 3: Competitor (Ages 25-30)**
**Theme**: Ambition & Combat
- Join the professional dueling circuit
- Strategic potion-based combat against rivals
- Build Combat Instinct and tactical thinking
- Navigate fame, sponsorships, and competition ethics
- Championship tournament determines standing

### **Season 4: Investigator (Ages 31-40)**
**Theme**: Mystery & Consequence
- Recruited to royal court as alchemical investigator
- Solve poisonings, expose conspiracies, analyze substances
- Political intrigue and moral gray areas
- Intuition and Knowledge reach peak importance
- Uncover deeper world threats

### **Season 5: Master (Ages 41+)**
**Theme**: Legacy & Mentorship
- Establish your alchemical legacy
- Train apprentices and pass on knowledge
- Face world-scale crisis requiring mastery
- Reflect on life choices and their cumulative impact
- Multiple endings based on choices across all seasons

---

## Design Philosophy

**Key Principles:**
1. **Make crafting satisfying and strategic**
2. **Ensure every NPC feels distinct and memorable**
3. **Give players meaningful choices with visible consequences**
4. **Balance complexity with accessibility**
5. **Create a world that reacts to and remembers player actions**

**Success Metrics:**
- Players engage with crafting experimentation
- Players form emotional connections with NPCs
- Players replay to explore different moral paths
- Players feel their choices matter
- Players complete the full life journey (all 5 seasons)

---

## Document Structure

This game design is organized into four interconnected documents:

1. **[GameDesign_Overview.md](GameDesign_Overview.md)** *(this document)* - Vision, pillars, and season structure
2. **[GameDesign_Mechanics.md](GameDesign_Mechanics.md)** - Character systems, crafting, combat, economy, and progression
3. **[GameDesign_Narrative.md](GameDesign_Narrative.md)** - NPCs, relationships, world-building, and quests
4. **[GameDesign_Technical.md](GameDesign_Technical.md)** - UI/UX, accessibility, and Godot implementation

The interconnected systems create emergent gameplay where potion knowledge, social skills, and ethical choices all matter equally to success and satisfaction.
