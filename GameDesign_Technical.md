# PotionWorld: Technical Design

*See also: [Overview](GameDesign_Overview.md) | [Mechanics](GameDesign_Mechanics.md) | [Narrative](GameDesign_Narrative.md)*

---

## UI/UX Design Philosophy

### Core Principles

1. **Clarity First**: ESENS notation visible but explained
2. **Contextual Help**: Tutorials available when needed
3. **Efficient Navigation**: Quick access to common functions
4. **Visual Feedback**: Clear indication of success, failure, changes
5. **Accessibility**: Colorblind modes, text scaling, remappable controls

### Godot-Specific UI Implementation

**Control Nodes Used:**
- **Panel/MarginContainer**: Main UI containers
- **VBoxContainer/HBoxContainer**: Organized layouts
- **ItemList/Tree**: Inventory and recipe displays
- **RichTextLabel**: Formatted dialogue and descriptions with ESENS notation highlighting
- **TabContainer**: Switching between inventory sections
- **ProgressBar**: Crafting progress, stat displays, affinity meters
- **TextureRect**: Item icons, character portraits, ingredient images
- **PopupPanel**: Tooltips, detail windows, confirmation dialogs

**UI Theme:**
- Custom Godot theme for consistent styling
- Color palette for elements (Fire=red, Water=blue, etc.)
- Custom fonts for readability and atmosphere
- Particle effects for crafting success/failure

### Key UI Screens

**Main HUD:**
- Health/status indicators (in combat)
- Current season and date
- Active quest tracker
- Quick-access inventory (hotbar)
- Affinity indicators for nearby NPCs

**Crafting Screen:**
- Recipe view (ESENS notation + description)
- Ingredient slots with drag-and-drop
- Tools and equipment status
- Success chance indicator
- Quality potential display

**Inventory Screen:**
- Tabbed organization (Ingredients, Potions, Equipment, Recipes)
- Sort and filter options
- Quick-craft from recipe book
- Item detail pop-ups with lore

**Dialogue Screen:**
- Character portrait with expression
- Affinity indicator (heart/star system)
- Personality hints (subtle icons)
- Dialogue history scroll
- Choice preview (shows potential reactions)

**Shop Management Screen (Season 2):**
- Display shelves (what customers see)
- Storage management
- Customer list with preferences
- Ledger and finances
- Shop upgrade options

---

## Accessibility & Quality of Life

### Accessibility Features
- Text size adjustment (80% to 150%)
- Colorblind modes (Deuteranopia, Protanopia, Tritanopia)
- High contrast mode
- Screen reader support for UI elements
- Remappable controls
- Auto-save and multiple save slots

### Quality of Life Features
- Fast travel (Season 2+)
- Batch crafting for mastered recipes
- Ingredient highlighting in world
- Recipe favoriting
- Quest markers and waypoints
- Skip dialogue option (for replays)
- Comprehensive glossary and help system
- Tutorial replay option
- New Game+ with bonuses

---

## Design Priorities & Success Metrics

### Design Priorities
1. Make crafting satisfying and strategic
2. Ensure every NPC feels distinct and memorable
3. Give players meaningful choices with visible consequences
4. Balance complexity with accessibility
5. Create a world that reacts to and remembers player actions

### Success Metrics
- Players engage with crafting experimentation
- Players form emotional connections with NPCs
- Players replay to explore different moral paths
- Players feel their choices matter
- Players complete the full life journey (all 5 seasons)

---

## Conclusion

PotionWorld combines deep systems with meaningful narrative to create a unique life-journey RPG. The ESENS notation system provides rich crafting depth, while the Big 5 personality and affinity systems create believable, reactive relationships.

The interconnected systems create emergent gameplay where potion knowledge, social skills, and ethical choices all matter equally to success and satisfaction.
