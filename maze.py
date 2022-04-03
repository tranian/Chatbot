import random
import sys
import time

# e indicates the room's exit
# c indicates the puzzle in the room
# d indicates doors
room = [
    'xxxxx         xxxxxxxxxxxxx',
    'x...xxxxxxxxxxx...........x',
    'x...d.........d...........x',
    'xc..xxxxxxxxxxxc..........x',
    'xxdxx         xxxxxxxxxxxxx',
    ' x.x',
    'xxdxx',
    'xc..x',
    'x...x',
    'x..ex',
    'xxxxx',
]


computer_on = False
computer_unlocked = False
door_unlocked = False
computer_help = """
commands:
    help		shows all available commands
    map			show map
    exit		exit terminal
    unlock		unlock door
    lock		lock door
    logout		log off system
    reboot		initiates system reboot
"""
map_key = """
@ --> YOU
x --> WALL
d --> DOOR
e --> EXIT
"""
player_name = ''

help_menu = """
HELP COMMAND:
--------------------------
down  = move down
up    = move up
left  = move left
right = move right
help  = prints this help
--------------------------
"""

banner = """
########################################################################################
########################################################################################
##   ________  __    __  ________        __       __   ______   ________  ________    ##
##  |        \|  \  |  \|        \      |  \     /  \ /      \ |        \|        \   ##
##   \$$$$$$$$| $$  | $$| $$$$$$$$      | $$\   /  $$|  $$$$$$\ \$$$$$$$$| $$$$$$$$   ##
##     | $$   | $$__| $$| $$__          | $$$\ /  $$$| $$__| $$    /  $$ | $$__       ##
##     | $$   | $$    $$| $$  \         | $$$$\  $$$$| $$    $$   /  $$  | $$  \      ##
##     | $$   | $$$$$$$$| $$$$$         | $$\$$ $$ $$| $$$$$$$$  /  $$   | $$$$$      ##
##     | $$   | $$  | $$| $$_____       | $$ \$$$| $$| $$  | $$ /  $$___ | $$_____    ##
##     | $$   | $$  | $$| $$     \      | $$  \$ | $$| $$  | $$|  $$    \| $$     \   ##
##      \$$    \$$   \$$ \$$$$$$$$       \$$      \$$ \$$   \$$ \$$$$$$$$ \$$$$$$$$   ##
##                                                                                    ##
##                          You can't exit unless you beat it!                        ##
##                                                                                    ##
##                  (C) Copyright ChatBot. 2022.  All rights reserved                 ##
##                                                                                    ##
########################################################################################
########################################################################################
"""


def intro(name=None):
    """
    Intro to the game.

    Args:
        name (str): name of user.  Prompts if none.
    """
    time.sleep(1)
    print("Loading", end='')
    for i in range(5):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(.8)
    print("Done.")
    time.sleep(.7)
    print(banner)
    global player_name
    if name is None:
        name = input('What is your name? ')
    player_name = name
    print("You awaken in what seems to be a dark and abandoned facility.  "
          "Near you is a computer and a door.  There must be something on the computer to "
          "help me get out of here.")
    print(help_menu)


def computer_message(msg, sleep=0):
    """
    Prints a computer message with a time delay

    Args:
        msg (str): takes in a message to print
        sleep (int): takes in time for message delay (defaults to 0)
    """
    print(msg)
    time.sleep(sleep)


def computer_intro():
    """
    Startup intro for computer
    """
    time.sleep(1.3)
    computer_message('Initializing Filesystem...', .2)
    computer_message('Checking Root System...', .1)
    computer_message('Performing Memory Check...', .1)
    computer_message('Memory Check Finished.', .2)
    computer_message("Mounting Drive...", .2)
    computer_message("Setting up network", .2)
    computer_message("Current Hostname is 0.0.0.0", .2)
    computer_message('Attempting connection with server 64.245.365.42', 1)
    computer_message('Connection Refused.')
    computer_message('System Check Ok\nBooting in safe mode...', .1)
    computer_message('--------------------------------------------------')
    computer_message('All Rights Reserved PyOs 2.52v2 #4345')


def login_check():
    """
    checks if computer is logged in
    """
    global computer_unlocked
    computer_message('Starting AuthLoginD.v1.4...', .2)
    computer_message('Checking User Authentication...')
    if (not computer_unlocked):
        computer_message('ERROR: UNAUTHORIZED USER', .5)
    else:
        computer_message('Success', .4)
        computer_message('Logging in as root...', .5)


def check_computer_on():
    """
    checks if the computer is on, otherwise play startup intro
    """
    global computer_on
    if not(computer_on):
        computer_on = True
        computer_intro()


def run_puzzle(row, col):
    """
    Runs a password minigame for the player, also checks for terminal login
    Args:
        current_row (int): takes current 2d array x position of player for map function
        current_col (int): takes current 2d array y position of player for map function
    """
    global computer_unlocked, computer_stay
    check_computer_on()
    if not (computer_unlocked):
        computer_stay = True
        login_check()
        while(computer_stay):
            check_computer_on()
            passwords = ["password", "admin", "rockyou", "log34me34", "bizbaz45"]
            random_password = random.choice(passwords)
            computer_message('Fetching Password List...', .2)
            computer_message('-----------------------------------')
            for stuff in passwords:
                if (stuff == random_password):
                    print(stuff.upper())
                else:
                    print(stuff)
            computer_message('-----------------------------------')
            computer_message('Generating valid one-time password...', .5)
            input_password = input("Please enter valid passphrase from list:\n# ")
            if (input_password == random_password):
                computer_message("Password Correct")
                computer_unlocked = True
                computer_message('Restarting AuthLoginD.v.1.4', .3)
                terminal(row, col)
            elif (input_password == 'exit'):
                computer_message('Exiting...', .2)
                computer_stay = False
            else:
                computer_message("Incorrect Password")
    else:
        terminal(row, col)


def terminal(row, col):
    """
    A simple "terminal shell" for the user to interact with
    Args:
        row (int): takes current 2d array x position of player
        col (int): takes current 2d array y position of player
    """
    global door_unlocked, computer_unlocked, computer_on, computer_stay
    login_check()
    exit = False
    while (not exit):
        terminal_input = input("root~# ")
        if (terminal_input == "help"):
            print(computer_help)
        elif (terminal_input == "map"):
            computer_message('Starting vmap2.3 process...', .5)
            computer_message('SUCCESS')
            room_map(row, col)
        elif terminal_input == "exit":
            computer_message('Exiting...', .3)
            exit = True
            computer_stay = False
        elif terminal_input == "unlock":
            computer_message('Unlocking door...', .3)
            door_unlocked = True
            computer_message('Door unlocked...', .2)
        elif terminal_input == "lock":
            computer_message('Locking door...', .3)
            door_unlocked = False
            computer_message('Door locked.', .2)
        elif terminal_input == 'logout':
            computer_message('Exiting shell...', .5)
            computer_message('Logging out of user \'root\'', .3)
            computer_unlocked = False
            login_check()
            exit = True
        elif terminal_input == 'reboot':
            computer_message('Rebooting System....', .5)
            computer_on = False
            exit = True
        else:
            computer_message('Error:  Unknown command.\nType \'help\' for commands')


def check(obj, current_row, current_col):
    """
    checks for any objects near the player and announces it
    Args:
        obj (char): takes in object near player
        current_row (int): takes current 2d array x position of player
        current_col (int): takes current 2d array y position of player
    """
    if obj == 'c':
        obj_type = 'computer'
    elif obj == 'd':
        obj_type = 'door'
    elif obj == 'x':
        obj_type = 'wall'
    if room[current_row - 1][current_col] == obj:
        print(f'There is a {obj_type} up')
    if room[current_row + 1][current_col] == obj:
        print(f'There is a {obj_type} down')
    if room[current_row][current_col - 1] == obj:
        print(f'There is a {obj_type} left')
    if room[current_row][current_col + 1] == obj:
        print(f'There is a {obj_type} right')


def move(current_row, current_col, direction):
    """
    move the player, also checks for collision with objects
    Args:
        current_row (int): takes current 2d array x position of player
        current_col (int): takes current 2d array y position of player
        direction (str): takes in direction command from player
    Returns:
        tuple: current position of the player
    """
    new_row = current_row
    new_col = current_col
    if direction == 'up':
        new_row -= 1
    elif direction == 'down':
        new_row += 1
    elif direction == 'left':
        new_col -= 1
    elif direction == 'right':
        new_col += 1
    elif direction == 'help':
        print(help_menu)
    else:
        print(f'Invalid command {direction}. Valid command: up, down, left, right, help')

    if room[new_row][new_col] == 'x':  # Hit a wall!
        print('A wall obstructs you')
        return (current_row, current_col)
    elif room[new_row][new_col] == 'd':
        if (not door_unlocked):
            print('A locked door.  There might be a computer nearby to unlock it.')
            return (current_row, current_col)
        else:
            print('Entering unlocked door.')
            return (new_row, new_col)

    elif room[new_row][new_col] == 'c':
        run_puzzle(new_row, new_col)
    return new_row, new_col


def room_map(row, col):
    """
    prints the map of the game
    Args:
        row (int): takes current 2d array x position of player
        col (int): takes current 2d array y position of player
    """
    global room
    print('----------------------------------------------------')
    for x, map_row in enumerate(room):
        for y, map_col in enumerate(list(map_row)):		# typecasting into list splits string into char
            orig_val = room[x][y]
            if (x == row and y == col):
                print('@', end='')
            else:
                print(orig_val, end='')
        time.sleep(.1)
        print()
    computer_message('----------------------------------------------------', .5)
    computer_message('KEY:', .3)
    computer_message(map_key, .3)


def maze(name=None):
    """
    main function of the game
    """
    player_row = 2
    player_col = 1
    intro(name)
    while (room[player_row][player_col] != 'e'):
        # room_map(player_row, player_col)
        # check_door(player_row, player_col)
        check('c', player_row, player_col)
        check('d', player_row, player_col)
        check('x', player_row, player_col)
        direction = input('Enter location:\n> ')

        player_row, player_col = move(player_row, player_col, direction)

    print(f"You escaped, {player_name}.")


if __name__ == "__main__":
    maze()
