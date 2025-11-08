# PotionWorld: High-Level Development Roadmap

## Project Vision
PotionWorld is a narrative-driven RPG that follows the complete life journey of a potion maker, from apprentice to master. The game combines deep crafting mechanics using the ESENS notation system with meaningful character relationships and moral choices that reshape the game world.

---

## Development Phases

### Phase 1: Foundation & Core Systems (Months 1-4)

#### 1.1 Technical Infrastructure
- **Godot Engine Setup**
  - Install Godot 4.x and configure project
  - Establish project structure (scenes, scripts, resources, data)
  - Set up version control (Git with .gitignore for Godot)
  - Configure export templates for target platforms
  - Install essential plugins (Dialogue Manager, etc.)

- **ESENS Parser Integration**
  - Complete Python ESENS parser implementation ✓ (partially complete)
  - Add comprehensive unit tests for all notation patterns
  - **Option A**: Port ESENS parser to GDScript for native integration
  - **Option B**: Create GDScript wrapper to call Python parser
  - Optimize parser performance for real-time use
  - Create visual debugging tools for status effects in Godot UI

- **Data Management System**
  - Design JSON/database schema for game data
  - Implement save/load system
  - Create data validation tools
  - Set up character/NPC data structures

#### 1.2 Core Mechanics
- **Basic UI Framework**
  - Main menu and navigation
  - HUD and status displays
  - Inventory screen mockups
  - Dialogue system framework

- **Character System Foundation**
  - Player character data structure
  - NPC Big 5 personality implementation
  - Affinity tracking system
  - Basic character state management

- **Ingredient System**
  - Define all 17 ingredient types
  - Create ingredient data models
  - Implement basic inventory management
  - Design ingredient gathering mechanics

**Milestone 1**: Playable prototype with basic UI, character creation, and ingredient collection

---

### Phase 2: Season 1 - The Apprentice (Months 5-8)

#### 2.1 Apprentice Core Gameplay
- **Academy Setting**
  - Create academy environment and locations
  - Design classroom interactions
  - Implement lesson system for ESENS learning
  - Create academy schedule and calendar system

- **Basic Potion Crafting**
  - Implement 3-4 component potion recipes
  - Create crafting UI with ESENS visualization
  - Add success/failure mechanics
  - Design ingredient combination rules

- **Tutorial System**
  - Progressive ESENS notation tutorials
  - Guided crafting exercises
  - Character interaction tutorials
  - Moral choice introduction

#### 2.2 Character Relationships
- **Instructor Thornwood**
  - Full dialogue tree implementation
  - Personality-based reaction system
  - Affinity tracking and thresholds
  - Special events and teaching moments

- **Fellow Students (3-4 key NPCs)**
  - Unique personalities and motivations
  - Competition and cooperation mechanics
  - Friendship/rivalry systems
  - Impact on academy reputation

#### 2.3 Season 1 Content
- **Main Quest Line**
  - 10-15 structured lessons
  - 5-7 key moral choice moments
  - Academy Tournament climax event
  - Season transition to inheritor phase

- **Side Activities**
  - Ingredient gathering expeditions
  - Study groups and social events
  - Extra credit assignments
  - Secret experiments and discoveries

**Milestone 2**: Complete Season 1 with full academy experience, 20+ potions, and branching moral choices

---

### Phase 3: Intermediate Seasons (Months 9-16)

#### 3.1 Season 2 - The Inheritor (Months 9-11)
- **Village Shop Management**
  - Shop interface and customer system
  - Pricing and economy mechanics
  - Inventory management expansion
  - Recipe book deciphering puzzles

- **Intermediate Crafting**
  - 7-10 component potions
  - Rarer ingredient types (Crystals, Tree Sap, Seeds)
  - Customer-specific ailment system
  - Quality and efficacy metrics

- **Community Relationships**
  - Village healer and elder NPCs
  - Customer relationship management
  - Village reputation system
  - Epidemic event and moral choices

#### 3.2 Season 3 - The Competitor (Months 12-14)
- **Combat/Dueling System**
  - Turn-based potion combat mechanics
  - Strategic timing and counter-play
  - Combat ESENS implementation (triggers, chains)
  - Opponent AI with personality-based tactics

- **Advanced Crafting**
  - Combat-focused potions
  - Rare materials (Minerals, Insect Parts, Oils)
  - Status effect combinations and synergies
  - Pre-combat preparation strategies

- **Tournament Circuit**
  - Ranking and progression system
  - Multiple opponents with unique styles
  - Dueling house mechanics
  - Championship event and corruption storyline

#### 3.3 Season 4 - The Investigator (Months 15-16)
- **Analysis Mechanics**
  - Reverse-engineering potion effects
  - Mystery solving through alchemy
  - Counter-potion creation
  - Research and experimentation system

- **Exotic Ingredients**
  - Rare components (Spores, Feathers, Honey, Fish Scales)
  - Source tracking and ethical sourcing
  - Endangered species dilemmas
  - Black market vs. legitimate suppliers

- **Royal Court Politics**
  - Political faction system
  - Influence and reputation mechanics
  - Conspiracy investigation storyline
  - Mind control counter-potion climax

**Milestone 3**: Seasons 2-4 complete with evolving mechanics, 100+ potions, and complex moral systems

---

### Phase 4: Endgame & Polish (Months 17-20)

#### 4.1 Season 5 - The Master
- **Legacy Systems**
  - Business empire or research institution management
  - Apprentice training mechanics
  - Legacy-level potion creation
  - Metamorphic/Gobstopper effect implementation

- **Ultimate Challenge**
  - Elemental imbalance world crisis
  - Quintessence potion requiring all 17 ingredient types
  - Previous moral choices impact final outcome
  - Multiple endings based on player's life journey

- **Character Continuity**
  - Long-term relationship payoffs
  - Recurring character appearances
  - Reputation and renown systems
  - "Potion Book of Life" completion

#### 4.2 Content Completion
- **Remaining Potions**
  - All 17 ingredient type representations
  - Legendary and unique potions
  - Player-created innovations
  - Community-submitted recipes

- **NPC Development**
  - Complete all 4 main character arcs
  - Flesh out 12 secondary characters
  - Dynamic NPC aging and life changes
  - Memory system full implementation

#### 4.3 Polish & Quality Assurance
- **Technical Polish**
  - Performance optimization
  - Bug fixing and stability
  - UI/UX refinement
  - Accessibility features

- **Content Polish**
  - Writing and dialogue editing
  - Balance tuning for all systems
  - Achievement/trophy system
  - New Game+ features

**Milestone 4**: Complete game with all 5 seasons, 200+ potions, fully realized world, and multiple endings

---

### Phase 5: Post-Launch Support (Months 21+)

#### 5.1 Community Content
- **Modding Support**
  - Custom potion creation tools
  - NPC personality editor
  - Quest/event scripting
  - Community recipe database

- **DLC/Expansions (Optional)**
  - Additional side stories
  - New ingredient types and potion schools
  - Alternative career paths (poison maker, perfumer)
  - Multiplayer potion dueling

#### 5.2 Live Operations
- **Updates & Patches**
  - Regular bug fixes
  - Balance adjustments
  - Quality of life improvements
  - Seasonal events

- **Community Engagement**
  - Player feedback integration
  - Regular content updates
  - Speedrun and challenge modes
  - Community spotlight features

---

## Technical Architecture

### Architectural Patterns

#### System-Local Data Structures
Each system owns its data structures in dedicated `data_structures.py` files:

- `src/core/data_structures.py` - Only shared types (`Quality`, `Personality`)
- `src/crafting/data_structures.py` - Recipe, Potion, CraftInput, etc.
- `src/economy/data_structures.py` - Transaction, Wallet, PriceModifiers, etc.
- `src/combat/data_structures.py` - Combatant, StatusEffect, Trigger, etc.
- `src/relationships/data_structures.py` - NPC, Memory, Action, etc.

Benefits: Clear ownership, isolation, reduced coupling, SOLID compliance.

### Core Systems

#### 1. ESENS Engine
- **Parser & Validator**
  - Real-time notation parsing
  - Error handling and debugging
  - Performance optimization
  - Extensibility for new components

- **Effect Resolver**
  - Status effect application
  - Duration and trigger management
  - Stacking and interaction handling
  - Visual feedback system

#### 2. Character Management
- **Player System**
  - Stats and progression
  - Skill trees (if applicable)
  - Inventory management
  - Reputation tracking

- **NPC System**
  - Big 5 personality engine
  - Affinity calculation and decay
  - Memory and relationship tracking
  - Dialogue node management

#### 3. Crafting System
- **Recipe Management**
  - Recipe discovery and learning
  - Ingredient validation
  - Success calculation
  - Quality determination

- **Potion Effects**
  - ESENS-to-gameplay translation
  - Effect duration tracking
  - Potion consumption mechanics
  - Storage and degradation

#### 4. World State
- **Time Management**
  - Season transitions
  - Character aging
  - World event triggers
  - Calendar and scheduling

- **Consequence System**
  - Moral choice tracking
  - World state modifications
  - Long-term impact calculation
  - Alternative path unlocking

### Data Structures

#### Architecture
Data structures are organized by system ownership:
- Each system has its own `data_structures.py`
- Only truly shared types live in `src/core/data_structures.py`
- Systems import from each other when needed (e.g., Economy imports Potion from Crafting)

#### JSON Schema Examples
```json
{
  "NPC": {
    "id": "string",
    "name": "string",
    "personality": {
      "openness": [-1, 0, 1],
      "conscientiousness": [-1, 0, 1],
      "extraversion": [-1, 0, 1],
      "agreeableness": [-1, 0, 1],
      "neuroticism": [-1, 0, 1]
    },
    "affinity": 0,
    "memories": [],
    "dialogue_tree": "reference"
  },

  "Potion": {
    "id": "string",
    "name": "string",
    "esens_notation": "string",
    "ingredients": [],
    "difficulty": "number",
    "discovery_season": "number",
    "effects": []
  },

  "Ingredient": {
    "id": "string",
    "name": "string",
    "type": "string",
    "rarity": "string",
    "properties": {},
    "sources": []
  }
}
```

---

## Resource Requirements

### Team Composition (Recommended)
- **1 Lead Developer/Programmer** - Core systems, engine integration
- **1 Gameplay Programmer** - Mechanics, UI, combat systems
- **1 Narrative Designer/Writer** - Dialogue, quests, world-building
- **1 Game Designer** - Balance, progression, systems design
- **1 UI/UX Designer** - Interface design and user experience
- **1 2D/3D Artist** - Characters, environments, items
- **1 Sound Designer** (part-time) - Music, SFX, ambient audio
- **1 QA Tester** (part-time in later phases)

### Technology Stack
- **Game Engine**: Godot 4.x
- **Languages**: GDScript (primary), Python (ESENS parser)
- **Data Management**: JSON (Godot's built-in JSON parser)
- **Dialogue System**: Godot Dialogue Manager plugin or custom GDScript
- **Version Control**: Git (GitHub/GitLab)
- **Project Management**: Trello, Notion, or GitHub Projects
- **Art Tools**: Aseprite (pixel art), GIMP/Krita (2D art), or Inkscape (vector)
- **Testing**: Godot's built-in unit testing framework (GUT)

### Asset Requirements
- **Sprites/Models**:
  - 20+ character designs
  - 100+ ingredient illustrations
  - 200+ potion bottle variations
  - 30+ environment backgrounds

- **Audio**:
  - 20+ music tracks (varying by season/setting)
  - 200+ sound effects
  - Optional voice acting for key characters

---

## Risk Management

### Technical Risks
- **ESENS Complexity**: Notation system may be too complex for players
  - *Mitigation*: Progressive tutorials, simplified notation for early game

- **Save System Complexity**: Many variables to track across seasons
  - *Mitigation*: Robust data structure design, regular testing

- **Performance**: Status effect calculations may impact performance
  - *Mitigation*: Optimize parser, use caching, profile regularly

### Design Risks
- **Pacing**: Five seasons may feel too long or uneven
  - *Mitigation*: Extensive playtesting, optional season skipping

- **Moral Choice Clarity**: Players may not understand choice consequences
  - *Mitigation*: Clear UI feedback, journal tracking choices

- **Relationship Complexity**: Big 5 system may be opaque to players
  - *Mitigation*: Visual feedback, personality indicators, clearer reactions

### Content Risks
- **Writing Volume**: Massive amount of dialogue and content needed
  - *Mitigation*: Procedural dialogue generation, template-based responses

- **Balance**: 200+ potions need to be balanced and useful
  - *Mitigation*: Iterative balancing, community feedback, data-driven adjustments

---

## Success Metrics

### During Development
- Milestone completion on schedule
- Bug count and severity tracking
- Playtest feedback scores
- System performance benchmarks

### Post-Launch
- Player retention (% completing each season)
- Average playtime per season
- Achievement completion rates
- Player-created content (if applicable)
- Review scores and player sentiment
- Community engagement metrics

---

## Alternative Approaches

### Simplified Scope (If Resources Limited)
- **Reduce to 3 Seasons**: Apprentice, Competitor, Master
- **Fewer Potions**: 50-75 core potions instead of 200+
- **Streamlined Relationships**: 8 total NPCs instead of 16
- **Linear Progression**: Fewer branching paths

### Expanded Scope (If Resources Abundant)
- **Additional Seasons**: Retirement, Mentorship, Legend
- **Multiple Protagonists**: Different starting backgrounds
- **Open World**: Non-linear season progression
- **Multiplayer**: Co-op potion crafting, competitive dueling

---

## Conclusion

PotionWorld represents an ambitious blend of narrative RPG and crafting simulation with unique mechanics centered around the ESENS notation system. The phased development approach allows for iterative refinement while building toward a complete five-season experience.

**Key Success Factors:**
1. Solid technical foundation with ESENS engine
2. Compelling characters with meaningful relationships
3. Satisfying crafting progression across all seasons
4. Impactful moral choices with visible consequences
5. Strong narrative threading character's entire life journey

**Next Immediate Steps:**
1. Complete ESENS parser testing and optimization
2. Finalize Season 1 game design document
3. Create vertical slice prototype (first 30 minutes of gameplay)
4. Begin asset production pipeline
5. Establish regular playtesting schedule

With careful execution and community feedback integration, PotionWorld can deliver a unique and memorable gaming experience that resonates with players who enjoy deep crafting systems, meaningful choices, and character-driven narratives.
