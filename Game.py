import random
from random import randrange
from os import system


class Player:
    def __init__(self, name, atkstat, defstat, spdstat, hp, level, maxinv, xlocation, ylocation):
        self.name = name
        self.atkstat = atkstat
        self.defstat = defstat
        self.spdstat = spdstat
        self.hp = hp
        self.level = level
        self.maxinv = maxinv
        self.xlocation = xlocation
        self.ylocation = ylocation
        self.inventory = []
        self.rested = False
        self.placeheld = False


    def fight(self):
        enemyid = random.randrange(4)
        sec_hp = random.randrange(9)
        if enemyid == 0:
            enemytype = "Bollywog"
            potential_loot = "Bollywog Tongue"
            enemy_hp = 10 + sec_hp
        elif enemyid == 1:
            enemytype = "Goblin"
            potential_loot = "Goblin Club"
            enemy_hp = 5 + sec_hp
        elif enemyid == 2:
            enemytype = "Bear"
            enemy_hp = 15 + sec_hp
            potential_loot = "Bear Hide"
        elif enemyid == 3:
            enemytype = "Lich"
            potential_loot = "Lich Crown"
            enemy_hp = 20 + sec_hp

        dialogue(f"You have entered a fight with a {enemytype}.")
        dodge = False
        self.rested = False
        while True:
            print(" ")
            print(f"Name: {self.name}")
            print(f"HP: {self.hp}")
            print(f"Fighting: {enemytype}")
            print("What will you do?")
            userInput = input("(Attack/Dodge/Item/Run): ")
            if userInput.title() == "Attack":
                accuracy = random.randrange(4)
                if accuracy == 3:
                    dialogue("You miss.", True)
                else:
                    damage = self.atkstat - 10 + random.randrange(5)
                    dialogue(f"You hit and deal {damage} point(s) of damage to the {enemytype}.", True)
                    enemy_hp = enemy_hp - damage
                    if enemy_hp < 1:
                        dialogue(f"You beat the {enemytype}!")

                        input("Press Enter to continue...")
                        system('clear')
                        pickupchance = random.randrange(4)
                        if pickupchance == 3:
                            if len(self.inventory) < self.maxinv:
                                dialogue(f"You got a {potential_loot} from the fallen {enemytype}!")
                                self.inventory.append(potential_loot)
                                self.inventory.sort()
                                break
                            else:
                                dialgoue(f"The enemy drops {potential_loot}, but your bag was full.")
                                break
                        break
                    else:
                        print(" ")
            elif userInput.title() == "Dodge":
                dialogue("You will attempt to dodge this turn.")
                dodge = True
            elif userInput.title() == "Item":
                self.rummage()
                continue
            elif userInput.title() == "Run":
                runchance = random.randrange(3)
                if runchance == 2:
                    dialogue(f"You successfully escape the {enemytype}.")
                    break
                else:
                    dialogue("You fail to escape.")
            else:
                dialogue("This is not a valid command.")
                continue

            if dodge:
                hit = random.randrange(2)
                if hit == 1:
                    damage = random.randrange(15, 20) - self.defstat
                    self.hp = self.hp - damage
                    dialogue(f"You fail the dodge and take {damage} point(s) of damage. {self.hp} hit point(s) left.", True)
                    dodge = False
                    if self.hp < 1:
                        dialogue("You died. Game Over!")
                        input()
                        exit(0)
                    else:
                        continue
                elif hit == 0:
                    dialogue("You dodge your opponents attack.")
                    dodge = False
                    continue
            elif not dodge:
                en_acc = random.randrange(4)
                if en_acc == 3:
                    dialogue(f"The {enemytype}, misses")
                else:
                    damage = random.randrange(15, 30) - self.defstat
                    self.hp = self.hp - damage
                    dialogue(f"You get hit by the enemy and take {damage} point(s) of damage. {self.hp} hit point(s) left.")
                    if self.hp < 1:
                        dialogue("You died. Game Over!")
                        input()
                        exit(0)
                    else:
                        continue


    def move(self, direction):
        if direction == "n" or direction == "N" or direction.title() == "North":
            relx = self.xlocation - 1
            rely = self.ylocation
            if Map[relx][rely] == 1:
                dialogue("You move to the North Room.")
                self.xlocation = relx
            else:
                dialogue("There is not a room North of you.")
        elif direction == "e" or direction == "E" or direction.title() == "East":
            relx = self.xlocation
            rely = self.ylocation + 1
            if Map[relx][rely] == 1:
                dialogue("You move to the East Room.")
                self.ylocation = rely
            else:
                dialogue("There is not a room East of you.")
        elif direction == "s" or direction == "S" or direction.title() == "South":
            relx = self.xlocation + 1
            rely = self.ylocation
            if Map[relx][rely] == 1:
                dialogue("You move to the South Room.")
                self.xlocation = relx
            else:
                dialogue("There is not a room South of you.")
        elif direction == "w" or direction == "W" or direction.title() == "West":
            relx = self.xlocation
            rely = self.ylocation - 1
            if Map[relx][rely] == 1:
                dialogue("You move to the room West of you.")
                self.ylocation = rely
            else:
                dialogue("There is not a room to the West of you.")
        else:
            dialogue("That is not a valid direction.")


    def rummage(self):
        self.inventory.sort()
        count = len(self.inventory)
        loopnum = 0
        if self.inventory:
            print("You open your bag.")
            print(" ")
            while loopnum < count:
                print(f"{loopnum}: ", self.inventory[loopnum])
                loopnum = loopnum + 1
            print(" ")
            print("Would you like to use an item?")
            inpu = input("(Y/N): ")
            while True:
                if inpu.title() == "Y" or inpu.title() == "Yes":
                    while True:
                        item = input("Enter ID number for item: ")
                        try:
                            item = int(item)
                            if self.inventory[item]:
                                if self.inventory[item] == "Placeholder Crystal":
                                    self.useplaceholdercrystal()
                                    inpu = "N"
                                    break
                                elif self.inventory[item] == "Lich Crown":
                                    self.uselichcrown()
                                    inpu = "N"
                                    break
                                elif self.inventory[item] == "Bollywog Tongue":
                                    self.usetongue()
                                    inpu = "N"
                                    break
                                elif self.inventory[item] == "Bear Hide":
                                    self.usehide()
                                    inpu = "N"
                                    break
                                elif self.inventory[item] == "Goblin Club":
                                    self.usegoblinclub()
                                    inpu = "N"
                                    break
                                elif self.inventory[item] == "Banana":
                                    self.usebanana()
                                    inpu = "N"
                                    break
                                else:
                                    print("That item is not in your inventory.")
                                    break
                            else:
                                print("That is not a valid item ID.")
                        except:
                            print("Please enter an integer.")
                elif inpu.title() == "N" or inpu.title() == "No":
                    print("You close your bag.")
                    break
                else:
                    print("That is not a valid command.")
                    break
        else:
            print("Your bag is empty.")
            print(" ")


    def scout(self):
        treasure = random.randrange(3)
        print(treasure)
        if treasure == 2:
            if len(self.inventory) < self.maxinv:
                dialogue("You collect the Placeholder Crystal!")
                self.inventory.append("Placeholder Crystal")
                self.inventory.sort()
            else:
                dialogue("You don't have enough space in your inventory.")
        else:
            dialogue("You do not find any treasure here.")


    def rest(self):
        if not self.rested:
            recoverystepone = round(self.hp / 2) + 5
            self.hp = self.hp + recoverystepone
            dialogue(f"You recover {recoverystepone} hit point(s).")
            print(f"you now have {self.hp} hit point(s)")
            self.rested = True
        else:
            dialogue("You are already rested.")


    def useplaceholdercrystal(self):
        if self.placeheld:
            print(" ")
            print("Teleporting to a previous room will remove your ability to return there later.")
            print("Are you sure?")
            print(" ")
            confirm = input("(Y/N): ")
            if confirm.title() == "Y" or confirm == confirm.title() == "Yes":
                print(" ")
                print("You teleport to a held location. Your crystal breaks.")
                self.xlocation = self.savedx
                self.ylocation = self.savedy
                self.inventory.remove("Placeholder Crystal")
            elif confirm.title() == "N" or confirm == confirm.title() == "No":
                print(" ")
                print("You do not use the Placeholder Crystal.")
                eastereggchance = random.randrange(100)
                if eastereggchance == 99:
                    print("Have a cookie.")
                    self.inventory.append("Cookie")
            else:
                print(" ")
                print("...")
                print("Nevermind then...")
        else:
            print(" ")
            print("Would you like to set this room as a location you can teleport to later?")
            confirm = input("(Y/N): ")
            if confirm.title() == "Y" or confirm == "Yes":
                print(" ")
                print("You set this room as a placeheld location.")
                self.placeheld = True
                self.savedx = self.xlocation
                self.savedy = self.ylocation


    def uselichcrown(self):
        print("You use the Lich crown. You gain 5 Defense.")
        self.defstat = self.defstat + 5
        self.inventory.remove("Lich Crown")


    def usetongue(self):
        print("You eat the Bollywog Tongue. You gain 10 hp.")
        self.hp = self.hp + 5
        self.inventory.remove("Bollywog Tongue")


    def usehide(self):
        print("You wear the Bear Hide. You gain 1 attack.")
        self.atkstat = self.atkstat + 1
        self.inventory.remove("Bear Hide")


    def usegoblinclub(self):
        print("You equip the goblin club. You gain 4 attack.")
        self.atkstat = self.atkstat + 4
        self.inventory.remove("Goblin Club")


    def usebanana(self):
        print("You eat the banana. Potassium increased to dangerous levels. You feel two more bananas appear in your bag.")
        self.inventory.append("Banana")
        self.inventory.sort()


def split(dia):
    return [char for char in dia]


def dialogue(text, sleeptime=False):
    dia_list = split(text)
    char_num = len(dia_list)
    youp = 0
    system('clear')
    while youp < char_num:
        print(dia_list[youp], end='')
        youp = youp + 1
        system('sleep 0.01')
    print(" ")
    if sleeptime:
        system('sleep 1.5')


def mapgen(difficulty='easy'):
    ma = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    x = randrange(9)
    y = randrange(9)

    p1.xlocation = x
    p1.ylocation = y

    print("start room at", x, ", ", y)

    ma[x][y] = 1
    print("0:", ma[0])
    print("1:", ma[1])
    print("2:", ma[2])
    print("3:", ma[3])
    print("4:", ma[4])
    print("5:", ma[5])
    print("6:", ma[6])
    print("7:", ma[7])
    print("8:", ma[8])
    print("9:", ma[9])

    loop = 0
    if difficulty.title() == "Easy":
        t = 4
    elif difficulty.title() == "Difficult":
        t = 6
    elif difficulty.title() == "Hard":
        t = 8
    else:
        print("Bad map config. Setting difficulty to 'difficult' setting.")
        t = 6

    while loop <= t:
        print(loop)
        newdir = randrange(3)
        # generates room to the north.
        if newdir == 0:
            if x != 0:
                x = x - 1
                if ma[x][y] == 0:
                    ma[x][y] = 1
                    loop = loop + 1
                else:
                    print("Coordinate occupied. Rerouting..")
                    x = x + 1
                    continue
            elif x == 0:
                print("Room out of range. Retrying...")
        # generates room to the East
        elif newdir == 1:
            if y != 9:
                y = y + 1
                if ma[x][y] == 0:
                    ma[x][y] = 1
                    loop = loop + 1
                else:
                    print("Coordinate occupied. Rerouting...")
                    y = y - 1
                    continue
            elif y == 9:
                print("Room out of range. Retrying...")
        # generates room to the south
        elif newdir == 2:
            if x != 9:
                x = x + 1
                if ma[x][y] == 0:
                    ma[x][y] = 1
                    loop = loop + 1
                else:
                    print("Coordinate occupied. Rerouting...")
                    x = x - 1
                    continue
            elif x == 9:
                print("Room out of range. Retrying...")
        # generates room to the west
        elif newdir == 3:
            if y != 0:
                y = y - 1
                if ma[x][y] == 0:
                    ma[x][y] = 1
                    loop = loop + 1
                else:
                    print("Coordinate occupied. Rerouting...")
                    y = y + 1
                    continue
            elif y == 0:
                print("Room Out of range. Retrying...")
        else:
            break
    return ma


dialogue("What is your name?", True)
print(" ")
name = input("Enter Name: ").title()

system('sleep 2')
system('clear')
dialogue(f"And we named it... {name}.")
system('sleep 2')
system('clear')
p1 = Player(name, 15, 15, 15, 20, 1, 10, 0, 0)
p1.inventory.append("Bollywog Tongue")
p1.inventory.sort()
dialogue(f"Welcome, {name}. What kind of dungeon would you like to enter today?")
system('sleep 1')
userInput = input("(Easy, Difficult, or Hard): ")

Map = mapgen(userInput)
system('clear')
dialogue(f"You have chosen {userInput}. Let us... begin.")
print(" ")
print("Press Enter to continue...")
input()
system('clear')
dialogue("Tip: You can type 'help' to see a list of possible commands.")
print(" ")
while True:
    userInput = input("What would you like to do?: ")
    if userInput.title() == "Rummage":
        p1.rummage()
        print(" ")
        input("Press Enter to continue...")
        system('clear')
    elif userInput.title() == "Rest":
        p1.rest()
    elif userInput.title() == "Move":
        userInput = input("Which direction would you like to move? (N/S/E/W): ")
        p1.move(userInput)
        print(" ")
        input("Press Enter to continue...")
        system('clear')
        encounter_rate = random.randrange(3)
        if encounter_rate == 2:
            p1.fight()
    elif userInput.title() == "Scout":
        p1.scout()
        print(" ")
        input("Press Enter to continue...")
        system('clear')
    elif userInput.title() == "Map":
        print("0:", Map[0])
        print("1:", Map[1])
        print("2:", Map[2])
        print("3:", Map[3])
        print("4:", Map[4])
        print("5:", Map[5])
        print("6:", Map[6])
        print("7:", Map[7])
        print("8:", Map[8])
        print("9:", Map[9])
        print("--------------------------------")
        print("    0  1  2  3  4  5  6  7  8  9")
        print(f"You are located at {p1.ylocation}, {p1.xlocation}")
        input("Press Enter to continue...")
        system('clear')
    elif userInput.title() == "Banana":
        print(" ")
        print("You got the Banana.")
        p1.inventory.append("Banana")
    elif userInput.title() == "Help":
        jokechance = random.randrange(1, 100)
        system('clear')
        print(" ")
        print("The following are commands you can use at any time:")
        print("----------------------------------------------------------------------------------------------")
        print("Rummage: This command displays your inventory.")
        print("Rest: This command will have your character sleep, regaining a random amount of hit points.")
        print("Map: This command displays a map of the dungeon, and your current location.")
        print("Scout: This command makes you look for treasure.")
        print("Move: This command allows you to move to an adjacent room.")
        print("Quit: This command exits the game.")
        if jokechance > 95:
            print("Banana: Potassium.")
        print("----------------------------------------------------------------------------------------------")
        print("")
    elif userInput.title() == "Quit":
        userInput = input("Are you sure you want to quit? (y/n): ")
        if userInput.title() == "Yes" or userInput.title() == "Y":
            exit(0)
        elif userInput.title() == "No" or userInput.title() == "N":
            dialogue("Then the world shall not perish.")
        else:
            dialogue("That is not a valid command, so continue playing.... Please.")
    else:
        dialogue("That is not a valid command.")
        input("Press Enter to continue...")
