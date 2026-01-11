#!/usr/bin/env python3
"""
Enhanced Status Effect Notation System (ESENS) Parser
A syntax validator and interpreter for the ESENS language.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Union, Tuple, Any

# -----------------------------------------------------------------------------
# Constant Definitions - Basic Symbols & Tokens
# -----------------------------------------------------------------------------

class Target(Enum):
    PLAYER = "P"
    ENEMY = "E"
    ALL_ALLIES = "A"
    ALL_ENEMIES = "X"
    GLOBAL = "G"

class EffectType(Enum):
    INCREASE = "+"
    DECREASE = "-"
    SET = "="
    MULTIPLY = "*"
    NULLIFY = "!"
    SPECIAL = "#"

class StatType(Enum):
    STRENGTH = "S"
    DEFENSE = "D"
    ELEMENT = "E"
    LUCK = "L"
    GOLD = "G"
    HEALTH = "H"
    MOVEMENT = "M"
    INITIATIVE = "I"
    CRITICAL = "C"
    RESISTANCE = "R"

class ElementType(Enum):
    FIRE = "F"
    WATER = "W"
    EARTH = "E"
    SKY = "S"
    DEATH = "D"

class DurationType(Enum):
    TURNS = "T"  # Combined with a number
    COMBAT = "C"
    PERMANENT = "P"
    ACTION = "A"

class TriggerType(Enum):
    ON_ATTACK = ">A"
    ON_DEFEND = "<D"
    TURN_START = "^S"
    TURN_END = "vE"
    ON_KILL = "K"
    # Chance and condition triggers are handled separately

class SpecialFlag(Enum):
    STACKING = "ST"
    AREA_EFFECT = "AR"
    DAMAGE_OVER_TIME = "DOT"

class RemovabilityFlag(Enum):
    NON_REMOVABLE = "RN"
    EASILY_REMOVED = "RE"
    DIFFICULT_REMOVE = "RD"
    CLEANSE_SPECIFIC = "RC"

class ChainEffect(Enum):
    HEAL = ">Heal"
    EXPLODE = ">Expl"
    SPREAD = ">Sprd"
    TRIGGER = ">Trig"

class SourceDependency(Enum):
    PLAYER_LINKED = "~P"
    ENEMY_LINKED = "~E"
    INDEPENDENT = "~I"

class StackingBehavior(Enum):
    MAX_STACKS = "S"  # Combined with a number
    ADD_DURATION = "S+"
    MULTIPLY_EFFECT = "S*"
    UNIQUE_STACKING = "SU"

class VisibilityFlag(Enum):
    HIDDEN = "VH"
    VISIBLE_ALL = "VV"
    VISIBLE_PLAYER = "VP"

class ResourceConnection(Enum):
    MANA = "$MP"
    HEALTH = "$HP"
    GOLD = "$G"

class InteractionTag(Enum):
    EXCLUSIVE = "IX"
    ADDITIVE = "IA"
    MULTIPLICATIVE = "IM"

class MetaEffect(Enum):
    GOBSTOPPER = "#Gobstop"
    PHASE = "#Phase"
    ECHO = "#Echo"
    FLUX = "#Flux"


# -----------------------------------------------------------------------------
# Data Classes - Object Model
# -----------------------------------------------------------------------------

@dataclass
class Magnitude:
    value: float
    is_percentage: bool = False
    is_full: bool = False

    def __str__(self):
        if self.is_full:
            return "F"
        if self.is_percentage:
            return f"{self.value}%"
        return str(self.value)


@dataclass
class Duration:
    value: Optional[int] = None
    range_start: Optional[int] = None
    range_end: Optional[int] = None
    type: Optional[DurationType] = None

    def __str__(self):
        if self.type == DurationType.COMBAT:
            return "C"
        if self.type == DurationType.PERMANENT:
            return "P"
        if self.type == DurationType.ACTION:
            return "A"
        if self.range_start is not None and self.range_end is not None:
            return f"{self.range_start}-{self.range_end}T"
        return f"{self.value}T"


@dataclass
class Condition:
    attribute: str
    operator: str
    value: Union[int, str, float]
    is_percentage: bool = False

    def __str__(self):
        value_str = f"{self.value}%" if self.is_percentage else str(self.value)
        return f"{self.attribute}{self.operator}{value_str}"


@dataclass
class Trigger:
    type: Optional[TriggerType] = None
    chance: Optional[int] = None
    condition: Optional[Condition] = None

    def __str__(self):
        if self.type:
            return self.type.value
        if self.chance:
            return f"?{self.chance}%"
        if self.condition:
            return f"?{self.condition}"
        return ""


@dataclass
class StatusEffect:
    target: Target
    effect_type: EffectType
    stat_affected: Union[StatType, str]  # String for special conditions
    magnitude: Optional[Magnitude] = None
    duration: Optional[Duration] = None
    trigger: Optional[Trigger] = None
    element: Optional[List[ElementType]] = None
    special_flags: List[str] = field(default_factory=list)
    
    # Extended components
    removability: Optional[RemovabilityFlag] = None
    chain_effect: Optional[ChainEffect] = None
    chain_target: Optional['StatusEffect'] = None
    source_dependency: Optional[SourceDependency] = None
    stacking_behavior: Optional[StackingBehavior] = None
    stacking_value: Optional[int] = None
    visibility: Optional[VisibilityFlag] = None
    resource_connection: Optional[ResourceConnection] = None
    resource_amount: Optional[int] = None
    conditions: List[Condition] = field(default_factory=list)
    interaction_tag: Optional[InteractionTag] = None
    meta_effect: Optional[MetaEffect] = None

    def to_dict(self):
        """Convert to a dictionary representation"""
        result = {
            "target": self.target.value,
            "effect_type": self.effect_type.value,
        }

        # Handle stat affected (could be enum or string for special conditions)
        if isinstance(self.stat_affected, StatType):
            result["stat_affected"] = self.stat_affected.value
        else:
            result["stat_affected"] = self.stat_affected

        # Add other fields if present
        if self.magnitude:
            result["magnitude"] = {
                "value": self.magnitude.value,
                "is_percentage": self.magnitude.is_percentage,
                "is_full": self.magnitude.is_full
            }

        if self.duration:
            result["duration"] = {
                "value": self.duration.value,
                "range_start": self.duration.range_start,
                "range_end": self.duration.range_end,
                "type": self.duration.type.value if self.duration.type else None
            }

        if self.trigger:
            result["trigger"] = {
                "type": self.trigger.type.value if self.trigger.type else None,
                "chance": self.trigger.chance,
                "condition": str(self.trigger.condition) if self.trigger.condition else None
            }

        if self.element:
            result["element"] = [e.value for e in self.element]

        if self.special_flags:
            result["special_flags"] = self.special_flags

        if self.removability:
            result["removability"] = self.removability.value

        if self.chain_effect:
            result["chain_effect"] = self.chain_effect.value
            if self.chain_target:
                result["chain_target"] = self.chain_target.to_dict()

        if self.source_dependency:
            result["source_dependency"] = self.source_dependency.value

        if self.stacking_behavior:
            result["stacking_behavior"] = {
                "type": self.stacking_behavior.value,
                "value": self.stacking_value
            }

        if self.visibility:
            result["visibility"] = self.visibility.value

        if self.resource_connection:
            result["resource_connection"] = {
                "type": self.resource_connection.value,
                "amount": self.resource_amount
            }

        if self.conditions:
            result["conditions"] = [str(c) for c in self.conditions]

        if self.interaction_tag:
            result["interaction_tag"] = self.interaction_tag.value

        if self.meta_effect:
            result["meta_effect"] = self.meta_effect.value

        return result

    def to_text(self):
        """Generate a human-readable explanation of the effect"""
        target_map = {
            Target.PLAYER: "Player",
            Target.ENEMY: "Enemy",
            Target.ALL_ALLIES: "All allies",
            Target.ALL_ENEMIES: "All enemies",
            Target.GLOBAL: "Everyone"
        }
        
        effect_map = {
            EffectType.INCREASE: "gains",
            EffectType.DECREASE: "loses",
            EffectType.SET: "has set to",
            EffectType.MULTIPLY: "has multiplied",
            EffectType.NULLIFY: "has nullified",
            EffectType.SPECIAL: "is affected by"
        }
        
        stat_map = {
            StatType.STRENGTH: "strength",
            StatType.DEFENSE: "defense",
            StatType.ELEMENT: "element",
            StatType.LUCK: "luck",
            StatType.GOLD: "gold",
            StatType.HEALTH: "health",
            StatType.MOVEMENT: "movement",
            StatType.INITIATIVE: "initiative",
            StatType.CRITICAL: "critical hit chance",
            StatType.RESISTANCE: "resistance"
        }
        
        element_map = {
            ElementType.FIRE: "Fire",
            ElementType.WATER: "Water",
            ElementType.EARTH: "Earth",
            ElementType.SKY: "Sky",
            ElementType.DEATH: "Death"
        }
        
        # Start building the description
        description = f"{target_map[self.target]} {effect_map[self.effect_type]} "
        
        # Add stat affected
        if isinstance(self.stat_affected, StatType):
            description += f"{stat_map[self.stat_affected]}"
        else:
            # For special conditions
            description += f"the '{self.stat_affected}' condition"
        
        # Add magnitude if present
        if self.magnitude:
            if self.magnitude.is_full:
                description += " to its maximum value"
            elif self.magnitude.is_percentage:
                description += f" by {self.magnitude.value}%"
            else:
                description += f" by {self.magnitude.value}"
        
        # Add duration if present
        if self.duration:
            if self.duration.type == DurationType.COMBAT:
                description += " for the duration of combat"
            elif self.duration.type == DurationType.PERMANENT:
                description += " permanently"
            elif self.duration.type == DurationType.ACTION:
                description += " for a single action"
            elif self.duration.range_start is not None and self.duration.range_end is not None:
                description += f" for {self.duration.range_start}-{self.duration.range_end} turns"
            else:
                description += f" for {self.duration.value} turns"
        
        # Add trigger if present
        if self.trigger:
            if self.trigger.type:
                trigger_text = {
                    TriggerType.ON_ATTACK: "when attacking",
                    TriggerType.ON_DEFEND: "when defending",
                    TriggerType.TURN_START: "at the start of their turn",
                    TriggerType.TURN_END: "at the end of their turn",
                    TriggerType.ON_KILL: "on kill"
                }
                description += f" {trigger_text[self.trigger.type]}"
            elif self.trigger.chance:
                description += f" with a {self.trigger.chance}% chance each turn"
            elif self.trigger.condition:
                description += f" when {self.trigger.condition}"
        
        # Add element if present
        if self.element:
            element_names = [element_map[e] for e in self.element]
            if len(element_names) == 1:
                description += f" ({element_names[0]} element)"
            else:
                description += f" ({', '.join(element_names)} elements)"
        
        # Add special flags if present
        if self.special_flags:
            flag_descriptions = []
            for flag in self.special_flags:
                if flag == "ST":
                    flag_descriptions.append("can stack")
                elif flag == "AR":
                    flag_descriptions.append("affects an area")
                elif flag == "DOT":
                    flag_descriptions.append("deals damage over time")
            
            if flag_descriptions:
                description += f". This effect {', '.join(flag_descriptions)}"
        
        # Add extended components if present
        extended_descriptions = []
        
        if self.removability:
            removability_text = {
                RemovabilityFlag.NON_REMOVABLE: "cannot be removed",
                RemovabilityFlag.EASILY_REMOVED: "can be easily removed",
                RemovabilityFlag.DIFFICULT_REMOVE: "is difficult to remove",
                RemovabilityFlag.CLEANSE_SPECIFIC: "requires specific cleansing"
            }
            extended_descriptions.append(removability_text[self.removability])
        
        if self.chain_effect:
            chain_text = {
                ChainEffect.HEAL: "triggers healing when it ends",
                ChainEffect.EXPLODE: "explodes for damage when it ends",
                ChainEffect.SPREAD: "spreads to nearby targets when it ends",
                ChainEffect.TRIGGER: "triggers another effect when it ends"
            }
            extended_descriptions.append(chain_text[self.chain_effect])
        
        if self.source_dependency:
            dependency_text = {
                SourceDependency.PLAYER_LINKED: "ends if the player dies",
                SourceDependency.ENEMY_LINKED: "ends if the enemy dies",
                SourceDependency.INDEPENDENT: "persists regardless of source"
            }
            extended_descriptions.append(dependency_text[self.source_dependency])
        
        if self.stacking_behavior:
            if self.stacking_behavior == StackingBehavior.MAX_STACKS:
                extended_descriptions.append(f"stacks up to {self.stacking_value} times")
            elif self.stacking_behavior == StackingBehavior.ADD_DURATION:
                extended_descriptions.append("adds duration when reapplied")
            elif self.stacking_behavior == StackingBehavior.MULTIPLY_EFFECT:
                extended_descriptions.append("multiplies effect when stacked")
            elif self.stacking_behavior == StackingBehavior.UNIQUE_STACKING:
                extended_descriptions.append("allows unique stacking from different sources")
        
        if self.visibility:
            visibility_text = {
                VisibilityFlag.HIDDEN: "is hidden from the target",
                VisibilityFlag.VISIBLE_ALL: "is visible to all",
                VisibilityFlag.VISIBLE_PLAYER: "is only visible to the player"
            }
            extended_descriptions.append(visibility_text[self.visibility])
        
        if self.resource_connection:
            resource_text = {
                ResourceConnection.MANA: f"costs {self.resource_amount or 'some'} mana per turn",
                ResourceConnection.HEALTH: f"costs {self.resource_amount or 'some'} health per turn",
                ResourceConnection.GOLD: f"costs {self.resource_amount or 'some'} gold per turn"
            }
            extended_descriptions.append(resource_text[self.resource_connection])
        
        if self.conditions:
            conditions_text = [f"only works when {c}" for c in self.conditions]
            extended_descriptions.extend(conditions_text)
        
        if self.interaction_tag:
            interaction_text = {
                InteractionTag.EXCLUSIVE: "cancels similar effects",
                InteractionTag.ADDITIVE: "adds with similar effects",
                InteractionTag.MULTIPLICATIVE: "multiplies with similar effects"
            }
            extended_descriptions.append(interaction_text[self.interaction_tag])
        
        if self.meta_effect:
            meta_text = {
                MetaEffect.GOBSTOPPER: "transforms into new effects over time",
                MetaEffect.PHASE: "changes based on combat phase",
                MetaEffect.ECHO: "repeats at intervals",
                MetaEffect.FLUX: "fluctuates in strength"
            }
            extended_descriptions.append(meta_text[self.meta_effect])
        
        # Add extended descriptions if present
        if extended_descriptions:
            description += f". The effect {', '.join(extended_descriptions)}"
        
        return description


# -----------------------------------------------------------------------------
# Error Handling
# -----------------------------------------------------------------------------

class ESENSParseError(Exception):
    """Base class for ESENS parsing errors"""
    def __init__(self, message, position=None, snippet=None):
        self.message = message
        self.position = position
        self.snippet = snippet
        super().__init__(self.full_message())
    
    def full_message(self):
        msg = f"Error: {self.message}"
        if self.position is not None:
            msg += f" at position {self.position}"
        if self.snippet:
            msg += f"\n  {self.snippet}\n  {' ' * self.position}^"
        return msg


class TokenizationError(ESENSParseError):
    """Error during tokenization"""
    pass


class ValidationError(ESENSParseError):
    """Error during validation"""
    pass


# -----------------------------------------------------------------------------
# Tokenizer
# -----------------------------------------------------------------------------

@dataclass
class Token:
    type: str
    value: str
    position: int


class ESENSTokenizer:
    """Tokenizes ESENS notation strings"""
    
    def __init__(self):
        self.patterns = [
            # Target
            (r'[PEAXG]', 'TARGET'),
            
            # Effect type
            (r'[+\-=*!#]', 'EFFECT'),
            
            # Stat affected
            (r'[SDELGHMIRC]', 'STAT'),
            
            # Numbers
            (r'\d+', 'NUMBER'),
            
            # Percentage
            (r'%', 'PERCENTAGE'),
            
            # Full value
            (r'F', 'FULL'),
            
            # Duration types
            (r'[TCPA]', 'DURATION_TYPE'),
            
            # Range separator
            (r'-', 'RANGE'),
            
            # Triggers
            (r'[><^v]', 'TRIGGER_PREFIX'),
            (r'[ADESCK]', 'TRIGGER_TYPE'),
            (r'\?', 'CONDITION_PREFIX'),
            
            # Elements
            (r'[FWESD]', 'ELEMENT'),
            
            # Special flags and extended components
            (r'ST|AR|DOT', 'SPECIAL_FLAG'),
            (r'RN|RE|RD|RC', 'REMOVABILITY'),
            (r'>Heal|>Expl|>Sprd|>Trig', 'CHAIN_EFFECT'),
            (r'~[PEI]', 'SOURCE_DEPENDENCY'),
            (r'S[+*U]', 'STACKING_BEHAVIOR'),
            (r'V[HVP]', 'VISIBILITY'),
            (r'\$[MPG]', 'RESOURCE'),
            (r'I[XAM]', 'INTERACTION'),
            
            # Delimiters and operators
            (r'\.', 'DELIMITER'),
            (r',', 'COMMA'),
            (r'&', 'AND'),
            (r'{', 'OPEN_BRACE'),
            (r'}', 'CLOSE_BRACE'),
            (r'\(', 'OPEN_PAREN'),
            (r'\)', 'CLOSE_PAREN'),
            (r'<=|>=|=|<|>', 'OPERATOR'),
            
            # Special condition indicators
            (r'#[A-Za-z]+', 'SPECIAL_CONDITION'),
            
            # Identifiers
            (r'[A-Za-z]+', 'IDENTIFIER'),
            
            # Whitespace (ignored)
            (r'\s+', 'WHITESPACE'),
            
            # Anything else is an error
            (r'.', 'ERROR')
        ]
    
    def tokenize(self, text):
        """Convert text into a list of tokens"""
        position = 0
        tokens = []
        
        while position < len(text):
            match = None
            
            for pattern, token_type in self.patterns:
                regex = re.compile(pattern)
                match = regex.match(text, position)
                
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE':  # Skip whitespace
                        tokens.append(Token(token_type, value, position))
                    position = match.end()
                    break
            
            if not match:
                # This should never happen with our catch-all ERROR pattern
                raise TokenizationError(f"Unexpected character", position, text)
            
            if token_type == 'ERROR':
                raise TokenizationError(f"Invalid character '{value}'", position - 1, text)
        
        return tokens


# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------

class ESENSParser:
    """Parses ESENS notation into structured objects"""
    
    def __init__(self):
        self.tokenizer = ESENSTokenizer()
    
    def parse(self, text, explain=True):
        """Parse ESENS notation string into a StatusEffect object"""
        tokens = self.tokenizer.tokenize(text)
        
        if not tokens:
            raise ValidationError("Empty input", 0, text)
        
        # Basic validation: must start with valid target and effect
        if tokens[0].type != 'TARGET':
            raise ValidationError(f"Expected target (P,E,A,X,G), got {tokens[0].value}", 
                                 tokens[0].position, text)
        
        if len(tokens) < 2 or tokens[1].type != 'EFFECT':
            pos = tokens[0].position + 1 if len(tokens) > 1 else len(text)
            raise ValidationError(f"Expected effect type (+,-,=,*,!,#)", pos, text)
        
        # Need either a stat or special condition
        if len(tokens) < 3 or (tokens[2].type != 'STAT' and tokens[2].type != 'SPECIAL_CONDITION'):
            pos = tokens[1].position + 1 if len(tokens) > 2 else len(text)
            raise ValidationError(f"Expected stat affected or special condition", pos, text)
        
        # Continue with parsing the components
        effect = self._parse_core_components(tokens, text)
        
        # Add extended components if present
        self._parse_extended_components(effect, tokens, text)
        
        # Return the parsed effect
        result = {
            "object": effect,
            "dict": effect.to_dict()
        }
        
        if explain:
            result["explanation"] = effect.to_text()
        
        return result
    
    def _parse_core_components(self, tokens, text):
        """Parse the basic required components"""
        # Extract target
        target_token = tokens[0]
        try:
            target = Target(target_token.value)
        except ValueError:
            raise ValidationError(f"Invalid target: {target_token.value}", 
                                 target_token.position, text)
        
        # Extract effect type
        effect_token = tokens[1]
        try:
            effect_type = EffectType(effect_token.value)
        except ValueError:
            raise ValidationError(f"Invalid effect type: {effect_token.value}", 
                                 effect_token.position, text)
        
        # Extract stat affected
        stat_token = tokens[2]
        if stat_token.type == 'STAT':
            try:
                stat_affected = StatType(stat_token.value)
            except ValueError:
                raise ValidationError(f"Invalid stat: {stat_token.value}", 
                                     stat_token.position, text)
        else:  # Special condition
            stat_affected = stat_token.value
        
        # Create the basic StatusEffect
        effect = StatusEffect(
            target=target,
            effect_type=effect_type,
            stat_affected=stat_affected
        )
        
        # Parse optional components
        idx = 3
        
        # Check for magnitude
        if idx < len(tokens) and (tokens[idx].type == 'NUMBER' or tokens[idx].type == 'FULL'):
            magnitude, idx = self._parse_magnitude(tokens, idx, text)
            effect.magnitude = magnitude
        
        # Check for duration
        if idx < len(tokens) and (tokens[idx].type == 'NUMBER' or 
                                tokens[idx].type == 'DURATION_TYPE'):
            duration, idx = self._parse_duration(tokens, idx, text)
            effect.duration = duration
        
        # Check for trigger
        if idx < len(tokens) and (tokens[idx].type == 'TRIGGER_PREFIX' or 
                                tokens[idx].type == 'CONDITION_PREFIX' or
                                tokens[idx].type == 'TRIGGER_TYPE'):
            trigger, idx = self._parse_trigger(tokens, idx, text)
            effect.trigger = trigger
        
        # Check for element
        if idx < len(tokens) and tokens[idx].type == 'ELEMENT':
            elements, idx = self._parse_elements(tokens, idx, text)
            effect.element = elements
        
        return effect
    
    def _parse_magnitude(self, tokens, idx, text):
        """Parse magnitude component"""
        if tokens[idx].type == 'FULL':
            return Magnitude(value=0, is_full=True), idx + 1
        
        value = int(tokens[idx].value)
        idx += 1
        
        is_percentage = False
        if idx < len(tokens) and tokens[idx].type == 'PERCENTAGE':
            is_percentage = True
            idx += 1
        
        return Magnitude(value=value, is_percentage=is_percentage), idx
    
    def _parse_duration(self, tokens, idx, text):
        """Parse duration component"""
        if tokens[idx].type == 'DURATION_TYPE':
            # Single character duration (C, P, A)
            try:
                duration_type = DurationType(tokens[idx].value)
                return Duration(type=duration_type), idx + 1
            except ValueError:
                raise ValidationError(f"Invalid duration type: {tokens[idx].value}", 
                                    tokens[idx].position, text)
        
        # Must be a number of turns or a range
        value = int(tokens[idx].value)
        idx += 1
        
        # Check if it's a range (X-YT)
        if idx < len(tokens) and tokens[idx].type == 'RANGE':
            idx += 1
            if idx >= len(tokens) or tokens[idx].type != 'NUMBER':
                raise ValidationError("Expected end of range after '-'", 
                                    tokens[idx-1].position + 1, text)
            
            end_value = int(tokens[idx].value)
            idx += 1
            
            if idx >= len(tokens) or tokens[idx].type != 'DURATION_TYPE' or tokens[idx].value != 'T':
                raise ValidationError("Expected 'T' after duration range", 
                                    tokens[idx-1].position + 1, text)
            
            return Duration(range_start=value, range_end=end_value, type=DurationType.TURNS), idx + 1
        
        # Simple number of turns (XT)
        if idx >= len(tokens) or tokens[idx].type != 'DURATION_TYPE' or tokens[idx].value != 'T':
            raise ValidationError("Expected 'T' after duration value", 
                                tokens[idx-1].position + 1, text)
        
        return Duration(value=value, type=DurationType.TURNS), idx + 1
    
    def _parse_trigger(self, tokens, idx, text):
        """Parse trigger component"""
        # Handle simple trigger types (K)
        if tokens[idx].type == 'TRIGGER_TYPE' and tokens[idx].value == 'K':
            try:
                trigger_type = TriggerType.ON_KILL
                return Trigger(type=trigger_type), idx + 1
            except ValueError:
                raise ValidationError(f"Invalid trigger type: {tokens[idx].value}", 
                                    tokens[idx].position, text)
        
        # Handle prefixed triggers (>A, <D, ^S, vE)
        if tokens[idx].type == 'TRIGGER_PREFIX':
            prefix = tokens[idx].value
            idx += 1
            
            if idx >= len(tokens) or tokens[idx].type != 'TRIGGER_TYPE':
                raise ValidationError(f"Expected trigger type after '{prefix}'", 
                                    tokens[idx-1].position + 1, text)
            
            trigger_code = prefix + tokens[idx].value
            try:
                trigger_type = TriggerType(trigger_code)
                return Trigger(type=trigger_type), idx + 1
            except ValueError:
                raise ValidationError(f"Invalid trigger: {trigger_code}", 
                                    tokens[idx-1].position, text)
        
        # Handle condition triggers (?X)
        if tokens[idx].type == 'CONDITION_PREFIX':
            idx += 1
            
            # Check for chance trigger (?X%)
            if idx < len(tokens) and tokens[idx].type == 'NUMBER':
                chance = int(tokens[idx].value)
                idx += 1
                
                if idx >= len(tokens) or tokens[idx].type != 'PERCENTAGE':
                    raise ValidationError("Expected '%' after chance value", 
                                        tokens[idx-1].position + 1, text)
                
                return Trigger(chance=chance), idx + 1
            
            # For now, we'll handle simple conditions only
            # More complex condition parsing would go here
            if idx < len(tokens) and tokens[idx].type == 'IDENTIFIER':
                condition = Condition(
                    attribute=tokens[idx].value,
                    operator="=",
                    value=True
                )
                return Trigger(condition=condition), idx + 1
            
            raise ValidationError("Expected condition after '?'", 
                                tokens[idx-1].position + 1, text)
        
        # If we get here, it's an error
        raise ValidationError(f"Invalid trigger format", tokens[idx].position, text)
    
    def _parse_elements(self, tokens, idx, text):
        """Parse element component"""
        elements = []
        
        # Parse first element
        try:
            element = ElementType(tokens[idx].value)
            elements.append(element)
            idx += 1
        except ValueError:
            raise ValidationError(f"Invalid element: {tokens[idx].value}", 
                                tokens[idx].position, text)
        
        # Check for additional elements (comma-separated)
        while idx < len(tokens) and tokens[idx].type == 'COMMA':
            idx += 1
            
            if idx >= len(tokens) or tokens[idx].type != 'ELEMENT':
                raise ValidationError("Expected element after ','", 
                                    tokens[idx-1].position + 1, text)
            
            try:
                element = ElementType(tokens[idx].value)
                elements.append(element)
                idx += 1
            except ValueError:
                raise ValidationError(f"Invalid element: {tokens[idx].value}", 
                                    tokens[idx].position, text)
        
        return elements, idx
    
    def _parse_extended_components(self, effect, tokens, text):
        """Parse extended components after the core components"""
        # Find the first delimiter if any
        delimiter_indices = [i for i, t in enumerate(tokens) if t.type == 'DELIMITER']
        
        if not delimiter_indices:
            return  # No extended components
        
        # Process each extended section
        for i in range(len(delimiter_indices)):
            start_idx = delimiter_indices[i] + 1
            end_idx = delimiter_indices[i+1] if i+1 < len(delimiter_indices) else len(tokens)
            
            if start_idx >= end_idx:
                continue  # Empty section
            
            self._parse_extended_section(effect, tokens[start_idx:end_idx], text)
    
    def _parse_extended_section(self, effect, section_tokens, text):
        """Parse a single extended component section"""
        # This is a simplified version - we'd need more complex logic for full parsing
        if not section_tokens:
            return
        
        first_token = section_tokens[0]
        
        # Handle different extended component types
        if first_token.type == 'REMOVABILITY':
            try:
                effect.removability = RemovabilityFlag(first_token.value)
            except ValueError:
                raise ValidationError(f"Invalid removability flag: {first_token.value}", 
                                    first_token.position, text)
                                    
        elif first_token.type == 'CHAIN_EFFECT':
            try:
                effect.chain_effect = ChainEffect(first_token.value)
            except ValueError:
                raise ValidationError(f"Invalid chain effect: {first_token.value}", 
                                    first_token.position, text)
        
        elif first_token.type == 'SOURCE_DEPENDENCY':
            try:
                effect.source_dependency = SourceDependency(first_token.value)
            except ValueError:
                raise ValidationError(f"Invalid source dependency: {first_token.value}", 
                                    first_token.position, text)
        
        elif first_token.type == 'VISIBILITY':
            try:
                effect.visibility = VisibilityFlag(first_token.value)
            except ValueError:
                raise ValidationError(f"Invalid visibility flag: {first_token.value}", 
                                    first_token.position, text)
        
        elif first_token.type == 'INTERACTION':
            try:
                effect.interaction_tag = InteractionTag(first_token.value)
            except ValueError:
                raise ValidationError(f"Invalid interaction tag: {first_token.value}", 
                                    first_token.position, text)
        
        elif first_token.type == 'SPECIAL_FLAG':
            effect.special_flags.append(first_token.value)
        
        elif first_token.type == 'SPECIAL_CONDITION' and first_token.value.startswith('#Gobstop'):
            effect.meta_effect = MetaEffect.GOBSTOPPER
            
        # Note: We'd need more complex parsing for stacking behavior, resource connections,
        # conditions, and other components that need additional information


# -----------------------------------------------------------------------------
# API Functions
# -----------------------------------------------------------------------------

def parse_esens(notation_string, explain=True):
    """
    Parse an ESENS notation string into a structured object.
    
    Args:
        notation_string: The ESENS notation to parse
        explain: Whether to include a human-readable explanation (default: True)
        
    Returns:
        A dictionary containing the parsed object, dict representation, and explanation
        
    Raises:
        ESENSParseError: If the notation string is invalid
    """
    parser = ESENSParser()
    return parser.parse(notation_string, explain)


def validate_esens(notation_string):
    """
    Validate an ESENS notation string without returning the parsed object.
    
    Args:
        notation_string: The ESENS notation to validate
        
    Returns:
        True if the notation is valid
        
    Raises:
        ESENSParseError: If the notation string is invalid
    """
    parser = ESENSParser()
    parser.parse(notation_string, explain=False)
    return True


# -----------------------------------------------------------------------------
# Examples and Testing
# -----------------------------------------------------------------------------

def run_examples():
    """Run some example parses to demonstrate functionality"""
    examples = [
        "P+S10%3T",  # Player gains 10% strength for 3 turns
        "E-D15C",    # Enemy loses 15 defense for combat duration
        "P#Stun1T",  # Player stunned for 1 turn
        "X-H5",      # All enemies take 5 damage
        "P+S10%3T.ST",  # Player gains 10% strength for 3 turns, stacking allowed
        "P+S10%3T>A.F",  # Player gains 10% Fire strength for 3 turns when attacking
        "E#Burn3T^S.DOT",  # Enemy burned for 3 damage at start of turn, damage over time
    ]
    
    for example in examples:
        try:
            result = parse_esens(example)
            print(f"\nParsed: {example}")
            print(f"Explanation: {result['explanation']}")
            print(f"Object: {result['dict']}")
        except ESENSParseError as e:
            print(f"\nError parsing {example}:")
            print(e)


if __name__ == "__main__":
    run_examples()
