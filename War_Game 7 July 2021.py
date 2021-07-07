import random
import time


class Area:

    def __init__(self, alignment, terrain=None, name=None):
        self.alignment = alignment
        self.name = name
        self.terrain = terrain
        self.capacity = 3
        self.coordinates = []
        self.units = []

        self.upper_right = None
        self.upper_left = None
        self.right = None
        self.left = None
        self.bottom_right = None
        self.bottom_left = None

    def set_boundaries(self, board):
        """ Once called upon, sets upper right, left, etc. to other Areas. This is so that, when Unit.move() is called,
        the Unit can move its coordinates how many regions it wants, upper right, left, etc. to its designated area.
            Because of the way the dot map is set up, there needs to be two conditions for upper right, upper left,
        bottom left, and bottom right.
        """

        try:
            if self.coordinates[0] % 2 == 0:
                self.upper_right = board[self.coordinates[0] - 1][self.coordinates[1] + 1]
            else:
                self.upper_right = board[self.coordinates[0] - 1][self.coordinates[1]]
        except IndexError:
            self.upper_right = None

        try:
            if self.coordinates[0] % 2 == 0:
                self.upper_left = board[self.coordinates[0] - 1][self.coordinates[1]]
            else:
                self.upper_left = board[self.coordinates[0] - 1][self.coordinates[1] - 1]
        except IndexError:
            self.upper_left = None

        try:
            self.right = board[self.coordinates[0]][self.coordinates[1] + 1]
        except IndexError:
            self.right = None

        try:
            self.left = board[self.coordinates[0]][self.coordinates[1] - 1]
        except IndexError:
            self.left = None

        try:
            if self.coordinates[0] % 2 == 0:
                self.bottom_right = board[self.coordinates[0] + 1][self.coordinates[1] + 1]
            else:
                self.bottom_right = board[self.coordinates[0] + 1][self.coordinates[1]]
        except IndexError:
            self.bottom_right = None

        try:
            if self.coordinates[0] % 2 == 0:
                self.bottom_left = board[self.coordinates[0] + 1][self.coordinates[1]]
            else:
                self.bottom_left = board[self.coordinates[0] + 1][self.coordinates[1] - 1]
        except IndexError:
            self.bottom_left = None

    def __repr__(self):
        if self.terrain == "capital":
            return "*"

        lst_capacity = ["≡", "=", "-", "o"]
        if self.alignment == "Germany" and not self.units:
            return "\033[31m" + lst_capacity[self.capacity] + "\033[39m"
        elif self.alignment == "Poland" and not self.units:
            return "\033[32m" + lst_capacity[self.capacity] + "\033[39m"
        elif self.units[0].alignment == "Germany":
            return "\033[31m" + lst_capacity[self.capacity] + "\033[39m"
        elif self.units[0].alignment == "Poland":
            return "\033[32m" + lst_capacity[self.capacity] + "\033[39m"


class Unit:

    def __init__(self, name, strength, speed, size, alignment=None, coordinates=None):
        self.name = name
        self.strength = strength
        self.speed = speed
        self.size = size

        self.movement = speed

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

        dice_roll = random.randint(2, 12)
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

            dice_roll = random.randint(2, 12)

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

    def move(self, board, direction):
        unit_area = board[self.coordinates[0]][self.coordinates[1]]

        if direction == "upper_right":
            if unit_area.upper_right.units and unit_area.upper_right.units[0].alignment != self.alignment:
                print()
                print("There are enemy units in this region. Attack first!")
                return
            if unit_area.upper_right is None:
                print("Out of bounds!")
                print()
                return
            if unit_area.upper_right.capacity - self.size > 0:
                unit_area.upper_right.capacity -= self.size
                unit_area.upper_right.units.append(self)
                if self.coordinates[0] % 2 == 0:
                    self.coordinates[0] -= 1
                    self.coordinates[1] += 1
                else:
                    self.coordinates[0] -= 1
                print("Unit moved!")
            else:
                print("Not enough capacity for this unit!")
                return

        if direction == "upper_left":
            if unit_area.upper_left.units and unit_area.upper_left.units[0].alignment != self.alignment:
                print()
                print("There are enemy units in this region. Attack first!")
                return
            if unit_area.upper_left is None:
                print("Out of bounds!")
                print()
                return
            if unit_area.upper_left.capacity - self.size > 0:
                unit_area.upper_left.capacity -= self.size
                unit_area.upper_left.units.append(self)
                if self.coordinates[0] % 2 == 0:
                    self.coordinates[0] -= 1
                else:
                    self.coordinates[0] -= 1
                    self.coordinates[1] -= 1
                print("Unit moved!")
            else:
                print("Not enough capacity for this unit!")
                return

        if direction == "right":
            if unit_area.right.units and unit_area.right.units[0].alignment != self.alignment:
                print()
                print("There are enemy units in this region. Attack first!")
                return
            if unit_area.right is None:
                print("Out of bounds!")
                print()
                return
            if unit_area.right.capacity - self.size > 0:
                unit_area.right.capacity -= self.size
                unit_area.right.units.append(self)
                self.coordinates[1] += 1
                print("Unit moved!")
            else:
                print("Not enough capacity for this unit!")
                return

        if direction == "left":
            if unit_area.left.units and unit_area.left.units[0].alignment != self.alignment:
                print()
                print("There are enemy units in this region. Attack first!")
                return
            if unit_area.left is None:
                print("Out of bounds!")
                print()
                return
            if unit_area.left.capacity - self.size > 0:
                unit_area.left.capacity -= self.size
                unit_area.left.units.append(self)
                self.coordinates[1] -= 1
                print("Unit moved!")
            else:
                print("Not enough capacity for this unit!")
                return

        if direction == "bottom_right":
            if unit_area.bottom_right.units and unit_area.bottom_right.units[0].alignment != self.alignment:
                print()
                print("There are enemy units in this region. Attack first!")
                return
            if unit_area.bottom_right is None:
                print("Out of bounds!")
                print()
                return
            if unit_area.bottom_right.capacity - self.size > 0:
                unit_area.bottom_right.capacity -= self.size
                unit_area.bottom_right.units.append(self)
                if self.coordinates[0] % 2 == 0:
                    self.coordinates[0] += 1
                    self.coordinates[1] += 1
                else:
                    self.coordinates[0] += 1
                print("Unit moved!")
            else:
                print("Not enough capacity for this unit!")
                return

        if direction == "bottom_left":
            if unit_area.bottom_left.units and unit_area.bottom_left.units[0].alignment != self.alignment:
                print()
                print("There are enemy units in this region. Attack first!")
                return
            if unit_area.bottom_left is None:
                print("Out of bounds!")
                print()
                return
            if unit_area.bottom_left.capacity - self.size > 0:
                unit_area.bottom_left.capacity -= self.size
                unit_area.bottom_left.units.append(self)
                if self.coordinates[0] % 2 == 0:
                    self.coordinates[0] += 1
                else:
                    self.coordinates[0] += 1
                    self.coordinates[1] -= 1
                print("Unit moved!")
            else:
                print("Not enough capacity for this unit!")
                return

        unit_area.capacity += self.size
        unit_area.units.remove(self)
        self.movement -= 1
        print("Unit {} moved to coordinates {}.".format(self.name, [self.coordinates[0] + 1, self.coordinates[1] + 1]))
        print()

    def retreat(self, board):
        pass

    def destroyed(self, board):
        board[self.coordinates[0]][self.coordinates[1]].units.remove(self)
        board[self.coordinates[0]][self.coordinates[1]].capacity += self.size

    def __repr__(self):
        return self.name


def board_setup(board):
    # Will set up a regular WWII map. For now, just Germany and Poland.

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] is not None:
                if board[row][column] == "X":
                    board[row][column] = Area("Germany")
                elif board[row][column] == "+":
                    board[row][column] = Area("Poland")
                board[row][column].coordinates = [row, column]

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] is not None:
                board[row][column].set_boundaries(board)

    counter = 0
    for row in board:
        if counter % 2 == 0:
            print("  ", end="")
        counter += 1
        for column in row:
            if column is not None:
                print(column, " ", end="")
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
                        purchased_units_p1[-1].alignment = "Germany"
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
                        purchased_units_p1[-1].alignment = "Germany"
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
                        purchased_units_p1[-1].alignment = "Germany"
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
                        purchased_units_p1[-1].alignment = "Germany"
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
                            purchased_units_p2[-1].alignment = "Poland"
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
                            purchased_units_p2[-1].alignment = "Poland"
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
                            purchased_units_p2[-1].alignment = "Poland"
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
                                garrison_lst[number].speed, garrison_lst[number].strength * 3))

                    choice_2 = input()
                    choices_lst = [str(number + 1) for number in range(len(garrison_lst))]
                    if choice_2 in choices_lst:
                        if currency_p2 - garrison_lst[int(choice_2) - 1].strength * 3 >= 0:
                            purchased_units_p2.append(garrison_lst.pop(int(choice_2) - 1))
                            currency_p2 -= (purchased_units_p2[-1].strength * 3)
                            purchased_units_p2[-1].alignment = "Poland"
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
    unit = None

    placed_p1 = []
    placed_p2 = []

    while unit != "START":
        print()
        print("Player 1, please choose your unit (by number), and then the coordinates (row and then "
              "column, one by one), where you would like your units to be.")
        print("Enter START to start the battle.")
        print()

        for number in range(len(units_p1)):
            print("{}. ".format(number + 1) + units_p1[number].name + " with strength {} and speed {}"
                  .format(units_p1[number].strength, units_p1[number].speed) + ". {}"
                  .format("[PLACED]" if units_p1[number].coordinates is not None else ""))
        print()

        while 0 == 0:
            unit = input()
            if unit == "START" and len(units_p1) != len(placed_p1):
                print("Please finish placing all of your units!")
                unit = None
            elif unit == "START":
                break

            if unit is None:
                break

            if 1 <= int(unit) <= len(units_p1):
                if units_p1[int(unit) - 1].coordinates is not None:
                    print("This unit is already placed!")
                else:
                    print(units_p1[int(unit) - 1].name + " chosen.")
                    break
            else:
                print("Please enter a valid number.")

        if unit == "START":
            break

        if unit is None:
            continue

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

        none_num = 0
        for number in range(int(column)):
            if board[int(row) - 1][number] is None:
                none_num += 1

        if board[int(row) - 1][int(column) - 1 + none_num].alignment == "Germany":
            if units_p1[int(unit) - 1].size <= board[int(row) - 1][int(column) - 1 + none_num].capacity:

                board[int(row) - 1][int(column) - 1 + none_num].capacity -= units_p1[int(unit) - 1].size
                units_p1[int(unit) - 1].coordinates = [int(row) - 1, int(column) - 1 + none_num]
                placed_p1.append(units_p1[int(unit) - 1])
                board[int(row) - 1][int(column) - 1 + none_num].units.append(placed_p1[-1])

                print("{} is placed on coordinates {}, {}.".format(units_p1[int(unit) - 1].name,
                    units_p1[int(unit) - 1].coordinates[0] + 1, units_p1[int(unit) - 1].coordinates[1] + 1))
                print()

                update_board(board)

            else:
                print()
                print("This area does not have enough capacity for this additional unit!")
        else:
            print()
            print("You cannot place units on enemy territory!")

    print()

    unit = None
    if units_p2 is not None:
        update_board(board)
        while unit != "START":
            print()
            print("Player 2, please choose your unit (by number), and then the coordinates (row and then "
             "column, one by one), where you would like your units to be.")
            print("Enter START to start the battle.")
            print()

            for number in range(len(units_p2)):
                print("{}. ".format(number + 1) + units_p2[number].name + " with strength {} and speed {}"
                      .format(units_p2[number].strength, units_p2[number].speed) + ". {}"
                      .format("[PLACED]" if units_p2[number].coordinates is not None else ""))
            print()

            while 0 == 0:
                unit = input()
                if unit == "START" and len(units_p2) != len(placed_p2):
                    print("Please finish placing all of your units!")
                    unit = None
                elif unit == "START":
                    break

                if unit is None:
                    break

                if 1 <= int(unit) <= len(units_p2):
                    if units_p2[int(unit) - 1].coordinates is not None:
                        print("This unit is already placed!")
                    else:
                        print(units_p2[int(unit) - 1].name + " chosen.")
                        break
                else:
                    print("Please enter a valid number.")

            if unit == "START":
                break

            if unit is None:
                continue

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

            none_num = 0
            for number in range(int(column)):
                if board[int(row) - 1][number] is None:
                    none_num += 1

            if board[int(row) - 1][int(column) - 1 + none_num].alignment == "Poland":
                if units_p2[int(unit) - 1].size <= board[int(row) - 1][int(column) - 1 + none_num].capacity:

                    board[int(row) - 1][int(column) - 1 + none_num].capacity -= units_p2[int(unit) - 1].size
                    units_p2[int(unit) - 1].coordinates = [int(row) - 1, int(column) - 1 + none_num]
                    placed_p2.append(units_p2[int(unit) - 1])
                    board[int(row) - 1][int(column) - 1 + none_num].units.append(placed_p2[-1])

                    print("{} is placed on coordinates {}, {}.".format(units_p2[int(unit) - 1].name,
                        units_p2[int(unit) - 1].coordinates[0], units_p2[int(unit) - 1].coordinates[1]))
                    print()

                    update_board(board)

                else:
                    print()
                    print("This area does not have enough capacity for this additional unit!")
            else:
                print()
                print("You cannot place units on enemy territory!")
    else:

        units_poland = [
            Unit("inf_1", 2, 3, 2, "Poland"),
            Unit("inf_2", 2, 3, 2, "Poland"),
            Unit("inf_3", 2, 3, 2, "Poland"),
            Unit("inf_4", 1, 3, 1, "Poland"),
            Unit("inf_5", 1, 3, 1, "Poland"),
            Unit("intercept_1", 1, 4, 1, "Poland"),
            Unit("cav_1", 1, 4, 1, "Poland"),
            Unit("cav_2", 1, 4, 1, "Poland"),
            Unit("cav_3", 1, 4, 1, "Poland")
        ]

        print("Placing enemy troops...")
        time.sleep(1)

        for number in range(len(units_poland)):

            while units_poland[number].coordinates is None:
                row = random.randint(0, len(board)-1)
                column = random.randint(0, len(board[row])-1)
                if board[row][column] is None:
                    continue

                if board[row][column].alignment == "Poland":
                    if units_poland[number].size <= board[row][column].capacity:
                        board[row][column].capacity -= units_poland[number].size
                        units_poland[number].coordinates = [row, column]
                        placed_p2.append(units_poland[row])
                        board[row][column].units.append(placed_p2[-1])

        print()

        update_board(board)


def update_board(board):

    counter = 0
    for row in board:
        if counter % 2 == 0:
            print("  ", end="")
        counter += 1
        for column in row:
            if column is not None:
                print(column, " ", end="")
            else:
                print("   ", end="")
        print(end="\n")


def next_turn(units_p1, units_p2):
    pass


def move_unit(unit, board):

    if unit.movement == 0:
        print("No more movements for this unit!")
        return

    again_condition = "Y"

    while again_condition == "Y":

        update_board(board)
        print()
        print("Where would you like to move {}?".format(unit.name))
        print()

        while 0 == 0:
            print("1. Upper-right" + "\n" + "2. Upper-left" + "\n" + "3. Right" + "\n" +
                  "4. Left" + "\n" + "5. Bottom-right" + "\n" + "6. Bottom-left")

            direction_chosen = input()

            if direction_chosen == "1":
                unit.move(board, "upper_right")
                break
            elif direction_chosen == "2":
                unit.move(board, "upper_left")
                break
            elif direction_chosen == "3":
                unit.move(board, "right")
                break
            elif direction_chosen == "4":
                unit.move(board, "left")
                break
            elif direction_chosen == "5":
                unit.move(board, "bottom_right")
                break
            elif direction_chosen == "6":
                unit.move(board, "bottom_left")
                break
            else:
                print("Please choose a valid direction.")

        update_board(board)
        print()

        while unit.movement > 0:
            print("Would you like to keep moving this unit? (Y/N)")
            again_condition = input()
            if again_condition == "Y":
                break
            elif again_condition == "N":
                return
        else:
            again_condition = "N"


def check_surrounding_units_different_alignment(unit, board, avoid=None):
    conditions_lst = []

    if avoid is not None and avoid != "Bottom left":
        if board[unit.coordinates[0]][unit.coordinates[1]].upper_right:
            if board[unit.coordinates[0]][unit.coordinates[1]].upper_right.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].upper_right.units[0].alignment != unit.alignment:
                    conditions_lst.append(0)
    elif avoid is None:
        if board[unit.coordinates[0]][unit.coordinates[1]].upper_right:
            if board[unit.coordinates[0]][unit.coordinates[1]].upper_right.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].upper_right.units[0].alignment != unit.alignment:
                    conditions_lst.append(0)

    if avoid is not None and avoid != "Bottom right":
        if board[unit.coordinates[0]][unit.coordinates[1]].upper_left:
            if board[unit.coordinates[0]][unit.coordinates[1]].upper_left.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].upper_left.units[0].alignment != unit.alignment:
                    conditions_lst.append(1)
    elif avoid is None:
        if board[unit.coordinates[0]][unit.coordinates[1]].upper_left:
            if board[unit.coordinates[0]][unit.coordinates[1]].upper_left.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].upper_left.units[0].alignment != unit.alignment:
                    conditions_lst.append(1)

    if avoid is not None and avoid != "Left":
        if board[unit.coordinates[0]][unit.coordinates[1]].right:
            if board[unit.coordinates[0]][unit.coordinates[1]].right.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].right.units[0].alignment != unit.alignment:
                    conditions_lst.append(2)
    elif avoid is None:
        if board[unit.coordinates[0]][unit.coordinates[1]].right:
            if board[unit.coordinates[0]][unit.coordinates[1]].right.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].right.units[0].alignment != unit.alignment:
                    conditions_lst.append(2)

    if avoid is not None and avoid != "Right":
        if board[unit.coordinates[0]][unit.coordinates[1]].left:
            if board[unit.coordinates[0]][unit.coordinates[1]].left.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].left.units[0].alignment != unit.alignment:
                    conditions_lst.append(3)
    elif avoid is None:
        if board[unit.coordinates[0]][unit.coordinates[1]].left:
            if board[unit.coordinates[0]][unit.coordinates[1]].left.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].left.units[0].alignment != unit.alignment:
                    conditions_lst.append(3)

    if avoid is not None and avoid != "Upper left":
        if board[unit.coordinates[0]][unit.coordinates[1]].bottom_right:
            if board[unit.coordinates[0]][unit.coordinates[1]].bottom_right.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].bottom_right.units[0].alignment != unit.alignment:
                    conditions_lst.append(4)
    elif avoid is None:
        if board[unit.coordinates[0]][unit.coordinates[1]].bottom_right:
            if board[unit.coordinates[0]][unit.coordinates[1]].bottom_right.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].bottom_right.units[0].alignment != unit.alignment:
                    conditions_lst.append(4)

    if avoid is not None and avoid != "Upper right":
        if board[unit.coordinates[0]][unit.coordinates[1]].bottom_left:
            if board[unit.coordinates[0]][unit.coordinates[1]].bottom_left.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].bottom_left.units[0].alignment != unit.alignment:
                    conditions_lst.append(5)
    elif avoid is None:
        if board[unit.coordinates[0]][unit.coordinates[1]].bottom_left:
            if board[unit.coordinates[0]][unit.coordinates[1]].bottom_left.units:
                if board[unit.coordinates[0]][unit.coordinates[1]].bottom_left.units[0].alignment != unit.alignment:
                    conditions_lst.append(5)

    return conditions_lst


def give_enemy_unit(choice, unit, board):
    enemy_unit = None
    if choice == "0":
        enemy_unit = board[unit.coordinates[0]][unit.coordinates[1]].upper_right.units[0]
    if choice == "1":
        enemy_unit = board[unit.coordinates[0]][unit.coordinates[1]].upper_left.units[0]
    if choice == "2":
        enemy_unit = board[unit.coordinates[0]][unit.coordinates[1]].right.units[0]
    if choice == "3":
        enemy_unit = board[unit.coordinates[0]][unit.coordinates[1]].left.units[0]
    if choice == "4":
        enemy_unit = board[unit.coordinates[0]][unit.coordinates[1]].bottom_right.units[0]
    if choice == "5":
        enemy_unit = board[unit.coordinates[0]][unit.coordinates[1]].bottom_left.units[0]
    return enemy_unit


def battle(unit, board):
    # Rework this.

    update_board(board)
    print()

    conditions_lst = check_surrounding_units_different_alignment(unit, board)
    actions_lst = ["Upper right", "Upper left", "Right", "Left", "Bottom right", "Bottom left"]

    if len(conditions_lst) == 0:
        print("There are no enemy units nearby!")
        return

    while 0 == 0:
        print("Which region would you like this unit to attack?")
        for num in conditions_lst:
            print(str(num) + " - " + actions_lst[num])

        choice = input()

        if int(choice) not in conditions_lst:
            print("Invalid choice!")
            print()
        else:
            break

    enemy_unit = give_enemy_unit(choice, unit, board)

    enemy_conditions = check_surrounding_units_different_alignment(enemy_unit, board, actions_lst[int(choice)])

    joint_attack = None

    if not enemy_conditions:
        joint_attack = False
        print("There are no surrounding reinforces. Proceeding attack...")
    else:
        joint_attack = True
        print("There are reinforcements nearby. Joint attack? (Y/N)")

    joint_attack = input()

    if joint_attack == "Y":
        while 0 == 0:
            print("Add any many friendlies into the battle as you wish. Enter q to quit.")

            incorporated_friendlies = []
            for enemy_unit in range(len(enemy_conditions)):
                incorporated_friendlies.append(give_enemy_unit(str(enemy_unit), enemy_unit, board))

            choice_2 = input()

            if choice_2 == "q":
                break

            friendly_lst = []
            for number in range(len(incorporated_friendlies)):
                print(str(number + 1) + ". " + str(incorporated_friendlies[number]))
                friendly_lst.append(incorporated_friendlies[number])











def play_game(units_p1, units_p2, board):

    while 0 == 0:
        print()
        print("It is player 1's turn. Please select one of the following:")
        print("1. Move units" + "\n" + "2. Attack units" + "\n" + "3. End turn")

        choice = input()

        while choice == "1":
            print("Please select the unit to move:")
            print()

            for number in range(len(units_p1)):
                print("{}. ".format(number + 1) + units_p1[number].name + " with strength {} and speed {}."
                    .format(units_p1[number].strength, units_p1[number].speed) + " {}".format("[UNAVAILABLE "
                    "TO MOVE]" if units_p1[number].movement == 0 else "[{} movements remaining]"
                    .format(units_p1[number].movement)))

            unit_chosen = input()
            move_unit(units_p1[int(unit_chosen) - 1], board)
            break

        while choice == "2":
            print("Please select your attacker:")
            print()

            for number in range(len(units_p1)):
                print("{}. ".format(number + 1) + units_p1[number].name + " with strength {} and speed {} at "
                    "coordinates {}, {}.".format(units_p1[number].strength, units_p1[number].speed,
                    units_p1[number].coordinates[0] + 1, units_p1[number].coordinates[1] + 1) + " {}"
                    .format("[UNAVAILABLE TO ATTACK]" if units_p1[number].status == 0 else ""
                    .format(units_p1[number].movement)))

            unit_chosen = input()
            battle(units_p1[int(unit_chosen) - 1], board)
            break

        while choice == "3":
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

    time.sleep(0.5)

    print()
    print("Germany's invasion of Poland. September 1st, 1939.")
    print()

    time.sleep(1)

    board = [
        ["X", "X", "X", "X", "X", "+", "X", "X", "+", "+"],
        ["X", "X", "X", "X", "X", "+", "+", "+", "+", "+"],
        ["X", "X", "X", "X", "X", "+", "+", "+", "+"],
        [None, "X", "X", "X", "X", "X", "+", "+", "+"],
        [None, "X", None, "X", "X"]
    ]

    board_setup(board)
    units_p1, units_p2 = buy_units(game_type)
    place_units(units_p1, units_p2, board)

    play_game(units_p1, units_p2, board)


def main():
    print()
    print("Welcome to the game!", end="\n")
    start_game()





if __name__ == '__main__':
    main()
