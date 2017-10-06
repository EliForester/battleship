

import time

# real ships
SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

# test ships
#SHIP_INFO = [
#    ("Submarine", 3),
#    ("Cruiser", 3),
#    ("Patrol Boat", 2)
#]

BOARD_SIZE = 10

VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
EMPTY = 'O'
MISS = '.'
HIT = '*'
SUNK = '#'



class Player(object):

    def __init__(self, player_number):
        self.number = player_number
        self.ship_board = make_empty_board(BOARD_SIZE)
        self.guess_board = make_empty_board(BOARD_SIZE)
        self.ship_locations = []
        self.sunk_ships = []
        self.name = ''



def print_board_heading():
    print("   " + " ".join([chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]))


def print_board(board):
    print_board_heading()

    row_num = 1
    for row in board:
        print(str(row_num).rjust(2) + " " + (" ".join(row)))
        row_num += 1


def clear_screen():
    print("\033c", end="")


def make_empty_board(board_size):
    board = []
    for i in range(0,board_size):
        board_row = []
        for i in range(0,board_size):
            board_row.append(EMPTY)
        board.append(board_row)
    return board


def ship_placement(current_ship, current_player):
    # Board setting - placing the ships, validating input and board location
    ship_placed = 'No'

    clear_screen()

    while ship_placed == 'No':

        print('Your board {}:\n'.format(players[current_player].name))
        print_board(players[current_player].ship_board)
        print('Place your ship. {} occupies {} spaces.'.format(ship[0], ship[1]))

        orientation = ''
        while orientation == '':
            orientation = input('Horizontal or Vertical? (H, V): ')
            orientation = orientation.replace(' ', '')
            orientation = validate_user_input('orientation',orientation)

        column = ''
        while column == '':
            column = input('Enter a column (letters A-{}): '.format(str.upper([chr(i + 97) for i in range(0,BOARD_SIZE)][-1:][0])))
            column = column.replace(' ', '')
            column = validate_user_input('column',column)

        row = ''
        while row == '':
            row = input('Enter a row (numbers 1-{}): '.format(BOARD_SIZE))
            row = row.replace(' ', '')
            row = validate_user_input('row', row)

        placement = [row, column, orientation]

        if validate_ship_placement(current_player, current_ship, placement) == True:
            players[current_player].ship_locations.append([current_ship, placement])
            ship_placed = place_ship(current_player, current_ship, placement)
        else:
            print('Try again!')


def validate_user_input(row_column_or_orientation, data):
    # returns index value of row or column or 'False' if not properly formatted, and h/v orientation

    if row_column_or_orientation == 'row':
        # Only accept strings that can be converted to int
        try:
            if int(data) in list(range(1,BOARD_SIZE + 1)):
                return int(data) - 1
            else:
                print('Enter a number between 1 and {}.'.format(BOARD_SIZE))
                return ''

        except ValueError:

            print('Please enter a number.')
            return ''

    elif row_column_or_orientation == 'column':

        valid_chars = [chr(i + 97) for i in range(0,BOARD_SIZE)]

        if str.lower(data) in valid_chars:
            return int(ord(str.lower(data)) - 97)
        else:
            print('Enter a character between A and {}.'.format(str.upper(valid_chars[-1:][0])))
            return ''

    elif row_column_or_orientation == 'orientation':
        if str.lower(data) in ['h','v']:
            return str.lower(data)
        else:
            error = 'Choose (H)orizontal or (V)ertical.'
            return error


def validate_ship_placement(current_player, current_ship, placement):
    ship_length = current_ship[1]

    row = placement[0]
    column = placement[1]
    orientation = placement[2]

    # Go through reasons a ship can't be placed and return False for any one
    try:
        if orientation == 'h':
            for i in range(0,ship_length):
                if players[current_player].ship_board[row][column + i] != EMPTY:
                    print('Blocked by an existing ship! Try again.')
                    return False

        else:
            for i in range(0,ship_length):
                if players[current_player].ship_board[row + i][column] != EMPTY:
                    print('Blocked by an existing ship! Try again.')
                    return False

    except IndexError:
        print('Ship will go off the board!')
        return False

    # Otherwise return True
    return True


def get_other_player(current_player):
    return list(set(players) - {players[current_player]})[0].number


def place_ship(current_player, current_ship, placement):
    ship_length = current_ship[1]

    row = placement[0]
    column = placement[1]
    orientation = placement[2]

    # horizontal ships in row
    if orientation == 'h':
            for i in range(0, ship_length):
                players[current_player].ship_board[row][column + i] = HORIZONTAL_SHIP
    # vertical ships in a column
    else:
        for i in range(0, ship_length):
            players[current_player].ship_board[row + i][column] = VERTICAL_SHIP

    return 'Ship placed'


def place_attack(current_player):
    # Board setting - placing the ships, validating input and board location
    ship_attacked = False

    while ship_attacked == False:

        print('{} attack!'.format(players[current_player].name))

        column = ''
        while column == '':
            column = input('Enter a column (letters A-{}): '.format(str.upper([chr(i + 97) for i in range(0,BOARD_SIZE)][-1:][0])))
            column = column.replace(' ', '')
            column = validate_user_input('column',column)

        row = ''
        while row == '':
            row = input('Enter a row (numbers 1-{}): '.format(BOARD_SIZE))
            row = row.replace(' ', '')
            row = validate_user_input('row', row)

        placement = [row, column]

        ship_attacked = make_attack(current_player, placement)


def make_attack(current_player, placement):
    row = placement[0]
    column = placement[1]

    enemy_player = get_other_player(current_player)
    current_guess_board = players[current_player].guess_board
    enemy_ship_board = players[enemy_player].ship_board

    if enemy_ship_board[row][column] in [VERTICAL_SHIP, HORIZONTAL_SHIP]:
        enemy_ship_board[row][column] = HIT
        current_guess_board[row][column] = HIT
        print('Direct hit!')
        check_for_sinking(current_player, row, column)

    elif enemy_ship_board[row][column] == EMPTY:
        enemy_ship_board[row][column] = MISS
        current_guess_board[row][column] = MISS
        print('Miss...')

    elif enemy_ship_board[row][column] in [HIT, MISS]:
        print('Ok but you already attacked here once... Try again')
        return False

    return True


def check_for_sinking(current_player, row, column):
    enemy_player = get_other_player(current_player)
    enemy_player_ships = players[enemy_player].ship_locations

    for ship in enemy_player_ships:
        ship_name = ship[0][0]
        ship_length = ship[0][1]
        row = ship[1][0]
        column = ship[1][1]
        orientation = ship[1][2]

        if orientation == 'h':
            if HORIZONTAL_SHIP not in players[enemy_player].ship_board[row][column:column + ship_length]:
                print('{} sunk!'.format(ship_name))
                mark_as_sunk(current_player, ship)
                enemy_player_ships.pop(enemy_player_ships.index(ship))

        else:
            vertical_ship_list = []

            for i in range(0, ship_length):
                vertical_ship_list.append(players[enemy_player].ship_board[row + i][column])

            if VERTICAL_SHIP not in vertical_ship_list:
                print('{} sunk!'.format(ship_name))
                mark_as_sunk(current_player, ship)
                enemy_player_ships.pop(enemy_player_ships.index(ship))
            else:
                pass

    pass


def mark_as_sunk(current_player, ship):
    #ship_name = ship[0][0]
    ship_length = ship[0][1]
    row = ship[1][0]
    column = ship[1][1]
    orientation = ship[1][2]
    enemy_player = get_other_player(current_player)

    # horizontal ships in row
    if orientation == 'h':
            for i in range(0, ship_length):
                players[current_player].guess_board[row][column + i] = SUNK
                players[enemy_player].ship_board[row][column + i] = SUNK
    # vertical ships in a column
    else:
        for i in range(0, ship_length):
            players[current_player].guess_board[row + i][column] = SUNK
            players[enemy_player].ship_board[row + i][column] = SUNK

    players[enemy_player].sunk_ships.append(ship[0])

    pass


def check_if_winner(current_player):
    enemy_player = get_other_player(current_player)

    if players[enemy_player].ship_locations == []:
        return True
    else:
        return False


# Game Setup


players = []


battleship_art = """
                                     # #  ( )
                                  ___#_#___|__
                              _  |____________|  _
                       _=====| | |            | | |==== _
                 =====| |.---------------------------. | |====
   <--------------------'   .  .  .  .  .  .  .  .   '--------------/
     \                                                             /
      \_______________________________________________WWS_________/
  wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
   wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww 

"""

clear_screen()

for player in range(0, 2):
    players.append(Player(player))
    players[player].name = input('Player {} enter your name: '.format(player + 1))



print(battleship_art)
print('********** {} vs {} **********'.format(players[0].name, players[1].name))

time.sleep(1)
clear_screen()

# Place the ships

for player in range(0,2):
    for ship in SHIP_INFO:
        ship_placement(ship, player)
        print('Your board {}:'.format(players[player].name))
        print_board(players[player].ship_board)
        clear_screen()
    clear_screen()
    input('Press enter for the next player...')

# Game Play

current_player = 0
winner = False

while winner == False:

    clear_screen()
    player_name = players[current_player].name

    print('{} your turn!\n'.format(player_name))
    input('Press enter to attack...')

    print('{} Guesses:'.format(player_name))

    # Print boards for current player
    print_board(players[current_player].guess_board)
    print('\n')

    print('Your board:')
    print_board(players[current_player].ship_board)
    print('\n')

    print('Your sunk ships:')
    for ship in players[current_player].sunk_ships:
        print(ship[0])
    print('\n')

    # Get their new shot placement
    place_attack(current_player)

    winner = check_if_winner(current_player)

    if winner == True:
        print('You won {}!'.format(player_name))
        break

    input('Type enter to continue')

    current_player = get_other_player(current_player)

    time.sleep(.5)

