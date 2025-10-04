import random
from abc import ABC, abstractmethod
from .printer import Printer
from .functions import choose_option, wait_button
from .character import EnemyFactory, MimicFactory, TravelerFactory
from .battle import Battle

class Room(ABC):
    def __init__(self, center: str, description: str):
        self.center = center
        self.description = description
        self.printer = Printer()

    def sequence(self, party: list) -> bool:
        self.intro()
        self.room_description()
        return self.action(party)

    def intro(self):
        self.printer.divide_rooms()
        self.printer.message(f"\n\nYou enter a room with {self.center}.")
    
    def room_description(self):
        print(self.description)

    @abstractmethod
    def action(self, party: list) -> bool:
        pass

class FountainRoom(Room):
    def action(self, party):
        self.printer.yes_no_question("Will you drink from it?")
        drink = choose_option(2)
        if drink == 0:
            self.printer.message("\nDrinking from it soothes both body and spirit.\nEveryone has their HP and MP restored!")
            for member in party:
                member.change_HP(member.MHP)
                member.change_MP(member.MMP)
                self.printer.add_log(f"- Restored health at the fountain")
        else:
            self.printer.message("\nYou ignore the water and continue your way.")
            self.printer.add_log(f"- Passed by a fountain")
        return party

class BattleRoom(Room):
    def __init__(self, center, description, enemies):
        super().__init__(center, description)
        self.enemies = enemies

    def action(self, party):
        enemies = self.enemies
        battle = Battle(heroes=party, enemies=enemies)
        return battle.main_loop()

class AdventurerRoom(Room):
    def action(self, party):
        self.printer.yes_no_question("Will you ask the adventurer to join you?")
        self.printer.add_log(f"- Found another adventurer")
        partner = choose_option(2)
        if partner == 0:
            names = ["Alex", "Sam", "Harper", "Charlie", "Avery", "Blake", "Ashley", "Robin", "Jessie", "River", "Quinn"]
            adventurer = TravelerFactory().create_character(random.choice(names))
            self.printer.message(f"\nYou ask them to join forces with you, it should make surviving easier for everyone.\n{adventurer.name} has joined your party!")
            party.append(adventurer)
            self.printer.add_log(f"- {adventurer.name} joined the party")
        else:
            self.printer.message("\nYou leave them behind, maybe you should not trust random people on this place.")
        return party


class MimicRoom(Room):
    def __init__(self, center, description, disguise: str, mimic: str):
        super().__init__(center, description)
        self.disguise = disguise
        self.mimic = mimic

    def action(self, party):
        self.printer.yes_no_question(f"Will you {self.disguise}?")
        option = choose_option(2)
        if option == 0:
            self.printer.message("\nAs you get closer, it suddenly shivers and wobbles.\nThe mimic reveals itself after you fell for its trap!")
            enemy = [MimicFactory().create_character(self.mimic)]
            battle = Battle(heroes=party, enemies=enemy)
            self.printer.add_log(f"- Fell for the trap of the mimic")
            return battle.main_loop()
        else:
            self.printer.message("\nYou quickly avoid it and go to the next room.")
            self.printer.add_log(f"- Avoided the trap of the mimic")
            return party


class RoomFactory(ABC):
    @abstractmethod
    def create_room(self) -> Room:
        pass

class FountainFactory(RoomFactory):
    def create_room(self) -> Room:
        match random.randint(1, 4):
            case 1:
                return FountainRoom(center="a crystal spring", description="A pool of pristine water glows with a pale blue light, rippling gently as if stirred by unseen hands.")
            case 2:
                return FountainRoom(center="a pedestal", description="On the pedestal rests a simple chalice brimming with liquid light.")
            case 3:
                return FountainRoom(center="a blood-red spring", description="The water glows faintly crimson, unsettling yet strangely tentative.")
            case 4:
                return FountainRoom(center="an overgrown well", description="Roots and moss cling to a broken well, yet its waters remain impossibly pure")

class EnemyRoomFactory(RoomFactory):
    def create_room(self) -> Room:
        enemies = []
        total = random.randint(1, 3)
        for i in range(total):
            enemies.append(EnemyFactory().create_character(name=""))
        return BattleRoom(center="shadowy figures", description="The figures get closer, get ready to fight!", enemies=enemies)

class TravelerRoomFactory(RoomFactory):
    def create_room(self) -> Room:
        return AdventurerRoom(center="another adventurer taking a break", description="The other adventurer looks at you and nods.")

class MimicRoomFactory(RoomFactory):
    def create_room(self):
        match random.randint(1, 2):
            case 1:
                room = MimicRoom(center="a pedestal", description="On the pedestal rests a luxurious chalice brimming with a dark liquid.", disguise="drink from it", mimic="chalice")
            case 2:
                room = MimicRoom(center="another adventurer taking a break", description="The other adventurer stares at you.", disguise="ask the adventurer to join you", mimic="adventurer")
        return room


class Dungeon:
    def __init__(self, party):
        self.current = 0
        self.party = party
        self.printer = Printer()

    def game_over(self):
        self.printer.divide_rooms()
        match random.randint(1, 4):
            case 1:
                self.printer.message("\nThe tower swallows your final breath. Another soul lost in its endless halls.")
            case 2:
                self.printer.message("\nYou collapse into the silence. The next door will remain unopened.")
            case 3:
                self.printer.message("\nThe walls close in, erasing your presence as though you never entered.")
            case 4:
                self.printer.message("\nYou fall down. Not even the carrion eaters are interested in your now cursed corpse.")
        self.printer.divide_rooms()
        self.printer.message(f"\n\nGAME OVER\nYou got througt {self.current} rooms\n")
        wait_button()
        self.printer.add_log("End of the run")
        self.printer.show_log()

    def enter_room(self) -> bool:
        chance = random.randint(1, 5)
        if chance == 1:
            room = FountainFactory().create_room()
        elif chance == 2:
            room = TravelerRoomFactory().create_room()
        elif chance == 3:
            room = MimicRoomFactory().create_room()
        else:
            room = EnemyRoomFactory().create_room()
        return room.sequence(self.party)

    def cicle(self):
        alive = True
        print(f"""
The tower's doors open without a sound. Beyond them lies only darkness, and the promise of endless rooms.
It waits in silence, daring you to step inside...

They call it the Endless Tower.

No map can chart it, no adventurer has ever seen its summit. Its halls bend back on themselves, rooms
repeat yet never match, and stairways climb both up and down at once.

Some say the tower was built by the gods. Others, that it has a mind of its own, forever growing. Many
have entered seeking glory, riches, or the truth at its heart. Few have returned, and none agree on what
they saw.

Yet still, adventurers gather at its gates. For within its shifting walls lies a promise: that somewhere
beyond the endless doors… lies the entrance to the land of the gods, and the chance to receive the sacred
blessing.

You enter the first room, and already the exit behind you is gone. The only way is forward, deeper into
the unknown. Every step you take echoes endlessly. The tower feels empty, yet you know it is watching.\n\n""")
        wait_button()
        while alive:
            self.current += 1
            self.printer.add_log(f"Entered room {self.current}")
            self.party = self.enter_room()
            if len(self.party) == 0:
                alive = False
            wait_button()
        self.game_over()