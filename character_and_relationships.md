# Potion World: Character & Relationship Systems

## The Big 5 Personality System (Simplified)

Each NPC would have a personality profile with 5 traits, each having a value of -1 (Low), 0 (Moderate), or 1 (High):

### 1. Openness (O)
- **High (1)**: Curious, innovative, values experimentation
- **Moderate (0)**: Balanced between tradition and innovation
- **Low (-1)**: Traditional, prefers established methods

### 2. Conscientiousness (C)
- **High (1)**: Meticulous, organized, follows rules
- **Moderate (0)**: Reasonably reliable, somewhat flexible
- **Low (-1)**: Spontaneous, disorganized, bends rules

### 3. Extraversion (E)
- **High (1)**: Outgoing, energetic, seeks attention
- **Moderate (0)**: Adaptable to social situations
- **Low (-1)**: Reserved, reflective, prefers smaller groups

### 4. Agreeableness (A)
- **High (1)**: Cooperative, compassionate, conflict-averse
- **Moderate (0)**: Diplomatic, balanced approach
- **Low (-1)**: Challenging, skeptical, competitive

### 5. Neuroticism (N)
- **High (1)**: Emotionally reactive, worried about outcomes
- **Moderate (0)**: Generally stable with occasional stress
- **Low (-1)**: Emotionally resilient, calm under pressure

## Affinity System

NPCs have an affinity score toward the player ranging from -5 (Hostile) to +5 (Devoted).

### Affinity Values
- **+5**: Devoted (Would go to extraordinary lengths to help)
- **+4**: Loyal (Actively seeks to support player)
- **+3**: Friendly (Offers help and occasional discounts)
- **+2**: Warm (Generally positive interactions)
- **+1**: Positive (Slightly favorable view)
- **0**: Neutral (Professional, transaction-based relationship)
- **-1**: Cool (Mild dislike)
- **-2**: Unfriendly (Reluctant service, possible price increases)
- **-3**: Hostile (May refuse non-essential services)
- **-4**: Antagonistic (Works against player indirectly)
- **-5**: Nemesis (Actively sabotages player)

### Affinity Mechanics

#### 1. Regression to Neutrality
- Over time (e.g., every in-game week), affinity moves 0.5 points toward 0
- Example: NPC at +3 → after a week of no interaction → +2.5 → after another week → +2.0
- This creates natural "relationship maintenance" gameplay

#### 2. Personality-Based Reactions
NPCs respond differently to player actions based on personality:

```ini
[ActionResponses]
InnovativePotion=O(+1), E(+0.5), N(-0.5)
TraditionalPotion=O(-0.5), C(+0.5), N(+0.5)
GiftGiving=E(+1), A(+0.5)
Haggling=C(-0.5), A(-1), E(+0.5)
MissedDeadline=C(-1), N(+0.5)
```

This means an NPC with high Openness (+1) would gain +1 affinity when shown an innovative potion, while an NPC with low Openness (-1) would lose 0.5 affinity for the same action.

#### 3. Threshold Events
When crossing certain affinity thresholds, special events occur:
- **0 → +1**: NPC shares a personal story
- **+2 → +3**: NPC offers special ingredient or recipe
- **+4 → +5**: NPC becomes mentor/partner offering unique benefits
- **0 → -1**: NPC becomes noticeably cooler
- **-2 → -3**: NPC warns others about you
- **-4 → -5**: NPC actively works against you

#### 4. Memory System
- NPCs remember significant interactions (extremely positive or negative)
- "I still remember how you helped during the plague" or "I haven't forgotten how you stole my research"
- These memories resist the regression to neutrality for specific events

## Integration Examples

### Academy Instructor (Season 1)
```ini
[Instructor_Thornwood]
Openness=-1
Conscientiousness=1
Extraversion=0
Agreeableness=-1
Neuroticism=0
InitialAffinity=0

[Reactions]
FollowsRecipePrecisely=+0.5
ExperimentsWithFormula=-0.5
SubmitsLate=-1.0
HelpsOtherStudents=+0.3
AsksTooManyQuestions=-0.2
```

### Village Healer (Season 2)
```ini
[Healer_Wisteria]
Openness=0
Conscientiousness=1
Extraversion=-1
Agreeableness=1
Neuroticism=-1
InitialAffinity=+1

[Reactions]
SharesFamilyRecipe=+1.0
ChargesHighPrices=-0.7
HealsPoorForFree=+0.5
UsesRareIngredients=+0.2
```

## Gameplay Applications

1. **Ingredient Access**: High-affinity NPCs provide rare ingredients or better prices

2. **Knowledge Sharing**: Different personality types offer different insights:
   - High Openness NPCs teach experimental techniques
   - High Conscientiousness NPCs teach precision formulations
   - Low Neuroticism NPCs teach stabilization methods

3. **Reputation Networks**: NPCs talk to each other, with personality determining:
   - Who they trust
   - How far gossip spreads
   - Whether they verify information before believing

4. **Moral Dilemmas**: Choices often satisfy some personality types while alienating others:
   - Helping village (pleases high Agreeableness) vs. advancing research (pleases high Openness)
   - Following regulations (pleases high Conscientiousness) vs. breaking rules for greater good (displeases same trait)

This system creates a web of relationships that evolve naturally over the game, making the social landscape as important as the potion crafting while keeping the mechanics relatively simple.
