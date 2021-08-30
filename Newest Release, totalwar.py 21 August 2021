import random
import time
from tkinter import *
from tkinter import messagebox


STARTING_POINT = 40


class Shop:
    def __init__(self):

        self.inf_lst = [
            Unit("inf_1", 3, 3, 2),
            Unit("inf_2", 3, 3, 2),
            Unit("inf_3", 3, 3, 2),
            Unit("inf_4", 3, 3, 2),
            Unit("inf_5", 1, 3, 1),
            Unit("inf_6", 1, 3, 1)
        ]

        self.tank_lst = [
            Unit("tank_1", 4, 6, 2),
            Unit("tank_2", 4, 6, 2),
            Unit("tank_3", 4, 6, 2),
            Unit("tank_4", 4, 6, 2),
            Unit("tank_5", 2, 5, 1),
            Unit("tank_6", 2, 5, 1)
        ]

        self.air_lst = [
            Unit("intercept_1", 5, 4, 1),
            Unit("intercept_2", 5, 4, 1),
            Unit("bomber_1", 4, 6, 1),
            Unit("bomber_2", 4, 6, 1)
        ]

        self.garrison_lst = [
            Unit("garrison_1", 1, 0, 1),
            Unit("garrison_2", 1, 0, 1),
            Unit("garrison_3", 1, 0, 1),
            Unit("garrison_4", 1, 0, 1)
        ]

        self.temp_lst = []


class Player:
    def __init__(self):
        self.money = 100
        self.units = []


class Area:

    def __init__(self, alignment, name=None, button=None):
        self.alignment = alignment
        self.name = name
        self.capacity = 3
        self.coordinates = []
        self.units = []
        self.button = button
        self.x = None
        self.y = None

        self.upper_right = None
        self.upper_left = None
        self.right = None
        self.left = None
        self.bottom_right = None
        self.bottom_left = None

    def add_unit(self, unit):
        self.units.append(unit)
        if self.capacity - unit.size < 0:
            return False
        else:
            self.capacity -= unit.size
            return True

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

        self.activity = False

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
            introduction_str += ", with reinforcement from {}".format \
                (str([friendly_unit for friendly_unit in others_friendly]))
        introduction_str += " attacks " + "{}".format(enemy.name.upper())
        if others_hostile is not None:
            introduction_str += ", with enemy support from {}".format \
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
                print("\nThere are enemy units in this region. Attack first!")
                return
            if unit_area.upper_right is None:
                print("Out of bounds! \n")
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
                print("\nThere are enemy units in this region. Attack first!")
                return
            if unit_area.upper_left is None:
                print("Out of bounds! \n")
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
                print("\nThere are enemy units in this region. Attack first!")
                return
            if unit_area.right is None:
                print("Out of bounds! \n")
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
                print("\nThere are enemy units in this region. Attack first!")
                return
            if unit_area.left is None:
                print("Out of bounds! \n")
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
                print("\nThere are enemy units in this region. Attack first!")
                return
            if unit_area.bottom_right is None:
                print("Out of bounds! \n")
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
                print("\nThere are enemy units in this region. Attack first!")
                return
            if unit_area.bottom_left is None:
                print("Out of bounds! \n")
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
        print("Unit {} moved to coordinates {}. \n"
              .format(self.name, [self.coordinates[0] + 1, self.coordinates[1] + 1]))

    def retreat(self, board):
        pass

    def destroyed(self, board):
        board[self.coordinates[0]][self.coordinates[1]].units.remove(self)
        board[self.coordinates[0]][self.coordinates[1]].capacity += self.size

    def __repr__(self):
        return self.name


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
        print("\nWhere would you like to move {}? \n".format(unit.name))

        while True:
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

    while True:
        print("Which region would you like this unit to attack?")
        for num in conditions_lst:
            print(str(num) + " - " + actions_lst[num])

        choice = input()

        if int(choice) not in conditions_lst:
            print("Invalid choice! \n")
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
        while True:
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
    while True:
        print("\nIt is player 1's turn. Please select one of the following:")
        print("1. Move units" + "\n" + "2. Attack units" + "\n" + "3. End turn")

        choice = input()

        while choice == "1":
            print("Please select the unit to move: \n")

            for number in range(len(units_p1)):
                print("{}. ".format(number + 1) + units_p1[number].name + " with strength {} and speed {}."
                      .format(units_p1[number].strength, units_p1[number].speed) + " {}".format("[UNAVAILABLE "
                    "TO MOVE]" if units_p1[number].movement == 0 else "[{} movements remaining]".format(
                    units_p1[number].movement)))

            unit_chosen = input()
            move_unit(units_p1[int(unit_chosen) - 1], board)
            break

        while choice == "2":
            print("Please select your attacker: \n")

            for number in range(len(units_p1)):
                print("{}. ".format(number + 1) + units_p1[number].name + " with strength {} and speed {} at "
                                                                          "coordinates {}, {}.".format(
                    units_p1[number].strength, units_p1[number].speed,
                    units_p1[number].coordinates[0] + 1, units_p1[number].coordinates[1] + 1) + " {}"
                      .format("[UNAVAILABLE TO ATTACK]" if units_p1[number].status == 0 else ""
                              .format(units_p1[number].movement)))

            unit_chosen = input()
            battle(units_p1[int(unit_chosen) - 1], board)
            break

        while choice == "3":
            pass


def place_unit_on_board(board, unit, frame, window):

    def find_coords():
        abs_coord_x = window.winfo_pointerx() - window.winfo_rootx()
        abs_coord_y = window.winfo_pointery() - window.winfo_rooty()

        x_counter = 0
        for row in board:
            if x_counter % 2 == 0:
                addition = 27
            else:
                addition = 0
            for column in row:
                if column is not None:
                    if column.x <= abs_coord_x <= column.x + 55:
                        if column.y <= abs_coord_y <= column.y + 55:
                            x_coord = (abs_coord_x - addition - STARTING_POINT) // 55
                            y_coord = (abs_coord_y - 50) // 55
                            if unit.alignment == board[y_coord][x_coord].alignment:
                                condition = board[y_coord][x_coord].add_unit(unit)
                                if condition:
                                    unit.activity = True
                                    break
                                else:
                                    messagebox.showinfo("Illegal placement!", "Not enough space!")
                                    break
                            else:
                                messagebox.showinfo("Illegal placement!", "That's enemy territory!")
                                break
            x_counter += 1

    # To print the map in GUI form.
    x_counter = 0
    x_coord = STARTING_POINT
    y_coord = 50
    for row in board:
        if x_counter % 2 == 0:
            x_coord += 27
        for column in row:
            if column is not None:
                if column.alignment == "Germany":
                    button = Button(frame, width=6, height=3, bg="Dark Red", bd=3, command=find_coords)
                    button.place(x=x_coord, y=y_coord)
                    column.button = button
                    column.x = x_coord
                    column.y = y_coord
                elif column.alignment == "Poland":
                    button = Button(frame, width=6, height=3, bg="Green", bd=3, command=find_coords)
                    button.place(x=x_coord, y=y_coord)
                    column.button = button
                    column.x = x_coord
                    column.y = y_coord
            x_coord += 55
        x_coord = STARTING_POINT
        y_coord += 55
        x_counter += 1

    return frame, window, board, unit


def place_units(units_p1, units_p2, board, window):
    board_frame, window, board = board_setup(board, window)

    options = Listbox(board_frame, selectmode=SINGLE, width=45, height=3)
    options.place(x=350, y=280)
    for l in range(len(units_p1)):
        options.insert(l, units_p1[l])

    temp = []

    def end():
        pass

    Button(board_frame, command=end, text="Continue", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=12, height=1, bd=5, activeforeground="black").place(x=550, y=230)

    for i in range(len(units_p1)):

        def place(event):
            unit = units_p1[event.widget.curselection()[0]]
            frame, new_window, new_board, unit = place_unit_on_board(board, unit, board_frame, window)

            if unit.activity:
                temp.append(units_p1.pop(event.widget.curselection()[0]))
                options.delete(event.widget.curselection()[0])

        options.bind("<<ListboxSelect>>", place)

    window.mainloop()

    pass

    placed_p1 = []
    placed_p2 = []

    while unit != "START":
        print("\nPlayer 1, please choose your unit (by number), and then the coordinates (row and then "
              "column, one by one), where you would like your units to be. \n Enter START to start the battle. \n")

        for number in range(len(units_p1)):
            print("{}. ".format(number + 1) + units_p1[number].name + " with strength {} and speed {}"
                  .format(units_p1[number].strength, units_p1[number].speed) + ". {}"
                  .format("[PLACED]" if units_p1[number].coordinates is not None else ""))

        while True:
            unit = input()
            if unit == "START" and len(units_p1) != len(placed_p1):
                print("\nPlease finish placing all of your units!")
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

        while True:
            row = input()
            if 0 < int(row) <= len(board):
                print("Row {} chosen.".format(row))
                break
            else:
                print("Please enter a valid row.")

        while True:
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

                print("{} is placed on coordinates {}, {}. \n".format(units_p1[int(unit) - 1].name,
                        units_p1[int(unit) - 1].coordinates[0] + 1, units_p1[int(unit) - 1].coordinates[1] + 1))

                update_board(board)

            else:
                print("\nThis area does not have enough capacity for this additional unit!")
        else:
            print("\nYou cannot place units on enemy territory!")

    unit = None
    if units_p2 is not None:
        update_board(board)
        while unit != "START":
            print("\nPlayer 2, please choose your unit (by number), and then the coordinates (row and then "
                  "column, one by one), where you would like your units to be. \n Enter START to start the battle. \n")

            for number in range(len(units_p2)):
                print("{}. ".format(number + 1) + units_p2[number].name + " with strength {} and speed {}"
                      .format(units_p2[number].strength, units_p2[number].speed) + ". {}"
                      .format("[PLACED]" if units_p2[number].coordinates is not None else ""))

            while True:
                unit = input()
                if unit == "START" and len(units_p2) != len(placed_p2):
                    print("\nPlease finish placing all of your units!")
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

            while True:
                row = input()
                if 0 < int(row) <= len(board):
                    print("Row {} chosen.".format(row))
                    break
                else:
                    print("Please enter a valid row.")

            while True:
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

                    print("{} is placed on coordinates {}, {}. \n".format(units_p2[int(unit) - 1].name,
                        units_p2[int(unit) - 1].coordinates[0], units_p2[int(unit) - 1].coordinates[1]))

                    update_board(board)

                else:
                    print("\nThis area does not have enough capacity for this additional unit!")
            else:
                print("\nYou cannot place units on enemy territory!")
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
                row = random.randint(0, len(board) - 1)
                column = random.randint(0, len(board[row]) - 1)
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


def buy_units(game_type, window, shop, special_instructions=None):
    p1 = Player()

    def purchase_specific_unit(unit_list, player_currency, unit_type, player_number, unit_index, purchased_units):

        player_alignment = [0, "Germany", "Poland"]
        multipliers = [4, 6, 6, 3]

        choices = [str(number + 1) for number in range(len(unit_list))]

        if str(unit_index) in choices:
            if player_currency - unit_list[int(unit_index) - 1].strength * multipliers[unit_type] >= 0:
                purchased_units.append(unit_list.pop(int(unit_index) - 1))
                player_currency -= (purchased_units[-1].strength * multipliers[unit_type])
                purchased_units[-1].alignment = player_alignment[player_number]
            else:
                messagebox.showinfo("Spend your money wisely!", "Insufficient funds.")

        return player_currency, purchased_units, unit_list


    def list_available_units(unit_choice, unit_list):
        multipliers = [4, 6, 6, 3]
        type_unit = ["Infantry", "Tank", "Aircraft", "Garrison"]

        # Individual unit shop header.
        frame = Frame(window, width=680, height=360, bg="Dark Green")
        frame.place(x=0, y=0)
        Label(frame, text=type_unit[unit_choice] + " Shop", font=("Arial", 13, "bold"), fg="black", bd=7, relief=SOLID,
              padx=2.5, pady=2.5, anchor="n", justify=CENTER, width=66, height=1).place(x=0, y=0)

        x_coord = 30
        y_coord = 50

        # Individual unit shop unit list.
        options = Listbox(frame, selectmode=SINGLE, width=45, height=17)
        options.place(x=x_coord, y=y_coord)

        # Individual unit shop list of units.
        for number in range(len(unit_list)):
            text = "{}. ".format(number + 1) + unit_list[number].name + " with strength {} and speed {} for ${}."\
                .format(unit_list[number].strength, unit_list[number].speed,
                        unit_list[number].strength * multipliers[unit_choice])

            options.insert(number, text)

            y_coord += 30

        # Returns the particular unit selected.
        def get_unit():
            try:
                selected_index = options.curselection()[0] + 1
                global temp_list
                p1.money, p1.units, shop.temp_lst = purchase_specific_unit(unit_list, p1.money, unit_choice, 1,
                                                                           selected_index, p1.units)
                Label(new_frame, text="CURRENT BALANCE: {}".format(p1.money), font=("Arial", 14, "bold"), fg="black",
                      relief=SOLID, width=20, height=3, bd=4, padx=10, activeforeground="black").place(x=370, y=50)
                frame.destroy()

                p1_units = Listbox(new_frame, height=7, width=30)
                p1_units.place(x=340, y=220)
                for j in range(len(p1.units)):
                    p1_units.insert(j, p1.units[j])

            except IndexError:
                return

        # Gui for individual shop, including CURRENCY:, instructions, buy button.
        Button(frame, text="Buy", anchor="nw", relief=SOLID, padx=10, pady=10, justify=LEFT,
               font=("Arial", 10, "bold"), command=get_unit).place(x=170, y=235)

        Label(frame, text="CURRENT BALANCE: {}".format(p1.money), font=("Arial", 14, "bold"), fg="black",
              relief=SOLID, width=20, height=3, bd=4, padx=10, activeforeground="black").place(x=370, y=50)

        text = "To purchase the unit, please select the unit \nand click 'buy'."

        Label(frame, text=text, anchor="nw", relief=SOLID, padx=10, pady=10, justify=LEFT,
              font=("Arial", 10, "bold")).place(x=340, y=135)

        def back():
            frame.destroy()
            return

        Button(frame, command=back, text="Back", font=("Arial", 10, "bold"),
               fg="black", relief=RAISED, width=12, height=1, bd=5, activeforeground="black").place(x=550, y=300)

    def buy_inf():

        list_available_units(0, shop.inf_lst)
        shop.temp_lst = shop.inf_lst
        return

    def buy_tank():

        list_available_units(1, shop.tank_lst)
        shop.temp_lst = shop.tank_lst
        return

    def buy_air():

        list_available_units(2, shop.air_lst)
        shop.temp_lst = shop.air_lst
        return

    def buy_gar():

        list_available_units(3, shop.garrison_lst)
        shop.temp_lst = shop.garrison_lst
        return

    def end():
        if not p1.units:
            messagebox.showinfo("Buy units to strengthen your army!", "Please purchase some units.")
        else:
            new_frame.destroy()
        return

    # For collective shop GUI.
    new_frame = Frame(window, width=680, height=360, bg="Dark Green")
    new_frame.place(x=0, y=0)

    Label(new_frame, text="Global Arms Market", font=("Arial", 13, "bold"), fg="black", bd=7, relief=SOLID, padx=2.5,
          pady=2.5, anchor="n", justify=CENTER, width=66, height=1).place(x=0, y=0)

    Button(new_frame, command=buy_inf, text="INFANTRY", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=15, height=7, bd=10, activeforeground="black").place(x=20, y=50)

    Button(new_frame, command=buy_tank, text="TANK", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=15, height=7, bd=10, activeforeground="black").place(x=20, y=200)

    Button(new_frame, command=buy_air, text="AIR", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=15, height=7, bd=10, activeforeground="black").place(x=175, y=50)

    Button(new_frame, command=buy_gar, text="GARRISON", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=15, height=7, bd=10, activeforeground="black").place(x=175, y=200)

    if game_type == "single":
        text = "Since you're playing on single player mode, \nonly you will have to purchase units. Press \ncontinue" \
               " when you are done."

    elif game_type == "multi":
        if special_instructions is None:
            text = "Since you're playing on multiplayer mode, \nyou, player 1, will purchase units, and after, " \
                   "\nplayer 2 will likewise."
        else:
            text = "Player 2 should purchase his units now."

    Label(new_frame, text="CURRENT BALANCE: {}".format(p1.money), font=("Arial", 14, "bold"),
          fg="black", relief=SOLID, width=20, height=3, bd=4, padx=10, activeforeground="black").place(x=370, y=50)

    Label(new_frame, text=text, anchor="nw", relief=SOLID, padx=10, pady=10, justify=LEFT, font=("Arial", 10, "bold"))\
        .place(x=340, y=135)

    p1_units = Listbox(new_frame, height=7, width=30)
    p1_units.place(x=340, y=220)
    for i in range(len(p1.units)):
        p1_units.insert(i, p1.units[i])

    text = "Your current \narmy:"
    Label(new_frame, text=text, anchor="nw", relief=SOLID, padx=10, pady=10, justify=CENTER,
          font=("Arial", 10, "bold")).place(x=545, y=225)

    Button(new_frame, command=end, text="Continue", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=12, height=1, bd=5, activeforeground="black").place(x=550, y=300)

    return p1.units


def board_setup(board, window):

    board_frame = Frame(window, width=680, height=360, bg="Dark Green")
    board_frame.place(x=0, y=0)

    text = "Germany's invasion of Poland. September 1st, 1939."

    Label(board_frame, text=text, font=("Arial", 13, "bold"), fg="black", bd=7, relief=SOLID, padx=2.5, pady=2.5,
          anchor="n", justify=CENTER, width=66, height=1).place(x=0, y=0)

    # To set up object properties.
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] is not None:
                if board[row][column] == "X":
                    board[row][column] = Area("Germany")
                elif board[row][column] == "O":
                    board[row][column] = Area("Poland")
                board[row][column].coordinates = [row, column]

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] is not None:
                board[row][column].set_boundaries(board)

    # To print the map in GUI form.
    x_counter = 0
    x_coord = STARTING_POINT
    y_coord = 50
    for row in board:
        if x_counter % 2 == 0:
            x_coord += 27
        for column in row:
            if column is not None:
                if column.alignment == "Germany":
                    button = Button(board_frame, width=6, height=3, bg="Dark Red", bd=3)
                    button.place(x=x_coord, y=y_coord)
                    column.button = button
                    column.x = x_coord
                    column.y = y_coord
                elif column.alignment == "Poland":
                    button = Button(board_frame, width=6, height=3, bg="Green", bd=3)
                    button.place(x=x_coord, y=y_coord)
                    column.button = button
                    column.x = x_coord
                    column.y = y_coord
            x_coord += 55
        x_coord = STARTING_POINT
        y_coord += 55
        x_counter += 1

    return board_frame, window, board


def start_game(game_type, window, main_frame):
    p1 = Player()
    p2 = Player()
    shop = Shop()

    board = [
        ["X", "X", "X", "X", "X", "O", "X", "X", "O", "O"],
        ["X", "X", "X", "X", "X", "O", "O", "O", "O", "O"],
        ["X", "X", "X", "X", "X", "O", "O", "O", "O"],
        [None, "X", "X", "X", "X", "X", "O", "O", "O"],
        [None, "X", None, "X", "X"]
    ]

    main_frame.destroy()

    #################### Placement portion of the game. ####################
    board_frame, window, board = board_setup(board, window)

    text = "Player 1 will now set up the board--click the unit \nand the region you want it to occupy."

    Label(board_frame, text=text, anchor="nw", bd=3, justify=LEFT, font=("Arial", 10, "bold")).place(x=350, y=285)

    def go_place():

        place_units(p1.units, p2.units, board, window)

    Button(board_frame, command=go_place, text="Continue", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=12, height=1, bd=5, activeforeground="black").place(x=550, y=230)
    #################### Placement portion of the game. ####################

    #################### Shop portion of the game. ####################
    board_frame, window, board = board_setup(board, window)

    text = "You will be playing on this map. To start \nthe game, you need to purchase units..."

    Label(board_frame, text=text, anchor="nw", bd=3, justify=LEFT, font=("Arial", 10, "bold")).place(x=350, y=285)

    def go_shop():
        if game_type == "multi":
            unit_list = buy_units(game_type, window, shop, p2)
            p2.units = unit_list
        board_frame.destroy()
        unit_list = buy_units(game_type, window, shop)
        p1.units = unit_list

    Button(board_frame, command=go_shop, text="Continue", font=("Arial", 10, "bold"),
           fg="black", relief=RAISED, width=12, height=1, bd=5, activeforeground="black").place(x=550, y=230)
    #################### Shop portion of the game. ####################


    window.mainloop()


    play_game(units_p1, units_p2, board)



def options_gui():

    def single_player_command():
        global game_type
        game_type = "single"
        main_frame.destroy()
        start_game(game_type, window, main_frame)

    def multiplayer_command():
        global game_type
        game_type = "multi"
        main_frame.destroy()
        start_game(game_type, window, main_frame)

    def about():

        def go_back():
            frame.destroy()

        frame = Frame(window, width=680, height=360)
        frame.place(x=0, y=0)

        Label(frame, text="", image=background_image, fg="black").place(x=-5, y=0)

        text = """                                       
             
Total War is a miniature war simulation game consisting of (currently, a 
maximum of) 2 players, capable of buying, placing, and moving units to 
either capture their opponent's capital or destroy all enemy forces. 


A side project made by NYU student Leo Liu.
"""

        Label(frame, text=text, font=("Arial", 13, "bold"), fg="black", bd=5, relief=SOLID, padx=2.5, pady=2.5,
              anchor="n", justify=LEFT, width=60, height=10).place(x=35, y=50)

        Button(frame, command=go_back, text="Back", font=("Arial", 15, "bold"), width=15, height=1,
               fg="black", relief=RAISED, bd=5, activeforeground="black").place(x=470, y=300)

    window = Tk()
    window.geometry('680x360')
    window.title("Total War")
    window.resizable(False, False)

    main_frame = Frame(window, width=680, height=360)
    main_frame.place(x=0, y=0)

    background_image = PhotoImage(file="army.png")
    Label(main_frame, text="", image=background_image, fg="black").place(x=-5, y=0)
    Label(main_frame, text="Total War", font=("Arial", 30, "bold"), fg="black", bd=5, relief=SOLID, width=10, height=1,
          padx=5, pady=5).place(x=90, y=60)

    Button(main_frame, command=single_player_command, text="Single Player", font=("Arial", 15, "bold"),
           fg="black", relief=RAISED, width=15, height=1, bd=5, activeforeground="black").place(x=420, y=40)

    Button(main_frame, command=multiplayer_command, text="Multiplayer", font=("Arial", 15, "bold"), width=15,
           height=1, fg="black", relief=RAISED, bd=5, activeforeground="black").place(x=420, y=100)

    Button(main_frame, command=about, text="About", font=("Arial", 15, "bold"), width=15, height=1,
           fg="black", relief=RAISED, bd=5, activeforeground="black").place(x=420, y=160)

    window.mainloop()


def main():
    options_gui()




if __name__ == '__main__':
    main()
