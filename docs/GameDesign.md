# PotionWorld - Game Design Document

## Executive Summary

**Game Title:** PotionWorld
**Genre:** Crafting Simulation / Resource Management / Adventure
**Platform:** PC (Python-based)
**Target Audience:** Casual to mid-core gamers interested in crafting, experimentation, and progression systems
**Core Loop:** Gather ingredients → Craft potions → Sell/use potions → Unlock new recipes/areas → Repeat

---

## 1. Game Concept

### 1.1 High Concept
PotionWorld is a potion crafting simulator where players take on the role of an apprentice alchemist building their reputation in a magical world. Players explore diverse environments to gather rare ingredients, experiment with recipes, craft powerful potions, and serve a variety of customers with unique needs.

### 1.2 Unique Selling Points
- **Deep Crafting System**: Combine ingredients with multiple properties to create potions with emergent effects
- **Experimentation Rewards**: Discover recipes through trial and error, not just following guides
- **Dynamic World**: Ingredient availability changes with seasons, weather, and world events
- **Customer Stories**: Each NPC customer has unique needs, preferences, and storylines
- **Risk/Reward Crafting**: Higher quality ingredients and techniques can create powerful potions or spectacular failures

### 1.3 Design Pillars
1. **Experimentation**: Encourage creative problem-solving and discovery
2. **Progression**: Clear sense of growth and mastery
3. **Variety**: Diverse ingredients, recipes, and strategies
4. **Accessibility**: Easy to learn, deep to master

---

## 2. Core Gameplay Mechanics

### 2.1 Ingredient System

#### Ingredient Properties
Each ingredient has multiple properties:
- **Type**: Herb, Mineral, Creature Part, Essence, Catalyst
- **Rarity**: Common, Uncommon, Rare, Epic, Legendary
- **Primary Effect**: Healing, Mana, Strength, Speed, Intelligence, etc.
- **Secondary Effects**: 1-3 additional minor effects
- **Quality**: 1-5 stars (affects potency)
- **Freshness**: Degradation over time (affects quality)

#### Ingredient Sources
- **Wild Gathering**: Explore locations to find ingredients
- **Farming/Growing**: Cultivate renewable ingredient sources
- **Trading**: Purchase from merchants or other NPCs
- **Quests**: Special ingredients from completing missions
- **Events**: Limited-time seasonal or event ingredients

#### Example Ingredients
```
Moonpetal Flower
- Type: Herb
- Rarity: Uncommon
- Primary Effect: Mana Restoration
- Secondary Effects: Night Vision, Calm Mind
- Found: Night-blooming in Whispering Forest
- Quality: Varies with moon phase

Dragon Scale Fragment
- Type: Creature Part
- Rarity: Epic
- Primary Effect: Fire Resistance
- Secondary Effects: Strength Boost, Temperature Regulation
- Found: Dragon's Peak (high-level area)
- Quality: Depends on dragon age
```

### 2.2 Potion Crafting System

#### Basic Crafting Process
1. **Select Base**: Choose liquid base (water, oil, alcohol, etc.)
2. **Add Ingredients**: Combine 2-5 ingredients
3. **Choose Method**: Boiling, Distilling, Fermenting, Infusing, etc.
4. **Add Timing**: Precision timing affects outcome
5. **Optional Catalyst**: Special ingredients that modify effects
6. **Quality Check**: Success/failure based on skill and ingredients

#### Recipe Discovery
- **Learned Recipes**: Standard recipes from books, teachers, or purchase
- **Experimentation**: Try new combinations to discover recipes
- **Hints**: NPCs provide cryptic hints about legendary recipes
- **Research**: Spend time/resources studying to unlock recipes

#### Potion Effects Combination
Effects combine in interesting ways:
- **Synergy**: Some ingredients enhance each other (Healing + Regeneration = Enhanced Healing)
- **Conflict**: Some ingredients cancel out (Fire + Ice = Neutral/Explosion)
- **Mutation**: Rare combinations create unexpected effects
- **Quality Multiplier**: Higher quality ingredients = stronger effects

#### Crafting Outcomes
- **Perfect Potion**: All effects at maximum potency
- **Standard Potion**: Expected effects at normal levels
- **Weak Potion**: Reduced effectiveness
- **Failed Potion**: No effect or minor random effect
- **Explosive Failure**: Dangerous or comical disasters
- **Mutation**: Unexpected new potion discovered

### 2.3 Potion Usage

#### Potion Types
- **Consumables**: Single-use potions (healing, mana, buffs)
- **Throwables**: Grenades, area effects
- **Persistent**: Long-duration effects (days/weeks)
- **Transformation**: Change player/target form
- **Utility**: Solve puzzles, unlock areas, etc.

#### Quality Tiers
- ⭐ Basic: 100% base effect
- ⭐⭐ Quality: 150% base effect
- ⭐⭐⭐ Superior: 200% base effect + bonus duration
- ⭐⭐⭐⭐ Masterwork: 300% base effect + bonus effects
- ⭐⭐⭐⭐⭐ Legendary: 500% base effect + unique properties

---

## 3. Player Progression

### 3.1 Skill System

#### Core Skills
- **Herbalism**: Better gathering yields, identify rare plants
- **Alchemy**: Improved crafting success rate, unlock methods
- **Appraisal**: Identify ingredient properties and quality
- **Negotiation**: Better prices with merchants
- **Exploration**: Access to new areas, faster travel

#### Skill Progression
- Gain experience through relevant actions
- Level up to unlock new abilities and passive bonuses
- Specialization trees for different playstyles

### 3.2 Reputation System

#### Reputation Tracks
- **Local Community**: Affects prices and quest availability
- **Merchants Guild**: Unlocks rare ingredients and recipes
- **Adventurers Society**: Access to dangerous gathering locations
- **Magic Academy**: Advanced alchemical techniques
- **Underground Market**: Forbidden or rare recipes

#### Reputation Actions
- Positive: Complete quests, sell quality potions, help NPCs
- Negative: Sell poor potions, refuse quests, illegal activities

### 3.3 Unlockables

#### Workshop Upgrades
- **Better Equipment**: Increase success rate, reduce time
- **Storage Expansion**: Hold more ingredients and potions
- **Automation**: Auto-gather, auto-craft basic recipes
- **Decoration**: Cosmetic improvements, customer attraction

#### New Locations
- Unlock through progression, quests, or reputation
- Each location has unique ingredients and challenges
- Some locations have environmental hazards or requirements

---

## 4. World & Setting

### 4.1 World Overview
A magical realm where alchemy is an essential part of society. From healing the sick to empowering warriors, potions serve countless purposes. The player starts as a novice alchemist in a small village and can eventually become a legendary master serving kings and heroes.

### 4.2 Key Locations

#### Starting Area: Meadowbrook Village
- Tutorial area with basic ingredients
- Friendly NPCs who teach basics
- Simple quests and challenges

#### Whispering Forest
- Dense woodland with magical plants
- Night-exclusive ingredients
- Mild dangers (wild animals)

#### Crystal Caves
- Underground network with minerals and gems
- Mining mechanics
- Environmental puzzles

#### Dragon's Peak
- High-level area with rare ingredients
- Dangerous creatures
- Epic quest lines

#### The Wetlands
- Unique aquatic and fungal ingredients
- Swamp-specific recipes
- Challenging navigation

#### Merchant's Harbor
- Trading hub
- Exotic imported ingredients
- Competition and timed challenges

### 4.3 Time & Seasons

#### Day/Night Cycle
- Some ingredients only appear at specific times
- Different customers available at different times
- Workshop operations (some recipes require moonlight, etc.)

#### Seasonal Changes
- **Spring**: Abundant herbs and flowers
- **Summer**: Peak growing season
- **Autumn**: Fungi and harvest ingredients
- **Winter**: Rare ice/snow ingredients, scarcity

#### Dynamic Events
- Festivals (special customers, limited ingredients)
- Natural disasters (affect ingredient availability)
- Magical phenomena (boost certain potion types)

---

## 5. NPCs & Customers

### 5.1 Customer Types

#### Regular Customers
- **Villagers**: Simple healing and utility potions
- **Adventurers**: Combat buffs and healing
- **Merchants**: Bulk orders for resale
- **Students**: Practice potions (low quality acceptable)

#### Special Customers
- **Knights/Warriors**: High-quality combat potions
- **Wizards**: Complex magical potions
- **Nobility**: Luxury and vanity potions
- **Healers**: Medical-grade precision potions

#### Story NPCs
- Have ongoing storylines and multiple quests
- Unlock special recipes or areas
- Build relationships over time

### 5.2 Customer Interaction

#### Order System
- Customers request specific potion types or effects
- Can specify quality requirements
- Timed orders add pressure
- Repeat customers build reputation

#### Customer Satisfaction
- Quality vs. expectation
- Delivery time
- Price fairness
- Affects tips, repeat business, and reputation

---

## 6. Economy & Business Management

### 6.1 Currency System
- **Gold Coins**: Primary currency for basic transactions
- **Alchemical Tokens**: Special currency from guild, for rare items
- **Reputation Points**: Unlock privileges and access

### 6.2 Pricing Mechanics
- Base price determined by ingredients and quality
- Market fluctuations based on supply/demand
- Reputation affects prices (buy and sell)
- Can negotiate or set own prices

### 6.3 Shop Management
- Manage inventory (ingredients and potions)
- Stock popular items for regular customers
- Fulfill custom orders for better profit
- Balance between gathering, crafting, and selling

---

## 7. Challenge & Difficulty

### 7.1 Core Challenges
- **Resource Management**: Limited inventory and time
- **Recipe Discovery**: Finding the right combinations
- **Quality Control**: Meeting customer expectations
- **Risk Assessment**: Balancing safety vs. potential rewards

### 7.2 Optional Challenges

#### Timed Orders
- Rush orders with time limits
- Higher rewards but increased pressure

#### Competitions
- Compete with other alchemists
- Judged on quality, creativity, or speed
- Rewards: Recipes, ingredients, reputation

#### Perfectionist Mode
- Try to create perfect (5-star) versions of all potions
- Achievement tracking

### 7.3 Difficulty Scaling
- Early game: Forgiving, educational
- Mid game: Balanced challenge, strategic choices
- Late game: Complex recipes, demanding customers
- Post-game: Master challenges, legendary recipes

---

## 8. User Interface & Experience

### 8.1 Main Screens

#### Workshop View
- Crafting station in center
- Ingredient storage accessible
- Current orders displayed
- Customer queue visible

#### Inventory Screen
- Organized by ingredient type and quality
- Potion storage separate
- Quick search and filtering
- Detailed item information

#### World Map
- Available locations
- Ingredient distribution hints
- Travel time indicators
- Unlockable areas grayed out

#### Customer Interface
- Order details and requirements
- Customer profile and history
- Negotiation options
- Delivery confirmation

### 8.2 Crafting Interface
- Clear visual feedback during crafting
- Ingredient combination preview
- Success probability indicator
- Step-by-step process visualization

### 8.3 Tutorial & Learning
- Gentle introduction to mechanics
- Tooltips and help system
- Practice mode for experimentation
- Alchemy journal with discovered recipes

---

## 9. Progression & Content

### 9.1 Early Game (Hours 0-5)
- Learn basic crafting
- Gather common ingredients
- Serve simple customers
- Unlock first few locations
- Discover 10-20 basic recipes

### 9.2 Mid Game (Hours 5-20)
- Master complex recipes
- Build reputation with factions
- Unlock advanced crafting methods
- Access challenging locations
- Manage multiple customer relationships
- Discover 50+ recipes

### 9.3 Late Game (Hours 20-50)
- Create legendary potions
- Complete major story arcs
- Unlock all locations
- Master all crafting techniques
- Serve high-profile customers
- Discover 100+ recipes

### 9.4 End Game (Hours 50+)
- Perfect all recipes
- Complete all achievements
- Master challenges and competitions
- Experimental legendary recipes
- New Game+ options

---

## 10. Technical Considerations

### 10.1 Save System
- Auto-save functionality
- Manual save slots
- Cloud save support (future)
- Save file integrity checks

### 10.2 Performance Targets
- Smooth 60 FPS gameplay
- Fast load times (<3 seconds)
- Responsive UI (<100ms input response)
- Efficient resource management

### 10.3 Accessibility
- Colorblind-friendly design
- Adjustable text size
- Keyboard/mouse and controller support
- Difficulty options

---

## 11. Monetization (Future Consideration)

### 11.1 Free Version
- Complete base game experience
- No pay-to-win mechanics

### 11.2 Potential Premium Content
- Cosmetic workshop decorations
- Additional story campaigns
- Seasonal event passes
- Expansion packs (new regions, ingredients)

### 11.3 Ethical Guidelines
- No gameplay advantages from purchases
- No predatory mechanics
- Reasonable pricing
- Substantial free content

---

## 12. Audio & Visual Direction

### 12.1 Visual Style
- Whimsical fantasy aesthetic
- Colorful ingredients and potions
- Satisfying particle effects for crafting
- Clear visual feedback for success/failure

### 12.2 Audio Design
- Ambient sounds for different locations
- Satisfying crafting sound effects
- Calming background music
- Audio cues for important events

---

## 13. Success Metrics & Goals

### 13.1 Player Engagement
- Average session length: 30-60 minutes
- 7-day retention: 60%+
- 30-day retention: 30%+
- Average playtime: 20+ hours

### 13.2 Quality Metrics
- 4+ star user rating
- Low bug report rate
- High review sentiment
- Active community participation

### 13.3 Content Metrics
- 70%+ recipe discovery rate
- 80%+ location exploration rate
- 50%+ achievement completion rate

---

## 14. Post-Launch Support

### 14.1 Regular Updates
- Bug fixes and balance patches
- New ingredients and recipes
- Seasonal events
- Quality of life improvements

### 14.2 Community Engagement
- Listen to feedback
- Community challenges
- User-generated content support (future)
- Active social media presence

### 14.3 Expansion Roadmap
- Major content updates every 3-6 months
- New regions and storylines
- Advanced game modes
- Multiplayer features (long-term)

---

## 15. Appendix

### 15.1 Inspiration
- Potion Craft: Alchemist Simulator
- Stardew Valley
- Minecraft brewing system
- Atelier series
- Fantasy RPG crafting systems

### 15.2 References
- Alchemy and herbalism in fantasy literature
- Traditional potion-making mechanics
- Crafting system best practices
- Resource management game design

---

**Document Version:** 1.0
**Last Updated:** 2025-11-07
**Status:** Living Document - Subject to iteration and refinement
