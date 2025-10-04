from abc import ABC, abstractmethod
from .functions import dice_roll
from .enumeration import HitType, Behavior
from .functions import choose_option


# Returns a list of valid targets for a skill
class Objective(ABC):
    @abstractmethod
    def candidates(self, user, allies, enemies):
        pass


# Skills
class Skill(ABC):
    flyweight = {}
    def __init__(self, name: str, description: str, attack_type, target_strategy, use_strategy, cost: int):
        self.name = name
        self.description = description
        self.cost = cost
        self.type = attack_type
        self.target_strategy = target_strategy
        self.use_strategy = use_strategy

    def __new__(cls, name, description, attack_type, target_strategy, use_strategy, cost):
        if name not in cls.flyweight:
            cls.flyweight[name] = super().__new__(cls)
        return cls.flyweight[name]

    def read_skill(self) -> str:
        return (f"{self.name}: {self.description}, {self.use_strategy.power} + {self.use_strategy.dice}d{self.use_strategy.die} ({self.cost} MP)")

    def roll_hit(self) -> int:
        return dice_roll(20, 1)

    @abstractmethod
    def use(self, user, target) -> int:
        pass

class DamageSkill(Skill):
    def use(self, user, target):
        roll = self.roll_hit()
        damage = self.use_strategy.calculate(user, target)
        if roll == 20:
            return {"damage": damage * 2, "hit": HitType.CRIT}
        elif roll == 1:
            return {"damage": 0, "hit": HitType.FAILED}
        else:
            return {"damage": damage, "hit": HitType.NORMAL}

class HealingSkill(Skill):
    def use(self, user, target):
        damage = self.use_strategy.calculate(user, target)
        return {"damage": damage, "hit": HitType.NORMAL}


class Attack(ABC):
    def __init__(self, power: int, die: int, dice: int):
        self.power = power
        self.die = die
        self.dice = dice
    @abstractmethod
    def calculate(self):
        pass

class PhysicalAttack(Attack):
    def __init__(self, power, die, dice):
        super().__init__(power, die, dice)

    def calculate(self, user, target):
        roll = dice_roll(sides= self.die, dice= self.dice)
        return  max(1, self.power + roll + user.get_ATK() - target.get_DEF())

class MagicalAttack(Attack):
    def __init__(self, power, die, dice):
        super().__init__(power, die, dice)

    def calculate(self, user, target):
        roll = dice_roll(sides=self.die, dice= self.dice)
        return max(1, self.power + roll + user.get_MAG() - target.get_RES())

class MagicalHeal(Attack):
    def __init__(self, power, die, dice):
        super().__init__(power, die, dice)

    def calculate(self, user, target):
        roll = dice_roll(sides=self.die, dice= self.dice)
        return self.power + roll + user.get_MAG()


class EnemyObjective(Objective):
    def candidates(self, user, allies: list, enemies: list):
        if user.behavior is Behavior.PLAYABLE:
            print(f"\nChoose a target:")
            for i, character in enumerate(enemies, start=1):
                print(f"[{i}] {character.name} {character.health_bar()}")
            print(f"[{len(enemies) + 1}] Back")
        return [user.pick_target(enemies)]

class AlliedObjective(Objective):
    def candidates(self, user, allies: list, enemies: list):
        if user.behavior is Behavior.PLAYABLE:
            print(f"\nChoose a target:")
            for i, character in enumerate(allies, start=1):
                print(f"[{i}] {character.name} {character.health_bar()}")
            print(f"[{len(allies) + 1}] Back")
        return [user.pick_target(allies)]

class AllEnemyObjective(Objective):
    def candidates(self, user, allies, enemies):
        if user.behavior is Behavior.PLAYABLE:
            print(f"\nChoose a target:\n[1] All")
            for character in enemies:
                print(f"{character.name} {character.health_bar()}")
            print(f"\n[2] Back")
            if choose_option(2) == 1:
                return [None]
        return enemies

class AllAlliedObjective(Objective):
    def candidates(self, user, allies, enemies):
        if user.behavior is Behavior.PLAYABLE:
            print(f"\nChoose a target:\n[1] All")
            for character in allies:
                print(f"{character.name} {character.health_bar()}")
            print(f"\n[2] Back")
            if choose_option(2) == 1:
                return [None]
        return allies

class SelfObjective(Objective):
    def candidates(self, user, allies, enemies):
        return [user]