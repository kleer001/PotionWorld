# Season 0: Realistic Solo Parent Dev Plan
## "Proof of Concept in Your Spare Time"

**Your Reality:**
- 10 hours/week average (between parenting two kids)
- No budget for assets
- Working in 1-5 minute chunks
- Claude Code is your teammate
- Already built significant systems in 5 days

**Forget everything else. Here's what you ACTUALLY build:**

---

## The Ultra-Minimal Demo (30-Minute Playable)

**Goal:** Prove ONE thing works and is fun
**Timeline:** 3 months (120 hours at 10 hrs/week)
**Scope:** Small enough to finish, big enough to matter

### What You're Testing:
1. **Is crafting fun?** (the core loop)
2. **Do players care about Marcus?** (one relationship)
3. **Does one choice feel meaningful?** (the moral dilemma)

That's IT. Everything else is cut.

---

## The 30-Minute Experience

### Scene 1: Garden (5 min)
- Text intro: "You're at the academy. First day. Time to gather ingredients."
- Simple gathering: Click mushrooms, berries, roots (free placeholder sprites)
- **Teaching:** Gathering is satisfying

### Scene 2: Crafting (10 min)
- Simple crafting UI (no fancy animations)
- Recipe: Mushrooms + Berries + Sap = Healing Potion
- **FOCUS HERE:** Make the crafting interaction feel good
- Even with programmer art, make the FEEL right

### Scene 3: Meet Marcus (10 min)
- Text-based dialogue (no portraits needed yet)
- Marcus: "I got in trouble for experimenting. They might expel me."
- **THE CHOICE:**
  - Support him
  - Stay neutral
  - Report him
- See immediate consequence (text changes, unlocks different ending)

### Scene 4: Consequence (5 min)
- Next day, Marcus approaches (or doesn't)
- Different text based on your choice
- **END CARD:** "This is the core of PotionWorld. Want more?"

**Total Runtime:** 30 minutes
**Total Assets Needed:** Almost none

---

## Asset Strategy: 100% Free

### Visuals (Programmer Art Phase)
- **UI:** Godot's built-in UI (grey boxes, default theme)
- **Ingredients:** Colored circles (blue = mushroom, red = berry, green = root)
- **Characters:** Text names only, no portraits
- **Environments:** Solid color backgrounds

**Upgrade Later (Free Assets):**
- **Kenney.nl** - Free game assets (UI, icons, simple sprites)
- **OpenGameArt.org** - Free 2D art
- **itch.io freebies** - Lots of free asset packs

### Audio (Free Assets)
- **Music:** Incompetech (Kevin MacLeod) - Royalty-free
- **SFX:** Freesound.org - Creative Commons
- **No custom composition needed**

### Writing
- **You write it** (you're already good at this based on your design docs)

---

## 3-Month Roadmap (10 hrs/week)

### Month 1: Make It Work (40 hours)
**Weeks 1-4: Core Systems**

Using what you ALREADY HAVE:
- Inventory system ✓ (already built)
- Crafting foundation ✓ (already have)
- Relationship tracking ✓ (already have)

**NEW work (40 hours):**
- Scene 1: Gathering UI (click to collect) - 8 hours
- Scene 2: Crafting minigame (simple version) - 16 hours
  - Just ingredient selection + "Craft" button
  - Success/failure based on ESENS
  - Result screen
- Scene 3: Dialogue system (text boxes + choices) - 12 hours
- Scene 4: Branching based on choice - 4 hours

**Milestone:** Can play through 30 minutes, ugly but functional

---

### Month 2: Make It Feel Good (40 hours)
**Weeks 5-8: Polish the Core Loop**

**Focus: Crafting Interaction**
- Add simple visual feedback (color changes, particles) - 8 hours
- Free sound effects from Freesound.org - 4 hours
- Juice it up (screen shake, better transitions) - 8 hours

**Focus: Marcus Character**
- Write compelling dialogue - 8 hours
- Make choice feel weighty (timer? dramatic music?) - 4 hours
- Different outcomes actually feel different - 8 hours

**Milestone:** Core loop feels satisfying, Marcus moment lands

---

### Month 3: Test & Validate (40 hours)
**Weeks 9-12: Get Feedback**

- Bug fixing - 12 hours
- Free UI assets from Kenney.nl - 8 hours
- Tutorial clarity pass - 8 hours
- Playtest with 5 friends/family - 4 hours
- Iterate based on feedback - 8 hours

**Milestone:** 30-min demo you can share publicly

**Success Metric:** 3/5 playtesters say "I'd play more of this"

---

## Your Week-to-Week in 10 Hours

**Example Week (Month 1, Week 2):**

**Monday (5-min chunk):** Fix gathering button position
**Tuesday (1-min chunk):** Commit yesterday's work
**Wednesday (15-min chunk):** Start crafting UI layout
**Thursday (1-min chunk):** Test gathering on phone during break
**Friday (2 hours):** Kids asleep, big push on crafting system
**Saturday (30 min):** Morning coffee coding session
**Sunday (1 hour):** Naptime coding, finish crafting button logic

**Total:** ~10 hours, spread across tiny chunks

---

## What You Cut (For Now)

❌ Character portraits (text names only)
❌ Beautiful environments (solid colors)
❌ Multiple recipes (just one)
❌ 4 NPCs (just Marcus)
❌ 60 minutes (just 30)
❌ Music composition (free royalty-free)
❌ Multiple locations (just garden + classroom, simple)
❌ Crafting minigame complexity (just "select ingredients + click craft")
❌ Kira, Sena, Thornwood (save for v2)
❌ Journal system (too much UI work)
❌ Visual novel-style portraits
❌ Fancy animations

**You can add these LATER if the concept validates.**

---

## What You Keep (Essential)

✅ One crafting loop (must feel good)
✅ One meaningful choice (Marcus dilemma)
✅ ESENS notation (your unique system)
✅ Relationship tracking (what you've built)
✅ 30 minutes of gameplay
✅ Text-based storytelling (your strength)

---

## The Claude Code Strategy

**Since you're using Claude Code in tiny chunks:**

### Good Tasks for 1-5 Min Chunks:
- "Add this button to the UI"
- "Fix this bug in gathering"
- "Write dialogue for Marcus scene"
- "Adjust ingredient spawn positions"
- "Test and commit"

### Good Tasks for Longer Sessions (1-2 hrs):
- "Build gathering scene from scratch"
- "Implement crafting success/failure logic"
- "Create choice branching system"

### Perfect for Claude:
- **Code generation** (you design, Claude codes)
- **Bug fixing** (paste error, Claude fixes)
- **Asset integration** (Claude helps import free assets)
- **Refactoring** (keep code clean as you go)

---

## Free Asset Hunting List

### Essential Free Resources:

**Art:**
- Kenney.nl - UI packs, simple sprites (CC0 license)
- OpenGameArt.org - Search "potion," "fantasy," "UI"
- itch.io → Browse → Free → Assets

**Audio:**
- Freesound.org - Search "bottle," "pour," "bubbling," "cork"
- Incompetech - Search "fantasy," "calm," "cozy"
- Zapsplat.com - Free with attribution

**Fonts:**
- Google Fonts - 100% free
- DaFont - Filter by "free for commercial use"

**Tools:**
- Godot - Your engine (free)
- GIMP - If you need to edit images (free)
- Audacity - If you need to edit audio (free)

---

## The Realistic Success Path

### After 3 Months (120 hours):
**You have:** 30-min playable proof of concept

**Test it with 5 people:**
- 3/5 say "I'd play more" → **SUCCESS, keep going**
- 1-2/5 say "I'd play more" → **Iterate, test again**
- 0/5 say "I'd play more" → **Pivot or move on**

### If It Works:
**Next 3 months (another 120 hours):**
- Add Kira, Sena, Thornwood (more NPCs)
- Expand to 60 minutes
- Add basic UI from free assets
- Maybe add portraits (if you find free ones or commission cheap Fiverr)

**Next 6 months (another 240 hours):**
- Expand to 2 hours (mini-Season 1)
- Add more recipes
- Consider Kickstarter with what you have
- Or keep building slowly

### The Long Game:
**At 10 hrs/week, getting to "full Season 1" (20 hours gameplay) would take:**
- ~2 years of work (500-1000 hours)
- But you'd validate it works at 3 months
- And you'd have a Kickstarter-able demo at 6 months

---

## Brutal Honesty Section

### This Is Hard Mode:
- Solo dev
- No budget
- Minimal time
- Parenting two young kids

**Most games don't finish in this situation.**

### Your Advantages:
- You can code (huge)
- You can write (huge)
- You have Claude Code (MASSIVE)
- You work in tiny chunks (sustainable)
- You already built a ton in 5 days (you're FAST)

### Real Talk:
**3-month goal (30-min demo):** Achievable
**6-month goal (60-min demo):** Achievable
**12-month goal (2-hour game):** Achievable
**Full 5-season game:** 5-10 years at this pace

**Is that okay?**
- If this is your passion project → Yes
- If you need income soon → No, get a job first
- If you want to validate for Kickstarter → 6-month demo, then crowdfund

---

## The "Good Enough" Philosophy

### For Month 1-3:
- Ugly is fine
- Programmer art is fine
- Free assets are fine
- Text-only is fine
- 30 minutes is fine

**Just prove the core is fun.**

### You Can Add Later:
- Art (commission or buy after Kickstarter)
- Music (hire composer after funding)
- More content (expand after validation)
- Polish (add when you have time)

**Ship bad art with good gameplay.**
**Never ship good art with bad gameplay.**

---

## What You Do This Week

### Next 10 Hours (This Week):

**Hour 1-2:** Simplify your prototype goal
- Cut scope to 30 minutes
- Write out the 4 scenes (Garden, Craft, Marcus, Consequence)
- Commit to "ugly but functional" for v1

**Hour 3-5:** Build Scene 1 (Gathering)
- Simple UI: 3 buttons (Mushroom, Berry, Root)
- Click to add to inventory
- "Done Gathering" button → Scene 2

**Hour 6-8:** Build Scene 2 (Crafting)
- Recipe display (text only: "Need: 2 mushroom, 1 berry, 1 sap")
- Ingredient selector (dropdowns or buttons)
- "Craft" button
- Success/failure based on ESENS parser you already have
- Result text: "You made a Simple Healing Tonic!"

**Hour 9-10:** Build Scene 3 Start (Marcus intro)
- Text display: Marcus's dialogue
- 3 choice buttons
- Store choice variable

**END OF WEEK STATUS:**
- Scenes 1-2 playable
- Scene 3 started
- You've proven you can build this in chunks

---

## The Real Question

**Do you want to:**

**Option A:** Build slow, validate in 3 months, keep as passion project
- Totally reasonable
- Sustainable with your life
- Could eventually crowdfund if it works

**Option B:** Build fast prototype (30 min), use to get game dev job
- Demo shows your skills
- Could lead to income
- Then finish PotionWorld on side

**Option C:** Shelve for now, focus on getting income first
- Come back when financially stable
- Not a failure, just timing

**I'm guessing it's Option A?** (Passion project, sustainable pace)

If so, let's rewrite everything for **"3-month ugly prototype"** instead of **"12-week professional demo."**

Want me to create:
1. **Ultra-minimal 30-min scope doc**
2. **This week's task list** (10 specific hours)
3. **Free asset shopping list** (links to everything you need)
4. **Claude Code prompt templates** (for your 1-5 min chunks)

Let me know and I'll make you a REAL plan for your REAL situation.