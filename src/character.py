from abc import ABC, abstractmethod
import random
from .enumeration import Behavior, AttackType
from .functions import choose_option
from .skill import Skill, DamageSkill, HealingSkill, EnemyObjective, AlliedObjective, AllEnemyObjective, AllAlliedObjective, PhysicalAttack, MagicalAttack, MagicalHeal


class Character(ABC):
    @abstractmethod
    def __init__(self, name: str, HP: int, MP: int, ATK: int, MAG: int, DEF: int, RES: int):
        self.name = name
        self.MHP = HP
        self.HP = HP
        self.MMP = MP
        self.MP = MP
        self.ATK = ATK
        self.MAG = MAG
        self.DEF = DEF
        self.RES = RES
        self.skills = []
        self.behavior: Behavior = None
    
    def get_ATK(self):
        return self.ATK
    def get_DEF(self):
        return self.DEF
    def get_MAG(self):
        return self.MAG
    def get_RES(self):
        return self.RES

    @abstractmethod
    def choose_action(self) -> Skill:
        pass

    @abstractmethod
    def pick_target(self, targets):
        pass

    def check_MP(self, cost: int) -> bool:
        return self.MP >= cost

    def learn_skill(self, skill: Skill):
        self.skills.append(skill)

    def change_HP(self, ammount: int):
        self.HP += ammount
        if self.HP > self.MHP:
            self.HP = self.MHP
        elif self.HP < 0:
            self.HP = 0
    
    def change_MP(self, ammount: int):
        self.MP += ammount
        if self.MP > self.MMP:
            self.MP = self.MMP
        elif self.MP < 0:
            self.MP = 0

    def health_bar(self) -> str:
        percent = self.HP/self.MHP * 10
        dec = int(percent)
        partial = percent % 1 > 0
        return ("HP: [" + "X" * dec + "/" * partial + "-" * (10 - dec - partial) + f"] ({self.HP}/{self.MHP})")
    
    def mana_bar(self) -> str:
        if self.MMP > 0:
            percent = self.MP/self.MMP * 10
        else:
            percent = 0
        dec = int(percent)
        partial = percent % 1 > 0
        return ("MP: [" + "X" * dec + "/" * partial + "-" * (10 - dec - partial) + f"] ({self.MP}/{self.MMP})")

    def recieve_damage(self, damage: int, skill: Skill):
        if skill.type == AttackType.HEAL:
            self.change_HP(damage)
        else:
            self.change_HP(-damage)


class PlayableCharacter(Character):
    def __init__(self, name, HP, MP, ATK, MAG, DEF, RES):
        super().__init__(name, HP, MP, ATK, MAG, DEF, RES)
        self.behavior = Behavior.PLAYABLE
    
    def pick_target(self, targets: list[Character]) -> Character:
        option = choose_option(len(targets))
        if option == len(targets):
            return None
        else:
            return targets[option]

    def choose_action(self) -> Skill:
        option = choose_option(len(self.skills))
        if option == len(self.skills):
            return None
        else:
            return self.skills[option]

class EnemyCharacter(Character):
    def __init__(self, name, HP, MP, ATK, MAG, DEF, RES):
        super().__init__(name, HP, MP, ATK, MAG, DEF, RES)
        self.behavior = Behavior.BASIC
    
    def pick_target(self, targets: list[Character]) -> Character:
        return random.choice(targets)
    
    def choose_action(self) -> Skill:
        usable = []
        for skill in self.skills:
            if skill.cost <= self.MP:
                usable.append(skill)
        return random.choice(usable)


# Character factories
class CharacterFactory(ABC):
    @abstractmethod
    def create_character(self, name):
        pass

class MainCharacterFactory(CharacterFactory):
    def create_character(self, name):
        player = PlayableCharacter(name= name,HP=30, MP=20, ATK=6, MAG=5, DEF=5, RES=4)
        player.learn_skill(DamageSkill(name="Swing", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 1), cost=0))
        player.learn_skill(DamageSkill(name="Fire I", description="Magical attack, 1 foe", attack_type=AttackType.MAGICAL, target_strategy=EnemyObjective(), use_strategy=MagicalAttack(power=6, die=6, dice=1), cost=5))
        player.learn_skill(DamageSkill(name="Heal I", description="Restores HP, 1 ally", attack_type=AttackType.HEAL, target_strategy=AlliedObjective(), use_strategy=MagicalHeal(power=4, die=6, dice=1), cost=5))
        return player

class TravelerFactory(CharacterFactory):
    def create_character(self, name):
        option = random.randint(1, 5)
        match option:
            case 1: # Warrior
                traveler = PlayableCharacter(name=name, HP=50, MP=10, ATK=8, MAG=3, DEF=6, RES=3)
                traveler.learn_skill(DamageSkill(name="Swing", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 1), cost=0))
                traveler.learn_skill(DamageSkill(name="Axe-dive", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 4, die= 6, dice= 1), cost=2))
                traveler.learn_skill(DamageSkill(name="Cross slash", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 2), cost=2))
            case 2: # Mage
                traveler = PlayableCharacter(name=name, HP=20, MP=40, ATK=2, MAG=8, DEF=4, RES=6)
                traveler.learn_skill(DamageSkill(name="Mi-Fire", description="Magical attack, 1 foe", attack_type= AttackType.MAGICAL, target_strategy= EnemyObjective(), use_strategy= MagicalAttack(power= 1, die= 6, dice= 1), cost=0))
                traveler.learn_skill(DamageSkill(name="Fire I", description="Magical attack, 1 foe", attack_type=AttackType.MAGICAL, target_strategy=EnemyObjective(), use_strategy=MagicalAttack(power=6, die=6, dice=1), cost=5))
                traveler.learn_skill(DamageSkill(name="Al-Fire I", description="Magical attack, all foes", attack_type=AttackType.MAGICAL, target_strategy=AllEnemyObjective(), use_strategy=MagicalAttack(power=6, die=6, dice=1), cost=10))
            case 3: # Assassin
                traveler = PlayableCharacter(name=name, HP=40, MP=20, ATK=6, MAG=5, DEF=5, RES=4)
                traveler.learn_skill(DamageSkill(name="Stab", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 4, dice= 2), cost=0))
                traveler.learn_skill(DamageSkill(name="Al-Thunder I", description="Magical attack, all foes", attack_type=AttackType.MAGICAL, target_strategy=AllEnemyObjective(), use_strategy=MagicalAttack(power=6, die=6, dice=1), cost=10))
                traveler.learn_skill(DamageSkill(name="Close combat", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 20, dice= 1), cost=4))
            case 4: # Healer
                traveler = PlayableCharacter(name=name, HP=25, MP=35, ATK=1, MAG=8, DEF=5, RES=6)
                traveler.learn_skill(DamageSkill(name="Mi-Wind", description="Magical attack, 1 foe", attack_type= AttackType.MAGICAL, target_strategy= EnemyObjective(), use_strategy= MagicalAttack(power= 1, die= 6, dice= 1), cost=0))
                traveler.learn_skill(HealingSkill(name="Heal I", description="Restores HP, 1 ally", attack_type=AttackType.HEAL, target_strategy=AlliedObjective(), use_strategy=MagicalHeal(power=4, die=6, dice=1), cost=5))
                traveler.learn_skill(HealingSkill(name="Al-Heal I", description="Restores HP, party", attack_type=AttackType.HEAL, target_strategy=AllAlliedObjective(), use_strategy=MagicalHeal(power=4, die=6, dice=1), cost=10))
            case 5: # AoE
                traveler = PlayableCharacter(name=name, HP=20, MP=40, ATK=4, MAG=6, DEF=5, RES=5)
                traveler.learn_skill(DamageSkill(name="Arrow", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 1, die= 12, dice= 1), cost=0))
                traveler.learn_skill(DamageSkill(name="Arrow rain", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= AllEnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 10, dice= 1), cost=4))
                traveler.learn_skill(DamageSkill(name="Al-Blizzard I", description="Magical attack, all foes", attack_type=AttackType.MAGICAL, target_strategy=AllEnemyObjective(), use_strategy=MagicalAttack(power=6, die=6, dice=1), cost=10))
        return traveler

class MimicFactory(CharacterFactory):
    def create_character(self, name):
        mimic = EnemyCharacter(name= name + " mimic", HP=30, MP=0, ATK=4, MAG=2, DEF=4, RES=5)
        mimic.learn_skill(DamageSkill(name="Bite", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 1), cost=0))
        mimic.learn_skill(DamageSkill(name="Tackle", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 1), cost=0))
        return mimic

class EnemyFactory(CharacterFactory):
    def create_character(self, name):
        match random.randint(1, 4):
            case 1: # Slime
                enemy = EnemyCharacter(name="Slime", HP=15, MP=0, ATK=3, MAG=1, DEF=3, RES=4)
                enemy.learn_skill(DamageSkill(name="Tackle", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 1), cost=0))
            case 2: # Goblin
                enemy = EnemyCharacter(name="Goblin", HP=25, MP=10, ATK=5, MAG=1, DEF=5, RES=2)
                enemy.learn_skill(DamageSkill(name="Pierce", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 1), cost=0))
                enemy.learn_skill(DamageSkill(name="Spear-dive", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 4, die= 6, dice= 1), cost=2))
            case 3: # Orc
                enemy = EnemyCharacter(name="Orc", HP=40, MP=10, ATK=3, MAG=1, DEF=3, RES=4)
                enemy.learn_skill(DamageSkill(name="Smash", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 1), cost=0))
                enemy.learn_skill(DamageSkill(name="Cross slash", description="Physical attack, 1 foe", attack_type= AttackType.PHYSICAL, target_strategy= EnemyObjective(), use_strategy= PhysicalAttack(power= 2, die= 6, dice= 2), cost=2))
            case 4: # Wizard
                enemy = EnemyCharacter(name="Wizard", HP=20, MP=20, ATK=1, MAG=6, DEF=2, RES=5)
                enemy.learn_skill(DamageSkill(name="Mi-Wind", description="Magical attack, 1 foe", attack_type= AttackType.MAGICAL, target_strategy= EnemyObjective(), use_strategy= MagicalAttack(power= 1, die= 6, dice= 1), cost=0))
                enemy.learn_skill(DamageSkill(name="Thunder I", description="Magical attack, 1 foe", attack_type=AttackType.MAGICAL, target_strategy=EnemyObjective(), use_strategy=MagicalAttack(power=6, die=6, dice=1), cost=5))
        return enemy


class CharacterDecorator(Character):
    def __init__(self, character: Character):
        self.character = character
    
    def get_ATK(self):
        return self.character.get_ATK()