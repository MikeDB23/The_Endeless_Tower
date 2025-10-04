import random

def dice_roll(sides, dice) -> int:
    total = 0
    for i in range(dice):
        total += random.randint(1, sides)
    return total

def wait_button() -> None:
    input(f"\nPress enter to continue\n")

def choose_option(options: int) -> int:
    picked = -1
    while True:
        chosen = input(f"Option: ")
        try:
            picked = int(chosen)
        except:
            print(f"Value is not valid!")
        else:
            picked -= 1
            if picked >= 0 and picked <= options:
                return picked
            else:
                print(f"value out of range!")