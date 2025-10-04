from src import MainCharacterFactory, Dungeon

if __name__ == "__main__":
    player_name = input("\nPlease enter your name: ")
    player = MainCharacterFactory().create_character(player_name)
    dungeon = Dungeon([player])
    dungeon.cicle()