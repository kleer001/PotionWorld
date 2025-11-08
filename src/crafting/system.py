import time
import uuid
from typing import List

from src.core.event_bus import EventBus
from src.core.data_structures import Quality
from src.crafting.data_structures import (
    CraftInput,
    CraftResult,
    FormulaBreakdown,
    Potion,
    IngredientInstance,
)
from src.core.events import (
    CraftCompleted,
    PotionCreated,
    RecipeMasteryGained,
    XPGained,
    IngredientsConsumed,
)
from src.crafting.formulas import (
    calculate_success_chance,
    roll_craft_attempt,
    determine_quality,
    calculate_potency,
    calculate_xp_reward,
    update_recipe_mastery,
    get_mastery_bonus,
)


class CraftingSystem:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def craft(
        self,
        input: CraftInput,
        crafter_id: str,
        current_mastery: int = 0
    ) -> CraftResult:
        mastery_bonus = get_mastery_bonus(current_mastery)

        success_chance = calculate_success_chance(
            knowledge=input.crafter_stats.knowledge,
            precision=input.crafter_stats.precision,
            intuition=input.crafter_stats.intuition,
            recipe_difficulty=input.recipe.difficulty,
            tool_bonus=input.tool_bonus,
            prep_bonus=input.prep_bonus
        ) + mastery_bonus

        success, roll = roll_craft_attempt(success_chance)

        breakdown = FormulaBreakdown(
            base_chance=0.5,
            knowledge_bonus=input.crafter_stats.knowledge / 200.0,
            tool_bonus=input.tool_bonus,
            mastery_bonus=mastery_bonus,
            difficulty_penalty=input.recipe.difficulty / 100.0,
            dice_roll=roll,
            final_chance=success_chance + ((roll - 10) / 20.0),
            success_threshold=0.5
        )

        potion = None
        quality = None

        if success:
            success_margin = breakdown.final_chance - breakdown.success_threshold
            avg_ingredient_quality = self._calculate_avg_ingredient_quality(
                input.ingredients
            )

            quality = determine_quality(
                success_margin=success_margin,
                ingredient_quality=avg_ingredient_quality,
                precision=input.crafter_stats.precision
            )

            potency = calculate_potency(quality, input.recipe.base_potency)
            potion = Potion(
                id=self._generate_id(),
                recipe_id=input.recipe.id,
                esens_notation=input.recipe.esens,
                quality=quality,
                potency=potency,
                created_by=crafter_id,
                created_at=time.time()
            )

            self.event_bus.emit(PotionCreated(
                potion=potion,
                quality=quality,
                potency=potency,
                crafter_id=crafter_id
            ))

        xp_rewards = calculate_xp_reward(
            recipe_difficulty=input.recipe.difficulty,
            success=success,
            quality=quality or Quality.POOR
        )

        for stat, amount in xp_rewards.items():
            if amount > 0:
                self.event_bus.emit(XPGained(
                    stat=stat,
                    amount=amount,
                    crafter_id=crafter_id
                ))

        new_mastery = update_recipe_mastery(
            current_mastery=current_mastery,
            success=success,
            quality=quality or Quality.POOR
        )

        if new_mastery > current_mastery:
            self.event_bus.emit(RecipeMasteryGained(
                recipe_id=input.recipe.id,
                old_mastery=current_mastery,
                new_mastery=new_mastery,
                crafter_id=crafter_id
            ))

        self.event_bus.emit(IngredientsConsumed(
            ingredient_ids=[i.id for i in input.ingredients],
            recipe_id=input.recipe.id,
            crafter_id=crafter_id
        ))

        self.event_bus.emit(CraftCompleted(
            success=success,
            recipe_id=input.recipe.id,
            quality=quality,
            potion_id=potion.id if potion else None,
            crafter_id=crafter_id,
            timestamp=int(time.time())
        ))

        return CraftResult(
            success=success,
            quality=quality,
            potion=potion,
            xp_rewards=xp_rewards,
            mastery_gain=new_mastery - current_mastery,
            formula_breakdown=breakdown
        )

    def _calculate_avg_ingredient_quality(
        self,
        ingredients: List[IngredientInstance]
    ) -> Quality:
        if not ingredients:
            return Quality.STANDARD

        avg = sum(i.quality for i in ingredients) / len(ingredients)
        return Quality(round(avg))

    def _generate_id(self) -> str:
        return f"potion_{uuid.uuid4().hex[:8]}"
