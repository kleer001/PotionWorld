from typing import Dict, List, Optional
from src.core.event_bus import EventBus
from src.core.events import (
    XPGained, StatIncreased, MilestoneReached, SpecializationChosen,
    ReputationChanged, RecipeMasteryGained, CraftCompleted, CombatEnded
)
from src.progression.data_structures import StatChange, Specialization
from src.progression.formulas import (
    xp_to_stat, stat_to_xp, xp_for_next_milestone,
    update_mastery, get_mastery_bonuses,
    calculate_reputation_level, get_reputation_modifiers,
    can_choose_specialization, get_specialization_by_id
)


class ProgressionSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe(CraftCompleted, self.on_craft_completed)
        self.event_bus.subscribe(CombatEnded, self.on_combat_ended)

    def add_xp(
        self,
        player_id: str,
        stat: str,
        amount: int,
        current_xp: int
    ) -> StatChange:
        old_xp = current_xp
        new_xp = old_xp + amount

        old_stat = xp_to_stat(old_xp)
        new_stat = xp_to_stat(new_xp)

        milestone_reached = False
        if (new_stat // 20) > (old_stat // 20):
            milestone_reached = True

        result = StatChange(
            stat=stat,
            xp_gained=amount,
            old_xp=old_xp,
            new_xp=new_xp,
            old_stat=old_stat,
            new_stat=new_stat,
            milestone_reached=milestone_reached
        )

        self.event_bus.emit(XPGained(
            stat=stat,
            amount=amount,
            crafter_id=player_id
        ))

        if new_stat > old_stat:
            self.event_bus.emit(StatIncreased(
                player_id=player_id,
                stat=stat,
                old_value=old_stat,
                new_value=new_stat
            ))

        if milestone_reached:
            milestone = (new_stat // 20) * 20
            unlocks = self._get_milestone_unlocks(stat, milestone)

            self.event_bus.emit(MilestoneReached(
                player_id=player_id,
                stat=stat,
                milestone=milestone,
                unlocks=unlocks
            ))

        return result

    def choose_specialization(
        self,
        player_id: str,
        spec_id: str,
        player_stats: Dict[str, int]
    ) -> bool:
        spec = get_specialization_by_id(spec_id)

        if not spec:
            return False

        if not can_choose_specialization(spec, player_stats):
            return False

        self.event_bus.emit(SpecializationChosen(
            player_id=player_id,
            specialization=spec
        ))

        return True

    def update_reputation(
        self,
        player_id: str,
        region: str,
        delta: int,
        current_reputation: int,
        reason: str
    ) -> int:
        old_value = current_reputation
        new_value = max(0, min(100, old_value + delta))

        if new_value != old_value:
            self.event_bus.emit(ReputationChanged(
                player_id=player_id,
                region=region,
                old_value=old_value,
                new_value=new_value,
                reason=reason
            ))

        return new_value

    def update_recipe_mastery(
        self,
        player_id: str,
        recipe_id: str,
        current_mastery: int,
        success: bool,
        quality: 'Quality'
    ) -> int:
        old_mastery = current_mastery
        new_mastery = update_mastery(old_mastery, success, quality)

        if new_mastery != old_mastery:
            self.event_bus.emit(RecipeMasteryGained(
                recipe_id=recipe_id,
                old_mastery=old_mastery,
                new_mastery=new_mastery,
                crafter_id=player_id
            ))

        return new_mastery

    def _get_milestone_unlocks(self, stat: str, milestone: int) -> List[str]:
        unlocks_map = {
            "knowledge": {
                20: ["basic_recipes"],
                40: ["intermediate_recipes"],
                60: ["advanced_recipes"],
                80: ["expert_recipes"],
                100: ["master_recipes"]
            },
            "precision": {
                20: ["quality_boost"],
                40: ["consistent_crafting"],
                60: ["perfectionist_spec"],
                80: ["masterwork_chance"],
                100: ["guaranteed_quality"]
            },
            "intuition": {
                20: ["ingredient_insight"],
                40: ["recipe_variation"],
                60: ["innovator_spec"],
                80: ["advanced_substitution"],
                100: ["recipe_creation"]
            },
            "business_acumen": {
                20: ["market_awareness"],
                40: ["price_negotiation"],
                60: ["merchant_spec"],
                80: ["bulk_discounts"],
                100: ["trade_empire"]
            },
            "combat_instinct": {
                20: ["basic_tactics"],
                40: ["advanced_tactics"],
                60: ["combat_mastery"],
                80: ["tactical_genius"],
                100: ["legendary_duelist"]
            }
        }

        return unlocks_map.get(stat, {}).get(milestone, [])

    def on_craft_completed(self, event: CraftCompleted):
        pass

    def on_combat_ended(self, event: CombatEnded):
        pass
