from .printer import Printer
from .enumeration import HitType
from .functions import wait_button
from .character import PlayableCharacter

class Battle:
    def __init__(self, heroes: list, enemies: list):
        self.heroes = heroes
        self.enemies = enemies
        self.printer = Printer()
        self.victory = False
    
    def check_HP(self, character):
        if character.HP < 1:
            self.printer.show_death(character)
            return True
        return False

    def remove_character(self, character):
        if isinstance(character, PlayableCharacter):
            self.heroes.remove(character)
            self.printer.add_log(f"- {character.name} died")
        else:
            self.enemies.remove(character)
    
    def end_condition(self) -> bool:
        if len(self.heroes) == 0:
            return True
        elif len(self.enemies) == 0:
            self.victory = True
            self.printer.add_log(f"- Enemies defeated!")
            return True
        else:
            return False
    
    def applyDamage(self, user, targets: list, skill):
        defeated = []
        for target in targets:
            damage = skill.use(user, target)
            if damage["hit"] == HitType.FAILED:
                self.printer.miss_hit(user)
            else:
                self.printer.show_damage(user=user, target=target, damage=damage["damage"], skill=skill)
                if damage["hit"] == HitType.CRIT:
                    self.printer.crit_hit()
                target.recieve_damage(damage["damage"], skill)
                self.printer.show_hp(target)
                if self.check_HP(target):
                    defeated.append(target)
        for char in defeated:
            self.remove_character(char)


    def main_loop(self):
        self.printer.message("Battle starts!")
        on_battle = True
        self.printer.add_log("- Battle started")
        self.printer.message("\nYour party:")
        self.printer.show_characters(self.heroes)
        self.printer.message("\nEnemy group:")
        self.printer.show_characters(self.enemies)
        wait_button()
        while on_battle:
            # Player's team
            for hero in self.heroes:
                self.printer.show_turn_start(hero)
                while True:
                    self.printer.show_skills(hero)
                    skill = hero.choose_action()
                    if skill:
                        if hero.check_MP(skill.cost):   
                            targets = skill.target_strategy.candidates(user=hero, allies=self.heroes, enemies=self.enemies)
                            if not targets[0] is None:
                                hero.change_MP(-skill.cost)
                                self.applyDamage(user=hero, targets=targets, skill=skill)
                                break
                        else:
                            self.printer.insuficient_MP(hero)
                    else:
                        self.printer.pass_turn(hero)
                        break
                self.printer.show_health(hero)
                wait_button()
                if self.end_condition():
                    on_battle = False
                    break
            # Enemy team
            for enemy in self.enemies:
                self.printer.show_turn_start(enemy)
                skill = enemy.choose_action()
                targets = skill.target_strategy.candidates(user=enemy, allies=self.enemies, enemies=self.heroes)
                self.applyDamage(user=enemy, targets=targets, skill=skill)
                self.printer.show_health(enemy)
                wait_button()
                if self.end_condition():
                    on_battle = False
                    break
                
        if self.victory:
            self.printer.show_victory()
        else:
            self.printer.show_defeat()
        return self.heroes