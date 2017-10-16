import time


class GameBase():
    def __init__(self):
        self.SHIP_INFO = [
            ("Aircraft Carrier", 5),
            ("Battleship", 4),
            ("Submarine", 3),
            ("Cruiser", 3),
            ("Patrol Boat", 2)
         ]
        self.BOARD_SIZE = 10
        self.VERTICAL_SHIP = '|'
        self.HORIZONTAL_SHIP = '-'
        self.EMPTY = 'O'
        self.MISS = '.'
        self.HIT = '*'
        self.SUNK = '#'

    def print_board_heading(self):
        print("   " + " ".join(
            [chr(c) for c in range(ord('A'), ord('A') + self.BOARD_SIZE)]))

    def print_board(self, board):
        self.print_board_heading()

        row_num = 1
        for row in board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

    def clear_screen(self):
        print("\033c", end="")

    def make_empty_board(self, board_size):
        board = []
        for i in range(0, board_size):
            board_row = []
            for i in range(0, board_size):
                board_row.append(self.EMPTY)
            board.append(board_row)
        return board


class Player(GameBase):
    def __init__(self, player_number):
        GameBase.__init__(self)
        self.number = player_number
        self.ship_board = self.make_empty_board(self.BOARD_SIZE)
        self.guess_board = self.make_empty_board(self.BOARD_SIZE)
        self.ship_locations = []
        self.sunk_ships = []
        self.name = ''


class Game(GameBase):
    def __init__(self):
        GameBase.__init__(self)
        self.setup_board_and_players()

    def play(self):
        self.place_ships()
        self.gameplay()

    def setup_board_and_players(self):
        self.players = []

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
        wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
           wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww

        """

        self.clear_screen()

        for player in range(0, 2):
            self.players.append(Player(player))
            self.players[player].name = \
                input('Player {} enter your name: '.format(player + 1))

        print(battleship_art)
        print('********** {} vs {} **********'.format(
            self.players[0].name, self.players[1].name))

        time.sleep(1)
        self.clear_screen()

    def place_ships(self):
        for player in range(0, 2):
            for ship in self.SHIP_INFO:
                self.ship_placement(ship, player)
                print('Your board {}:'.format(self.players[player].name))
                self.print_board(self.players[player].ship_board)
                self.clear_screen()
            self.clear_screen()
            input('Press enter for the next player...')

    def gameplay(self):
        current_player = 0
        winner = False

        while winner is False:
            self.clear_screen()
            player_name = self.players[current_player].name

            print('{} your turn!\n'.format(player_name))
            input('Press enter to attack...')
            print('{} Guesses:'.format(player_name))

            # Print boards for current player
            self.print_board(self.players[current_player].guess_board)
            print('\n')
            print('Your board:')
            self.print_board(self.players[current_player].ship_board)
            print('\n')
            print('Your sunk ships:')
            for ship in self.players[current_player].sunk_ships:
                print(ship[0])
            print('\n')

            # Get their new shot placement
            self.place_attack(current_player)
            winner = self.check_if_winner(current_player)

            if winner is True:
                print('You won {}!'.format(player_name))
                break

            input('Type enter to continue')

            current_player = self.get_other_player(current_player)
            time.sleep(.5)

    def ship_placement(self, current_ship, current_player):
        # Board setting - placing ships, validating input and board location
        ship_placed = 'No'

        self.clear_screen()

        while ship_placed == 'No':

            print('Your board {}:\n'.format(self.players[current_player].name))
            self.print_board(self.players[current_player].ship_board)
            print('Place your ship. {} occupies {} spaces.'.format(
                current_ship[0], current_ship[1]))

            orientation = ''
            while orientation == '':
                orientation = input('Horizontal or Vertical? (H, V): ')
                orientation = orientation.replace(' ', '')
                orientation = self.validate_user_input(
                    'orientation', orientation)

            column = ''
            while column == '':
                column = input('Enter a column (letters A-{}): '.format(
                    str.upper([chr(i + 97) for i in range(
                        0, self.BOARD_SIZE)][-1:][0])))
                column = column.replace(' ', '')
                column = self.validate_user_input('column', column)

            row = ''
            while row == '':
                row = input('Enter a row (numbers 1-{}): '.format(
                    self.BOARD_SIZE))
                row = row.replace(' ', '')
                row = self.validate_user_input('row', row)

            placement = [row, column, orientation]

            if self.validate_ship_placement(
                    current_player, current_ship, placement):
                self.players[current_player].ship_locations.append(
                    [current_ship, placement])
                ship_placed = self.place_ship(
                    current_player, current_ship, placement)
            else:
                print('Try again!')

    def validate_user_input(self, row_column_or_orientation, data):
        if row_column_or_orientation == 'row':
            # Only accept strings that can be converted to int
            try:
                if int(data) in list(range(1, self.BOARD_SIZE + 1)):
                    return int(data) - 1
                else:
                    print('Enter a number between 1 and {}.'.format(
                        self.BOARD_SIZE))
                    return ''

            except ValueError:

                print('Please enter a number.')
                return ''

        elif row_column_or_orientation == 'column':

            valid_chars = [chr(i + 97) for i in range(0, self.BOARD_SIZE)]

            if str.lower(data) in valid_chars:
                return int(ord(str.lower(data)) - 97)
            else:
                print('Enter a character between A and {}.'.format(
                    str.upper(valid_chars[-1:][0])))
                return ''

        elif row_column_or_orientation == 'orientation':
            if str.lower(data) in ['h', 'v']:
                return str.lower(data)
            else:
                print('Choose (H)orizontal or (V)ertical.')
                return ''

    def validate_ship_placement(self, current_player, current_ship, placement):
        ship_length = current_ship[1]

        row = placement[0]
        column = placement[1]
        orientation = placement[2]

        # Go through reasons a ship can't be placed, return False for any one
        try:
            if orientation == 'h':
                for i in range(0, ship_length):
                    if (self.players[current_player].ship_board
                            [row][column + i] != self.EMPTY):
                        print('Blocked by an existing ship! Try again.')
                        return False

            else:
                for i in range(0, ship_length):
                    if (self.players[current_player].ship_board
                            [row + i][column] != self.EMPTY):
                        print('Blocked by an existing ship! Try again.')
                        return False

        except IndexError:
            print('Ship will go off the board!')
            return False

        # Otherwise return True
        return True

    def get_other_player(self, current_player):
        return list(set(self.players) -
                    {self.players[current_player]})[0].number

    def place_ship(self, current_player, current_ship, placement):
        ship_length = current_ship[1]

        row = placement[0]
        column = placement[1]
        orientation = placement[2]

        # horizontal ships in row
        if orientation == 'h':
                for i in range(0, ship_length):
                    (self.players[current_player].ship_board
                     [row][column + i]) = self.HORIZONTAL_SHIP
        # vertical ships in a column
        else:
            for i in range(0, ship_length):
                (self.players[current_player].ship_board
                 [row + i][column]) = self.VERTICAL_SHIP

        return 'Ship placed'

    def place_attack(self, current_player):
        # Board setting - placing the ships, validate input and board location
        ship_attacked = False

        while ship_attacked is False:

            print('{} attack!'.format(self.players[current_player].name))

            column = ''
            while column == '':
                column = input('Enter a column (letters A-{}): '.format(
                    str.upper([chr(i + 97) for i in range(
                        0, self.BOARD_SIZE)][-1:][0])))
                column = column.replace(' ', '')
                column = self.validate_user_input('column', column)

            row = ''
            while row == '':
                row = input('Enter a row (numbers 1-{}): '.format(
                    self.BOARD_SIZE))
                row = row.replace(' ', '')
                row = self.validate_user_input('row', row)

            placement = [row, column]

            ship_attacked = self.make_attack(current_player, placement)

    def make_attack(self, current_player, placement):
        row = placement[0]
        column = placement[1]

        enemy_player = self.get_other_player(current_player)
        current_guess_board = self.players[current_player].guess_board
        enemy_ship_board = self.players[enemy_player].ship_board

        if enemy_ship_board[row][column] in [self.VERTICAL_SHIP,
                                             self.HORIZONTAL_SHIP]:
            enemy_ship_board[row][column] = self.HIT
            current_guess_board[row][column] = self.HIT
            print('Direct hit!')
            self.check_for_sinking(current_player, row, column)

        elif enemy_ship_board[row][column] == self.EMPTY:
            enemy_ship_board[row][column] = self.MISS
            current_guess_board[row][column] = self.MISS
            print('Miss...')

        elif enemy_ship_board[row][column] in [self.HIT, self.MISS]:
            print('Ok but you already attacked here once... Try again')
            return False

        return True

    def check_for_sinking(self, current_player, row, column):
        enemy_player = self.get_other_player(current_player)
        enemy_player_ships = self.players[enemy_player].ship_locations

        for ship in enemy_player_ships:
            ship_name = ship[0][0]
            ship_length = ship[0][1]
            row = ship[1][0]
            column = ship[1][1]
            orientation = ship[1][2]

            if orientation == 'h':
                if self.HORIZONTAL_SHIP not in \
                        (self.players[enemy_player].ship_board[row]
                         [column:column + ship_length]):
                    print('{} sunk!'.format(ship_name))
                    self.mark_as_sunk(current_player, ship)
                    enemy_player_ships.pop(enemy_player_ships.index(ship))

            else:
                vertical_ship_list = []

                for i in range(0, ship_length):
                    vertical_ship_list.append(
                        self.players[enemy_player].ship_board[row + i][column])

                if self.VERTICAL_SHIP not in vertical_ship_list:
                    print('{} sunk!'.format(ship_name))
                    self.mark_as_sunk(current_player, ship)
                    enemy_player_ships.pop(enemy_player_ships.index(ship))
                else:
                    pass

        pass

    def mark_as_sunk(self, current_player, ship):
        ship_length = ship[0][1]
        row = ship[1][0]
        column = ship[1][1]
        orientation = ship[1][2]
        enemy_player = self.get_other_player(current_player)

        # horizontal ships in row
        if orientation == 'h':
                for i in range(0, ship_length):
                    (self.players[current_player].guess_board
                     [row][column + i]) = self.SUNK
                    (self.players[enemy_player].ship_board
                     [row][column + i]) = self.SUNK

        # vertical ships in a column
        else:
            for i in range(0, ship_length):
                (self.players[current_player].guess_board
                 [row + i][column]) = self.SUNK
                (self.players[enemy_player].ship_board
                 [row + i][column]) = self.SUNK

        self.players[enemy_player].sunk_ships.append(ship[0])

        pass

    def check_if_winner(self, current_player):
        enemy_player = self.get_other_player(current_player)

        if self.players[enemy_player].ship_locations == []:
            return True
        else:
            return False


if __name__ == '__main__':
    battleship = Game()
    battleship.play()
