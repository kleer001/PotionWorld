# Season 0: Production Roadmap
## 30-Minute Playable Demo

**Scope:**
- 4 scenes (Gathering → Crafting → Marcus Choice → Consequence)
- 100% free assets
- Validates: Is crafting + one choice fun?

**Success Metric:** 3/5 playtesters say "I'd play more"

---

## What You're Building

### Scene 1: Garden Gathering
- Text intro
- Click 3 ingredient buttons (Mushroom, Berry, Root)
- Inventory populates
- "Done" button → next scene

### Scene 2: Crafting
- Display recipe: "2 Mushroom + 1 Berry + 1 Sap = Healing Potion"
- Select ingredients from inventory
- "Craft" button
- ESENS parser validates
- Success/failure screen

### Scene 3: Marcus Dilemma
- Text dialogue: Marcus caught experimenting, might be expelled
- 3 choices:
  1. Support him
  2. Stay neutral
  3. Report him
- Store choice

### Scene 4: Consequence
- Load player choice
- Different dialogue per choice
- End card: "This is PotionWorld. Want more?"

---

## Phase 1: Make It Work

### Gathering Scene
- 3 ingredient buttons
- Inventory connection
- Scene transition to crafting

### Crafting Scene
- Recipe display
- Ingredient selector
- ESENS parser integration
- Success/failure screens

### Marcus Dialogue
- Text display system
- 3 choice buttons + branching
- Save choice to player data

### Consequence Scene
- Load choice
- Branch dialogue (3 variants)
- End screen

**Deliverable:** All 4 scenes playable, programmer art

---

## Phase 2: Make It Good

### Free Asset Integration
- UI kit from Kenney.nl
- Ingredient icons from OpenGameArt
- Fantasy font from Google Fonts

### Crafting Polish
- Particles on success
- Screen shake/flash
- Button hover states
- Smooth transitions

### Audio
- Gathering sounds (click, collect)
- Crafting sounds (bubbling, pour, cork pop)
- UI sounds (button clicks)
- Background music (2-3 tracks from Incompetech)

### Choice Polish
- Timer on choice (optional, creates tension)
- Dramatic music cue
- Clearer consequence presentation

**Deliverable:** Looks decent, sounds good, feels satisfying

---

## Phase 3: Validate

### Tutorial Pass
- Tooltips for gathering
- Recipe explanation
- Marcus setup clarity
- "How to Play" screen

### Bug Fixing
- Fix all crashes
- Performance optimization
- Polish pass

### Playtesting
- 5 people play it
- Exit survey (5 questions)
- Collect feedback

### Iteration
- Fix top 3 issues
- Final polish
- Build for distribution

**Deliverable:** Shippable 30-min demo with validation data

---

## Assets (100% Free)

### Visual
- Kenney.nl → UI pack
- OpenGameArt → Ingredient icons
- Google Fonts → 1 readable font

### Audio
- Freesound.org → Gathering, crafting, UI sounds
- Incompetech → Background music loops

---

## Success Criteria

**Phase 1:** All 4 scenes playable, no crashes

**Phase 2:** Free assets integrated, crafting has juice, music enhances

**Phase 3:** 5 people played, 3/5 say "I'd play more"

---

## What Happens Next?

### If 3-5/5 Want More → Validated
- Keep building (60-min demo)
- Post to itch.io
- Prep for Kickstarter
- Continue as passion project

### If 1-2/5 Want More → Iterate
- Analyze feedback
- Rebuild weak parts
- Re-test

### If 0/5 Want More → Pivot
- Different game or graceful exit
- Learned in 3 months vs years

---

## Claude Code Tasks

### Phase 1 Examples
- "Create scene with 3 ingredient buttons"
- "Connect button clicks to inventory"
- "Display recipe requirements from JSON"
- "Call ESENS parser on Craft button"
- "Create dialogue system with 3 choice buttons"
- "Save player choice to JSON"
- "Load choice and branch dialogue"

### Phase 2 Examples
- "Replace default UI with Kenney assets"
- "Add particle effect on successful craft"
- "Add screen shake when potion completes"
- "Add sound effects to gathering buttons"
- "Create volume control sliders"

### Phase 3 Examples
- "Add tooltip system for first-time players"
- "Fix bug where inventory doesn't clear"
- "Add 'How to Play' screen"

---

## Exit Survey Questions

1. Did you finish the 30 minutes?
2. Was crafting fun? (1-5 scale)
3. Did you care about Marcus's choice?
4. Would you play more of this game?
5. What was confusing or broken?

---

## Task Breakdown by Scene

### Gathering
- UI layout (buttons, text)
- Inventory system hookup
- Scene transition

### Crafting
- Recipe UI
- Ingredient selection
- ESENS parser connection
- Result screens

### Marcus
- Dialogue display
- Choice buttons + branching
- Choice storage

### Consequence
- Choice loading
- Dialogue variants (3)
- End card
