import random
import time


class Area:

    def __init__(self, alignment, terrain=None, name=None):
        self.alignment = alignment
        self.name = name
        self.terrain = terrain
        self.capacity = 3

    def __repr__(self):
        if self.terrain == "capital":
            return "*"

        if self.alignment == "Germany":
            return "X"
        elif self.alignment == "Poland":
            return "≡"


class Unit:

    def __init__(self, name, strength, speed, size, alignment=None, coordinates=None):
        self.name = name
        self.strength = strength
        self.speed = speed
        self.size = size

        self.alignment = alignment
        # Indicates whose unit it is.

        self.coordinates = coordinates

        self.status = True
        # True when alive; false when dead.

        self.attack_status = True
        # whether or not the unit has attacked for the turn; set false when attacked;
        # set true when next_turn is called.

    def attack(self, enemy, others_friendly=None, others_hostile=None):

        if not self.attack_status:
            print("This unit has already attacked!")
            return

        combined_strength = self.strength
        combined_enemy = enemy.strength

        if others_friendly is not None:
            for friendly_unit in others_friendly:
                combined_strength += friendly_unit.strength

        if others_hostile is not None:
            for enemy_unit in others_hostile:
                combined_enemy += enemy_unit.strength

        introduction_str = self.name.upper()
        if others_friendly is not None:
            introduction_str += ", with reinforcement from {}".format\
                (str([friendly_unit for friendly_unit in others_friendly]))
        introduction_str += " attacks " + "{}".format(enemy.name.upper())
        if others_hostile is not None:
            introduction_str += ", with enemy support from {}".format\
                (str([enemy_unit for enemy_unit in others_hostile])) + "."
        print(introduction_str)

        dice_roll = random.randrange(2, 12)
        ratio = combined_strength / combined_enemy

        turn_index = ["You counter-attack ", "The enemy counter-attacks "]
        turn = 0

        attack_result = 7

        roll_index = ["You ", "They "]

        while (attack_result >= 3) and (attack_result <= 12):
            print(roll_index[turn % 2] + "roll a " + str(dice_roll) + "!")
            attack_result = self.attack_result(ratio, dice_roll, turn)

            turn += 1

            if attack_result == 12:
                ratio = 5
                print(turn_index[turn % 2] + "at 5 to 1 odds...")
            elif attack_result == 11:
                ratio = 4
                print(turn_index[turn % 2] + "at 4 to 1 odds...")
            elif attack_result == 10:
                ratio = 3
                print(turn_index[turn % 2] + "at 3 to 1 odds...")
            elif attack_result == 9:
                ratio = 2
                print(turn_index[turn % 2] + "at 2 to 1 odds...")
            elif attack_result == 8:
                ratio = 1
                print(turn_index[turn % 2] + "at 1 to 1 odds...")
            elif attack_result == 7:
                ratio = combined_strength / combined_enemy
                print(turn_index[turn % 2] + "at initial odds...")
            elif attack_result == 6:
                ratio = 0.5
                print(turn_index[turn % 2] + "at 1 to 2 odds...")
            elif attack_result == 5:
                ratio = 0.33
                print(turn_index[turn % 2] + "at 1 to 3 odds...")
            elif attack_result == 4:
                ratio = 0.25
                print(turn_index[turn % 2] + "at 1 to 4 odds...")
            elif attack_result == 3:
                ratio = 0
                print(turn_index[turn % 2] + "at 1 to 5 odds...")

            time.sleep(1.5)

            dice_roll = random.randrange(2, 12)

        else:
            if attack_result == 16:
                enemy.status = False
                self.status = False
                print("Exchanged!")
            elif attack_result == 15:
                enemy.status = False
                self.coordinates = enemy.coordinates
                print("Defender eliminated!")
            elif attack_result == 14:
                enemy.status = False
                self.coordinates = enemy.coordinates
                print("Defender 50% eliminated!")
            elif attack_result == 13:
                enemy.status = False
                self.coordinates = enemy.coordinates
                print("Defender retreat!")

            elif attack_result == 2:
                print("Attacker retreat!")
            elif attack_result == 1:
                print("Attacker 50% eliminated!")
            elif attack_result == 0:
                print("Attacker eliminated!")

        self.attack_status = False

    def attack_result(self, ratio, dice_roll, turn):

        combat_results = {"EX": 16, "DE": 15, "DR50": 14, "DR": 13, "CA51": 12, "CA41": 11, "CA31": 10, "CA21": 9,
                          "CA11": 8, "CA": 7, "CA12": 6, "CA13": 5, "CA14": 4, "CA15": 3, "AR": 2, "AR50": 1, "AE": 0}

        ratio_15 = [None, None, "AE", "AE", "AE", "AE", "AR50", "AR50", "AR", "AR", "CA41", "CA31", "CA"]
        ratio_14 = [None, None, "AE", "AE", "AE", "AR50", "AR50", "AR", "AR", "CA41", "CA31", "CA", "EX"]
        ratio_13 = [None, None, "AE", "AE", "AR50", "AR50", "AR", "AR", "CA31", "CA21", "CA", "EX", "DR"]
        ratio_12 = [None, None, "AE", "AR50", "AR50", "AR", "AR", "CA21", "CA11", "CA", "EX", "DR", "DR"]
        ratio_11 = [None, None, "AR50", "AR", "AR", "CA", "CA", "EX", "CA", "CA", "DR", "DR", "DR50"]
        ratio_21 = [None, None, "AR", "AR", "EX", "CA", "CA11", "CA12", "DR", "DR", "DR50", "DR50", "DE"]
        ratio_31 = [None, None, "AR", "EX", "CA", "CA12", "CA13", "DR", "DR", "DR50", "DR50", "DE", "DE"]
        ratio_41 = [None, None, "EX", "CA", "CA13", "CA14", "DR", "DR", "DR50", "DR50", "DE", "DE", "DE"]
        ratio_51 = [None, None, "CA", "CA13", "CA14", "DR", "DR", "DR50", "DR50", "DE", "DE", "DE", "DE"]

        if turn % 2 == 1:
            ratio = 1 / ratio

        if ratio >= 5:
            return combat_results[ratio_51[dice_roll]]
        elif ratio >= 4:
            return combat_results[ratio_41[dice_roll]]
        elif ratio >= 3:
            return combat_results[ratio_31[dice_roll]]
        elif ratio >= 2:
            return combat_results[ratio_21[dice_roll]]
        elif ratio >= 1:
            return combat_results[ratio_11[dice_roll]]
        elif ratio >= 0.5:
            return combat_results[ratio_12[dice_roll]]
        elif ratio >= 0.33:
            return combat_results[ratio_13[dice_roll]]
        elif ratio >= 0.25:
            return combat_results[ratio_14[dice_roll]]
        else:
            return combat_results[ratio_15[dice_roll]]

    def place(self, area):
        pass

    def move(self):
        pass

    def __repr__(self):
        return self.name


def board_setup(board):
    # Will set up a regular WWII map. For now, just Germany and Poland.

    for row in range(len(board)):
        for item in range(len(board[row])):
            if board[row][item] is not None:
                if board[row][item] == "X":
                    board[row][item] = Area("Germany")
                elif board[row][item] == "≡":
                    board[row][item] = Area("Poland")

    counter = 0
    for row in board:
        if counter % 2 == 0:
            print("  ", end="")
        counter += 1
        for item in row:
            if item is not None:
                print(item, " ", end="")
            else:
                print("   ", end="")
        print(end="\n")


def buy_units(game_type):

    inf_lst = [
        Unit("inf_1", 3, 3, 2),
        Unit("inf_2", 3, 3, 2),
        Unit("inf_3", 3, 3, 2),
        Unit("inf_4", 3, 3, 2),
        Unit("inf_5", 1, 3, 1),
        Unit("inf_6", 1, 3, 1)
    ]
    
    tank_lst = [
        Unit("tank_1", 4, 6, 2),
        Unit("tank_2", 4, 6, 2),
        Unit("tank_3", 4, 6, 2),
        Unit("tank_4", 4, 6, 2),
        Unit("tank_5", 2, 5, 1),
        Unit("tank_6", 2, 5, 1)
    ]

    air_lst = [
        Unit("intercept_1", 5, 4, 1),
        Unit("intercept_2", 5, 4, 1),
        Unit("bomber_1", 4, 6, 1),
        Unit("bomber_2", 4, 6, 1)
    ]

    garrison_lst = [
        Unit("garrison_1", 1, 0, 1),
        Unit("garrison_2", 1, 0, 1),
        Unit("garrison_3", 1, 0, 1),
        Unit("garrison_4", 1, 0, 1)
    ]

    purchased_units_p1 = []
    purchased_units_p2 = []

    currency_p1 = 100
    currency_p2 = 100

    print()
    print("It's time for player 1 to purchase units.", end="\n")
    print()

    print("You currently have $" + str(currency_p1))
    while 0 == 0:
        print()

        print("Enter 1 for Infantry, 2 for Tanks, 3 for Air power, 4 for Garrisons. Enter q to quit.")
        choice = input()

        choice_2 = None
        if choice == "1":
            while choice_2 != "q":
                print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                print()

                for number in range(len(inf_lst)):
                    print("{}. ".format(number+1) + inf_lst[number].name + " with strength {} and speed {} for ${}."
                          .format(inf_lst[number].strength, inf_lst[number].speed, inf_lst[number].strength * 4))
                    
                choice_2 = input()
                choices_lst = [str(number + 1) for number in range(len(inf_lst))]
                if choice_2 in choices_lst:
                    if currency_p1 - inf_lst[int(choice_2) - 1].strength * 4 >= 0:
                        purchased_units_p1.append(inf_lst.pop(int(choice_2) - 1))
                        currency_p1 -= (purchased_units_p1[-1].strength * 4)
                        print("You purchased {}!".format(purchased_units_p1[-1]))
                        print("You currently have $" + str(currency_p1))
                        print()
                    else:
                        print("Not sufficient funds!")
                        print()

        elif choice == "2":
            while choice_2 != "q":
                print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                print()

                for number in range(len(tank_lst)):
                    print("{}. ".format(number+1) + tank_lst[number].name +
                          " with strength {} and speed {} for ${}.".format
                          (tank_lst[number].strength, tank_lst[number].speed, tank_lst[number].strength * 6))

                choice_2 = input()
                choices_lst = [str(number + 1) for number in range(len(tank_lst))]
                if choice_2 in choices_lst:
                    if currency_p1 - tank_lst[int(choice_2) - 1].strength * 4 >= 0:
                        purchased_units_p1.append(tank_lst.pop(int(choice_2) - 1))
                        currency_p1 -= (purchased_units_p1[-1].strength * 4)
                        print("You purchased {}!".format(purchased_units_p1[-1]))
                        print("You currently have $" + str(currency_p1))
                        print()
                    else:
                        print("Not sufficient funds!")
                        print()

        elif choice == "3":
            while choice_2 != "q":
                print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                print()

                for number in range(len(air_lst)):
                    print("{}. ".format(number+1) + air_lst[number].name +
                          " with strength {} and speed {} for ${}.".format
                          (air_lst[number].strength, air_lst[number].speed, air_lst[number].speed * 6))

                choice_2 = input()
                choices_lst = [str(number + 1) for number in range(len(air_lst))]
                if choice_2 in choices_lst:
                    if currency_p1 - air_lst[int(choice_2) - 1].speed * 6 >= 0:
                        purchased_units_p1.append(air_lst.pop(int(choice_2) - 1))
                        currency_p1 -= (purchased_units_p1[-1].speed * 6)
                        print("You currently have $" + str(currency_p1))
                        print("You purchased {}!".format(purchased_units_p1[-1]))
                        print()

                    else:
                        print("Not sufficient funds!")
                        print()
                            
        elif choice == "4":
            while choice_2 != "q":
                print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                print()

                for number in range(len(garrison_lst)):
                    print("{}. ".format(number+1) + garrison_lst[number].name +
                          " with strength {} and speed {} for ${}.".format(garrison_lst[number].strength,
                               garrison_lst[number].speed, garrison_lst[number].strength * 3))

                choice_2 = input()
                choices_lst = [str(number + 1) for number in range(len(garrison_lst))]
                if choice_2 in choices_lst:
                    if currency_p1 - garrison_lst[int(choice_2) - 1].strength * 3 >= 0:
                        purchased_units_p1.append(garrison_lst.pop(int(choice_2) - 1))
                        currency_p1 -= (purchased_units_p1[-1].strength * 3)
                        print("You currently have $" + str(currency_p1))
                        print("You purchased {}!".format(purchased_units_p1[-1]))
                        print()
                    else:
                        print("Not sufficient funds!")
                        print()

        elif choice == "q":
            if not purchased_units_p1:
                print("Please purchase some units!")
            else:
                break

    if game_type == "S":
        return purchased_units_p1, None
    else:
        print()
        print("It's time for player 2 to purchase units.", end="\n")
        print()

        print("You currently have $" + str(currency_p2))
        while 0 == 0:
            print()

            print("Enter 1 for Infantry, 2 for Tanks, 3 for Air power, 4 for Garrisons. Enter q to quit.")
            choice = input()

            choice_2 = None
            if choice == "1":
                while choice_2 != "q":
                    print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                    print()

                    for number in range(len(inf_lst)):
                        print(
                            "{}. ".format(number + 1) + inf_lst[number].name + " with strength {} and speed {} for ${}."
                            .format(inf_lst[number].strength, inf_lst[number].speed, inf_lst[number].strength * 4))

                    choice_2 = input()
                    choices_lst = [str(number + 1) for number in range(len(inf_lst))]
                    if choice_2 in choices_lst:
                        if currency_p2 - inf_lst[int(choice_2) - 1].strength * 4 >= 0:
                            purchased_units_p2.append(inf_lst.pop(int(choice_2) - 1))
                            currency_p2 -= (purchased_units_p2[-1].strength * 4)
                            print("You purchased {}!".format(purchased_units_p2[-1]))
                            print("You currently have $" + str(currency_p2))
                            print()
                        else:
                            print("Not sufficient funds!")
                            print()

            elif choice == "2":
                while choice_2 != "q":
                    print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                    print()

                    for number in range(len(tank_lst)):
                        print("{}. ".format(number + 1) + tank_lst[number].name +
                              " with strength {} and speed {} for ${}.".format
                              (tank_lst[number].strength, tank_lst[number].speed, tank_lst[number].strength * 6))

                    choice_2 = input()
                    choices_lst = [str(number + 1) for number in range(len(tank_lst))]
                    if choice_2 in choices_lst:
                        if currency_p2 - tank_lst[int(choice_2) - 1].strength * 4 >= 0:
                            purchased_units_p2.append(tank_lst.pop(int(choice_2) - 1))
                            currency_p2 -= (purchased_units_p2[-1].strength * 4)
                            print("You purchased {}!".format(purchased_units_p2[-1]))
                            print("You currently have $" + str(currency_p2))
                            print()
                        else:
                            print("Not sufficient funds!")
                            print()

            elif choice == "3":
                while choice_2 != "q":
                    print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                    print()

                    for number in range(len(air_lst)):
                        print("{}. ".format(number + 1) + air_lst[number].name +
                              " with strength {} and speed {} for ${}.".format
                              (air_lst[number].strength, air_lst[number].speed, air_lst[number].speed * 6))

                    choice_2 = input()
                    choices_lst = [str(number + 1) for number in range(len(air_lst))]
                    if choice_2 in choices_lst:
                        if currency_p2 - air_lst[int(choice_2) - 1].speed * 6 >= 0:
                            purchased_units_p2.append(air_lst.pop(int(choice_2) - 1))
                            currency_p2 -= (purchased_units_p2[-1].speed * 6)
                            print("You currently have $" + str(currency_p2))
                            print("You purchased {}!".format(purchased_units_p2[-1]))
                            print()

                        else:
                            print("Not sufficient funds!")
                            print()

            elif choice == "4":
                while choice_2 != "q":
                    print("Enter the corresponding number to purchase the listed units. Enter q to quit.")
                    print()

                    for number in range(len(garrison_lst)):
                        print("{}. ".format(number + 1) + garrison_lst[number].name +
                              " with strength {} and speed {} for ${}.".format(garrison_lst[number].strength,
                                                                               garrison_lst[number].speed,
                                                                               garrison_lst[number].strength * 3))

                    choice_2 = input()
                    choices_lst = [str(number + 1) for number in range(len(garrison_lst))]
                    if choice_2 in choices_lst:
                        if currency_p2 - garrison_lst[int(choice_2) - 1].strength * 3 >= 0:
                            purchased_units_p2.append(garrison_lst.pop(int(choice_2) - 1))
                            currency_p2 -= (purchased_units_p2[-1].strength * 3)
                            print("You currently have $" + str(currency_p2))
                            print("You purchased {}!".format(purchased_units_p2[-1]))
                            print()
                        else:
                            print("Not sufficient funds!")
                            print()

            elif choice == "q":
                if not purchased_units_p2:
                    print("Please purchase some units!")
                else:
                    break

        return purchased_units_p1, purchased_units_p2


def place_units(units_p1, units_p2, board):
    board_setup(board)

    while 0 == 0:

        display_board(board)
        print()
        print("Please choose your unit (by number), and then the coordinates (row and then column, one by one), "
              "where you would like your units to be.")
        print()

        for number in range(len(units_p1)):
            print("{}. ".format(number + 1) + units_p1[number].name + " with strength {} and speed {}"
                  .format(units_p1[number].strength, units_p1[number].speed) + ". {}"
                  .format("[PLACED]" if units_p1[number].coordinates is not None else ""))
        print()

        while 0 == 0:
            unit = input()
            if 1 <= int(unit) <= len(units_p1):
                if units_p1[int(unit) - 1].coordinates is not None:
                    print("This unit is already placed!")
                else:
                    print(units_p1[int(unit) - 1].name + " chosen.")
                    break
            else:
                print("Please enter a valid number.")

        while 0 == 0:
            row = input()
            if 0 < int(row) <= len(board):
                print("Row {} chosen.".format(row))
                break
            else:
                print("Please enter a valid row.")

        while 0 == 0:
            column = input()
            if 0 < int(column) <= len(board[int(row) - 1]):
                print("Column {} chosen.".format(column))
                break
            else:
                print("Please enter a valid column")

        print()

        if board[int(row) - 1][int(column) - 1].alignment == "Germany":
            if units_p1[int(unit) - 1].size < board[int(row) - 1][int(column) - 1].capacity:
                board[int(row) - 1][int(column) - 1].capacity -= units_p1[int(unit) - 1].size
                units_p1[int(unit) - 1].coordinates = [row, column]
                print("{} is placed on coordinates {}, {}.".format(units_p1[int(unit) - 1].name,
                            units_p1[int(unit) - 1].coordinates[0], units_p1[int(unit) - 1].coordinates[1]))
            else:
                print("This area does not have enough capacity for this additional unit!")
        else:
            print("You cannot place units on enemy territory!")

            


def display_board(board):
    counter = 0
    for row in board:
        if counter % 2 == 0:
            print("  ", end="")
        counter += 1
        for item in row:
            if item is not None:
                print(item, " ", end="")
            else:
                print("   ", end="")
        print(end="\n")


def play_game(units_p1, units_p2):
    pass


def start_game():
    # Self-made board is needed to start the game.

    while 0 == 0:
        print("Single player or multi-player? (S/M)")
        game_type = input()
        if game_type == "S":
            break
        elif game_type == "M":
            break

    time.sleep(0.75)

    print()
    print("Germany's invasion of Poland. September 1st, 1939.")
    print("Here is the map:")
    print()

    time.sleep(1)

    board = [
        ["X", "X", "X", "X", "X", "≡", "X", "X", "≡", "≡"],
        ["X", "X", "X", "X", "X", "≡", "≡", "≡", "≡", "≡"],
        ["X", "X", "X", "X", "X", "≡", "≡", "≡", "≡"],
        [None, "X", "X", "X", "X", "X", "≡", "≡", "≡"],
        [None, "X", None, "X", "X"]
    ]

    board_setup(board)
    units_p1, units_p2 = buy_units(game_type)
    place_units(units_p1, units_p2, board)
    play_game(units_p1, units_p2)

def main():
    print()
    print("Welcome to the game!", end="\n")
    start_game()





if __name__ == '__main__':
    main()
