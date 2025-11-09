# Season 0: Production Roadmap (Bird's Eye View)
## The Demo - 6-Step Production Plan

**Target:** 60-minute playable demo
**Timeline:** 12 weeks
**Goal:** Validate PotionWorld concept before full Season 1 production

---

## Overview: The 6 Steps

```
Step 1: Foundation          (Weeks 1-2)   → Core systems working
Step 2: Crafting Magic      (Weeks 3-4)   → Minigame is fun
Step 3: Living Characters   (Weeks 5-6)   → NPCs feel real
Step 4: Visual Identity     (Weeks 7-8)   → Art sets the tone
Step 5: Audio Atmosphere    (Weeks 9-10)  → Sounds bring it alive
Step 6: Polish & Validate   (Weeks 11-12) → Demo is shippable
```

---

## Step 1: Foundation & Core Systems
**Duration:** Weeks 1-2
**Theme:** "Make it work"

### Goals
- Establish technical foundation
- Prove core systems function
- Set up development pipeline
- De-risk technical challenges

### Deliverables

#### Week 1: Project Setup
- ✅ Godot 4.x project initialized
- ✅ Git repository configured
- ✅ Folder structure established (scenes/, scripts/, data/, assets/)
- ✅ Basic UI framework (main menu, settings, simple HUD)
- ✅ Save/load system (JSON-based)
- ✅ Scene transition system (fade in/out)

#### Week 2: Core Data Systems
- ✅ Inventory system (ingredients, potions)
- ✅ Stat tracking (Precision, Knowledge, Intuition, etc.)
- ✅ Recipe database (data structures)
- ✅ Affinity system (NPC relationship tracking)
- ✅ Choice consequence tracking
- ✅ Journal/stats screen (basic layout, no art yet)

### Success Criteria
- [ ] Can create player character with name and background
- [ ] Stats increment and persist through save/load
- [ ] Inventory can add/remove items
- [ ] Affinity values can change and track correctly
- [ ] Scene transitions work smoothly

### Team Focus
**Programmer(s):** Build all systems
**Designer:** Finalize data structures and formulas
**Artist:** Not needed yet (use placeholder art)
**Composer:** Not needed yet

### Risks
- **Technical debt:** Rushing architecture leads to refactoring later
- **Mitigation:** Code review, follow established patterns from existing systems

### Output
**Playable State:** Can navigate between placeholder scenes, stats change, data persists

---

## Step 2: Crafting Magic
**Duration:** Weeks 3-4
**Theme:** "Make it fun"

### Goals
- Build satisfying crafting minigame
- Validate core gameplay loop
- Ensure tactile feedback feels good
- Prove 60% cozy tone works

### Deliverables

#### Week 3: Minigame Mechanics
- ✅ Grinding mechanic (circular drag detection)
- ✅ Pouring mechanic (drag and tilt)
- ✅ Success/quality calculation
- ✅ Visual feedback (ingredient state changes)
- ✅ Particle effects (placeholder)
- ✅ Recipe: Simple Healing Tonic fully implemented

#### Week 4: Polish & Feel
- ✅ Timing windows and precision detection
- ✅ Sound effects (grinding, pouring, bubbling, cork pop)
- ✅ Visual polish (smooth animations, satisfying transitions)
- ✅ Tutorial tooltips ("Grind the mushrooms")
- ✅ Success/failure screens with warm messaging
- ✅ XP gain and level-up notifications

### Success Criteria
- [ ] 8/10 internal playtesters say "Crafting feels satisfying"
- [ ] Minigame takes 60-90 seconds (not too fast, not tedious)
- [ ] Clear when grinding is "perfect" vs "acceptable"
- [ ] No frustrating moments (controls feel good)

### Team Focus
**Programmer:** Minigame implementation, particle systems
**Designer:** Tuning (timing windows, difficulty, feedback)
**Artist:** Begin character sketches, create ingredient icons
**Composer:** Source placeholder sound effects (freesound.org)

### Risks
- **Minigame is boring:** Players find it tedious or repetitive
- **Mitigation:** Rapid prototyping, test early with team, iterate based on feel

### Output
**Playable State:** Can craft Simple Healing Tonic with satisfying tactile feel

---

## Step 3: Living Characters
**Duration:** Weeks 5-6
**Theme:** "Make them real"

### Goals
- Implement dialogue system
- Bring NPCs to life with personality
- Build emotional connection
- Validate 40% RPG (choices matter)

### Deliverables

#### Week 5: Dialogue & Personality
- ✅ Dialogue system (text display, choices, branching)
- ✅ NPC database (Big 5 personalities, affinity, dialogue trees)
- ✅ 4 main NPCs implemented:
  - Kira (warm roommate)
  - Marcus (innovator)
  - Sena (anxious perfectionist)
  - Thornwood (strict teacher)
- ✅ Personality-based dialogue variants
- ✅ Affinity changes trigger based on choices

#### Week 6: Major Choice Implementation
- ✅ Marcus dilemma scene (full dialogue tree)
- ✅ 4 choice outcomes with consequences
- ✅ Choice tracking in journal
- ✅ Day 2 Marcus encounter (varies by choice)
- ✅ Mysterious note scene
- ✅ Kira's nightmare cutscene

### Success Criteria
- [ ] 8/10 playtesters remember 2+ NPC names
- [ ] 7/10 playtesters say "I care about Marcus's situation"
- [ ] 8/10 playtesters say "My choice felt meaningful"
- [ ] Dialogue flows naturally, no awkward pauses

### Team Focus
**Writer:** All dialogue (estimated 3,000-5,000 words)
**Programmer:** Dialogue system, choice branching logic
**Designer:** Balance affinity changes, tune personality reactions
**Artist:** Character portrait sketches → finals (4 NPCs x 4 expressions = 16 portraits)

### Risks
- **NPCs feel flat:** Players don't connect emotionally
- **Mitigation:** Strong character writing, playtesting dialogue early, iterate based on feedback

### Output
**Playable State:** Can talk to NPCs, make choices, see consequences, feel emotional investment

---

## Step 4: Visual Identity
**Duration:** Weeks 7-8
**Theme:** "Make it beautiful"

### Goals
- Establish cozy art style
- Create warm, inviting environments
- Finalize character visuals
- Ensure UI supports cozy-RPG tone

### Deliverables

#### Week 7: Character Art Finalization
- ✅ All character portraits (4 NPCs x 4 expressions)
- ✅ Player character (4 variants x 3 expressions = 12 portraits)
- ✅ Character sprites (basic poses for movement/interaction)
- ✅ Cart driver portrait (optional)
- ✅ Background students (simple sprites)

#### Week 8: Environment & UI Art
- ✅ 5 environment illustrations:
  1. Cart approach scene (sunset)
  2. Dorm room interior
  3. Twilight garden (with glowing ingredients)
  4. Classroom
  5. Courtyard with fountain
- ✅ UI art (recipe cards, journal pages, notifications)
- ✅ Ingredient icons (5 types)
- ✅ Potion vial icon
- ✅ Particle effects (upgraded from placeholders)

### Success Criteria
- [ ] 9/10 playtesters say "Art style is warm and inviting"
- [ ] 8/10 playtesters say "Game looks cozy"
- [ ] Characters are visually distinct and memorable
- [ ] UI is readable and doesn't overwhelm

### Team Focus
**Artist:** Full-time production (characters, environments, UI, icons)
**Programmer:** Integrate art assets, adjust UI layouts
**Designer:** Provide feedback on composition, readability
**Composer:** Begin music composition

### Risks
- **Art style mismatch:** Art doesn't match "cozy" tone
- **Mitigation:** Art style test early (Week 7 Day 1), get feedback, adjust before full production

### Output
**Playable State:** Game looks beautiful, characters are expressive, environments are warm and inviting

---

## Step 5: Audio Atmosphere
**Duration:** Weeks 9-10
**Theme:** "Make it alive"

### Goals
- Add music that enhances cozy tone
- Create immersive soundscapes
- Ensure audio doesn't overwhelm
- Support emotional beats with sound

### Deliverables

#### Week 9: Music Composition
- ✅ Main Theme (character creation, 2-3 min loop)
- ✅ Garden Theme (gathering, peaceful)
- ✅ Crafting Theme (minigame, focused)
- ✅ Courtyard Theme (social, friendly)
- ✅ Evening Theme (reflection, soft)
- ✅ Choice Theme (Marcus dilemma, thoughtful)
- ✅ Hook Theme (mysterious note, anticipatory)

#### Week 10: Sound Design & Implementation
- ✅ Gathering SFX (plucks, rustles, success chimes)
- ✅ Crafting SFX (grinding, pouring, bubbling, cork)
- ✅ UI SFX (page turns, clicks, notifications)
- ✅ Ambient sounds (birds, wind, fountain, student chatter)
- ✅ Character barks (optional: laughs, sighs, gasps)
- ✅ Audio mixing and balancing
- ✅ Settings menu (music volume, SFX volume)

### Success Criteria
- [ ] 8/10 playtesters say "Music enhances the experience"
- [ ] 7/10 playtesters say "Sounds are satisfying, not annoying"
- [ ] Audio doesn't distract from gameplay
- [ ] Emotional moments feel more impactful with music

### Team Focus
**Composer:** All music tracks (7 tracks, ~15 min total)
**Sound Designer:** Create/source SFX (~30 sounds)
**Programmer:** Audio implementation, mixing, volume controls
**Designer:** Provide feedback on emotional beats, audio cues

### Risks
- **Music too repetitive:** 60 minutes with short loops feels tedious
- **Mitigation:** Longer loop compositions (2-3 min each), variation in instrumentation

### Output
**Playable State:** Game sounds alive, music enhances mood, audio supports emotional moments

---

## Step 6: Polish & Validate
**Duration:** Weeks 11-12
**Theme:** "Make it shippable"

### Goals
- Eliminate bugs and rough edges
- Ensure smooth 60-minute experience
- Validate with external playtesters
- Iterate based on feedback

### Deliverables

#### Week 11: Internal Polish
- ✅ Bug fixing (crash reports, softlocks, UI issues)
- ✅ Performance optimization (60 FPS target)
- ✅ Tutorial clarity pass (ensure new players understand)
- ✅ Dialogue editing (typos, awkward phrasing)
- ✅ Balance tuning (affinity changes, XP gains, timing)
- ✅ Accessibility features (text size, volume sliders)
- ✅ Credits screen
- ✅ "To Be Continued" end card

**Internal Playtesting (10+ runs):**
- Full 60-minute playthroughs
- Identify confusion points
- Note time to complete (should be 55-65 min)

#### Week 12: External Validation
- ✅ External playtesting (10-15 target audience players)
- ✅ Exit survey distribution and analysis
- ✅ Video recordings (with permission) to identify pain points
- ✅ Iteration based on feedback:
  - Fix critical bugs
  - Adjust unclear tutorials
  - Rebalance if needed
- ✅ Final polish pass
- ✅ Build for distribution (Windows, Mac, Linux, Web)

### Success Criteria
- [ ] **85%+ want to continue playing** ← CRITICAL METRIC
- [ ] 80%+ say "cozy and relaxing"
- [ ] 75%+ care about NPCs
- [ ] 75%+ say choices felt meaningful
- [ ] 90%+ complete full 60 minutes
- [ ] Zero critical bugs (crashes, softlocks)

### Team Focus
**All Hands:** Bug fixing, polish, playtesting
**Programmer:** Build pipeline, performance optimization
**Designer:** Survey analysis, balance adjustments
**Artist:** Final art tweaks if needed
**Composer:** Final mix adjustments

### Risks
- **Playtest feedback is negative:** Demo doesn't resonate
- **Mitigation:** Have contingency time for major fixes, be willing to delay if needed

### Output
**Shippable Demo:** Polished 60-minute experience ready for distribution, crowdfunding, or pitching

---

## Post-Step 6: Distribution Strategy

### If Metrics Hit Targets (85%+ success rate)
**You have validated the concept!**

**Next Steps:**
1. **Public Demo Release**
   - Itch.io (free demo)
   - Steam page with demo
   - Press outreach

2. **Crowdfunding Campaign** (Optional)
   - Kickstarter / Indiegogo
   - Use demo as proof of concept
   - Target: Fund Season 1 production

3. **Publisher Pitching** (Optional)
   - Use demo + metrics to pitch
   - Seek funding for full game

4. **Begin Season 1 Production**
   - Expand to full 20-hour Season 1
   - Hire additional team members if funded
   - Follow established pipeline

### If Metrics Miss Targets (65-84%)
**Partial success - iteration needed**

**Next Steps:**
1. **Deep Dive Analysis**
   - What specific elements failed?
   - Is it fixable or fundamental?

2. **Targeted Iteration**
   - Rebuild weak systems
   - Re-test with new playtesters
   - Aim for 85%+ before proceeding

3. **Soft Launch**
   - Limited release to gather more feedback
   - Iterate based on broader audience

### If Metrics Fail (<65%)
**Concept needs major pivot or cancellation**

**Next Steps:**
1. **Honest Assessment**
   - Is the core concept flawed?
   - Are we the right team?
   - Is the market not interested?

2. **Pivot Options**
   - Change genre (visual novel instead of RPG?)
   - Change tone (more RPG, less cozy?)
   - Change scope (smaller, different focus?)

3. **Graceful Exit**
   - If no viable pivot, cancel project
   - Document learnings
   - Move to next project

---

## Resource Requirements

### Team Composition (Minimum Viable)
**Core Team (Weeks 1-12):**
- 1 Lead Programmer (full-time)
- 1 Narrative Designer/Writer (full-time Weeks 5-6, part-time other weeks)
- 1 2D Artist (part-time Weeks 1-6, full-time Weeks 7-8)
- 1 Composer (part-time Weeks 9-10)

**Optional:**
- 1 Game Designer (can be Lead Programmer wearing two hats)
- 1 Sound Designer (can use freelance/asset store)
- QA Testers (friends & family for free)

### Budget Estimate (If Hiring)

**Salaries (12 weeks):**
- Lead Programmer: $15,000 (12 weeks @ $1,250/week)
- Narrative Designer: $6,000 (4 weeks full-time, 8 weeks half-time)
- 2D Artist: $10,000 (6 weeks full-time)
- Composer: $2,000 (2 weeks part-time, or flat fee)

**Assets & Software:**
- Godot: Free
- Art software (Aseprite, Krita): $20
- Audio software (Reaper, Audacity): Free
- Stock SFX: $100
- Misc (fonts, plugins): $100

**Playtesting Incentives:**
- 15 external playtesters @ $25 gift cards: $375

**Total Budget: ~$33,000-$35,000**

### Budget Options

**Option A: Solo Developer (You)**
- Time: 12 weeks full-time (or 24+ weeks part-time)
- Cost: $0 (your time/opportunity cost only)
- Use asset store, free tools, do everything yourself

**Option B: Small Team (Contract)**
- Time: 12 weeks
- Cost: $15,000-$20,000 (hire artist + composer only, you do programming/design/writing)

**Option C: Full Professional Team**
- Time: 12 weeks
- Cost: $33,000-$35,000 (hire all roles)

---

## Timeline Visualization

```
Week  1  2  3  4  5  6  7  8  9 10 11 12
Step [──1──][──2──][──3──][──4──][──5──][──6──]

FOUNDATION    CRAFTING     CHARACTERS    ART        AUDIO      POLISH
Systems       Minigame     Dialogue      Visuals    Sound      Testing
Data          Feel         NPCs          Env        Music      Launch
Save          Tutorial     Choices       UI         SFX        Iterate

Milestones:
 ↓             ↓            ↓             ↓          ↓          ↓
Stats         Crafting     Marcus        Art        Music      Demo
work          is fun       matters       is cozy    enhances   ships
```

---

## Success Criteria Summary

### Per-Step Validation

**Step 1:** Technical systems function
- [ ] Save/load works
- [ ] Stats track correctly
- [ ] Inventory functions

**Step 2:** Crafting is satisfying
- [ ] 8/10 say "crafting feels good"
- [ ] Minigame takes 60-90 seconds
- [ ] Clear feedback on success/quality

**Step 3:** Characters feel real
- [ ] 8/10 remember 2+ NPC names
- [ ] 7/10 care about Marcus
- [ ] 8/10 say choice mattered

**Step 4:** Visuals support cozy tone
- [ ] 9/10 say "warm and inviting"
- [ ] Art style is consistent
- [ ] UI is readable

**Step 5:** Audio enhances experience
- [ ] 8/10 say "music enhances"
- [ ] Sounds are satisfying
- [ ] Emotional beats land

**Step 6:** Demo is shippable
- [ ] **85%+ want to continue ← CRITICAL**
- [ ] 80%+ say "cozy"
- [ ] 75%+ care about NPCs
- [ ] 75%+ say choices matter
- [ ] Zero critical bugs

---

## Risk Mitigation Summary

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Crafting not fun | High | Medium | Prototype early, test with team, iterate |
| NPCs not engaging | High | Low | Strong writing, playtest dialogue, iterate |
| Art doesn't match tone | Medium | Medium | Style test early, feedback loop |
| Scope creep | High | High | Strict GDD, weekly check-ins, ruthless cuts |
| Timeline slip | Medium | Medium | Buffer time, cut "maybe" features first |
| Negative playtest | High | Low | Have contingency time, willing to delay |

---

## Key Deliverables Checklist

### By End of Week 12, You Should Have:

**Technical:**
- ✅ Playable 60-minute demo (Windows/Mac/Linux/Web builds)
- ✅ Save/load system functional
- ✅ All core systems implemented

**Content:**
- ✅ 5 locations (cart, dorm, garden, classroom, courtyard)
- ✅ 4 NPCs with personality (Kira, Marcus, Sena, Thornwood)
- ✅ 1 crafting minigame (Simple Healing Tonic)
- ✅ 5 ingredient types implemented
- ✅ 1 major choice with 4 outcomes
- ✅ Multiple minor choices
- ✅ 3,000-5,000 words of dialogue

**Art:**
- ✅ 28 character portraits
- ✅ 20 sprite variations
- ✅ 5 environment illustrations
- ✅ Complete UI (recipe cards, journal, notifications)
- ✅ 15+ icons

**Audio:**
- ✅ 7 music tracks (~15 min total)
- ✅ 30+ sound effects
- ✅ Ambient soundscapes

**Validation:**
- ✅ Playtesting with 10-15 external players
- ✅ Exit survey data collected
- ✅ Metrics analyzed (85%+ target hit)

---

## What Happens After Season 0?

### Success Path: Build Season 1

**Season 1 Scope:**
- Expand from 60 minutes to 20 hours
- Add 15-20 craftable recipes
- Expand to 10-12 NPCs
- Build full academy tournament arc
- Implement time management (100 in-game days)
- Add quest system
- Complete Season 1 story climax

**Timeline:** 6-12 months (depending on team size)
**Budget:** $150,000-$300,000 (professional team)

### Learning Path: Refine the Demo

**If metrics miss targets:**
- Identify weak points from playtesting
- Rebuild/refine specific systems
- Re-test until metrics hit 85%+
- Then proceed to Season 1

### Alternative Path: Standalone Demo

**If funding isn't available:**
- Release Season 0 as standalone experience
- Price at $3-$5
- Gauge market interest
- Use revenue to fund Season 1

---

## Conclusion

**Season 0 is not the full game—it's the proof of concept.**

The goal is to answer one critical question:
> **"Do players want more of this?"**

If 85%+ say yes, you have validated:
- ✅ The 60/40 cozy-RPG tone works
- ✅ Crafting is satisfying, not tedious
- ✅ NPCs are memorable and engaging
- ✅ Choices feel meaningful
- ✅ Players want to see the story continue

**Then, and only then, invest in full Season 1 production.**

This 6-step roadmap gets you there in 12 weeks with a clear path and measurable success criteria at every stage.

---

## Quick Reference: Week-by-Week

| Week | Focus | Key Deliverable |
|------|-------|-----------------|
| 1 | Project setup | Godot initialized, save system works |
| 2 | Data systems | Stats, inventory, affinity tracking |
| 3 | Minigame mechanics | Grinding and pouring work |
| 4 | Minigame polish | Crafting feels satisfying |
| 5 | Dialogue system | NPCs can talk, choices branch |
| 6 | Major choice | Marcus dilemma fully implemented |
| 7 | Character art | All portraits finished |
| 8 | Environment art | All 5 locations illustrated |
| 9 | Music | 7 tracks composed and integrated |
| 10 | Sound design | All SFX in place, mixed |
| 11 | Internal polish | Bugs fixed, performance optimized |
| 12 | External testing | Metrics collected, demo validated |

**Total: 12 weeks to shippable demo**

Good luck! 🧪✨
