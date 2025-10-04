class Printer:
    instance = None
    log = []

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def add_log(self, log: str):
        self.log.append(log)
    
    def show_log(self):
        for item in self.log:
            print(f"{item}")

    def message(self, message: str):
        print(f"{message}")

    def divide_rooms(self):
        print("_" * 80)

    def show_turn_start(self, character):
        print(f"\nIt's {character.name}'s turn")
        self.show_hp(character)
        self.show_mp(character)
    
    def show_health(self, character):
        print(f"\n{character.name}:")
        self.show_hp(character)
        self.show_mp(character)

    def show_hp(self, character):
        print(f"{character.health_bar()}")
    
    def show_mp(self, character):
        print(f"{character.mana_bar()}")

    def show_skills(self, character):
        print(f"\nWhat should {character.name} do?")
        for i, skill in enumerate(character.skills, start=1):
            print(f"[{i}] {skill.read_skill()}")
        print(f"[{len(character.skills) + 1}] Pass")
    
    def show_damage(self, user, target, damage: int, skill):
        print(f"\n{user.name} uses {skill.name} on {target.name} for {damage} hit points!")
    
    def show_victory(self):
        print(f"\nThe enemies have been slain!")
    
    def show_defeat(self):
        print(f"\nThe heroes have been defeated!")
    
    def choose_character(self, characters: list):
        print(f"\nChoose a target:")
        self.show_characters(characters)

    def show_characters(self, characters: list):
        for i, character in enumerate(characters, start=1):
            print(f"[{i}] {character.name} {character.health_bar()}")
    
    def show_death(self, character):
        print(f"\n{character.name} has fallen!")
    
    def insuficient_MP(self, character):
        print(f"\n{character.name} has not enough MP!")
    
    def pass_turn(self, character):
        print(f"\n{character.name} waits...")
    
    def miss_hit(self, character):
        print(f"\n{character.name}'s attack has failed!")

    def yes_no_question(self, question: str):
        print(f"{question}\n[1] Yes\n[2] No")

    def crit_hit(self):
        print(f"A critical hit!")