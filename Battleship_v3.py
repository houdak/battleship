# This is a game of battleship, based off of Codecademy course (my first program!)
# It currently supports a human playing against a computer

# The computer is somwhat 'smart':
# When picking randomly, it only guesses boxes which would fit in a checkerboard pattern
# Once it hits a ship, it guesses all surrounding spaces before moving on, helping it sink ships
# The concepts for a smarter computer are based on the following article: http://www.datagenetics.com/blog/december32011/index.html


from random import randint
from random import choice


# Dictionary to interpret letter index at top of board
letter_dict = {'A': 0,
               'B': 1,
               'C': 2,
               'D': 3,
               'E': 4,
               'F': 5,
               'G': 6,
               'H': 7}

# Dictionary to make printed statements look nicer(word instead of number)
number_dict = {1: 'one',
               2: 'two',
               3: 'three',
               4: 'four',
               5: 'five'}

# List of directions to make checking valid player input easier
direc_list = ['north', 'south', 'east', 'west']


# Fxn to make 8x8 board of 'O's
def make_board():
    board = []
    for __ in range(8):
        board.append(["O"]*8)
    return board

# Make all the boards that are needed for the game
comp_board = make_board()   # Shows player's hits/misses on the computer's board
hidden_board = make_board() # Where the computer hides ships' locations
player_board = make_board() # Where the player hides their ships


# Print boards with nicer format
# If second argument added, can print both boards
def print_board(*boards):
    if comp_board in boards:
        # Print letters on top edge
        print('\n', 'Computer Board', '\n', '\n', end= '  ', sep = '')
        for letter in letter_dict:
            print(letter, end= ' ')
        print('')
        # Print board filled with placeholders
        # And with number labels on the left
        label = 0
        for row in comp_board:
            label += 1
            print(str(label), " ".join(row))
        print('\n', end='')
    print('', end='', sep='') 
    if player_board in boards:
        # Print letters on top edge
        print('\n', 'Player Board', '\n', '\n', end= '  ', sep = '')
        for letter in letter_dict:
            print(letter, end= ' ')
        print('')
        # Print board filled with placeholders
        # And with number labels on the left
        label = 0
        for row in player_board:
            label += 1
            print(str(label), " ".join(row))
        print('\n', end='')



# Fxn for picking random locations and directions for boats by computer
def random_row(board):
    return randint(0, len(board) - 1)
def random_col(board):
    return randint(0, len(board[0]) - 1)
directions = ['north', 'south', 'east', 'west']
def random_dir():
    return choice(directions)

# Both assume board is 8 spaces long (0-7)
# Use random_col to get col. Get even box based on that
def random_row_parity(guess_col):
    if guess_col % 2 == 0:
        return choice([1,3,5,7])
    else:
        return choice([0,2,4,6])


# Check to see if player input for ship loc (placement or guess) was valid
def valid_input(player_input):
    try:
        if (    len(player_input) == 2
            and int(player_input[1]) <= 8
            and int(player_input[1]) >= 1
            and player_input[0].upper() in letter_dict):
                return True
        else:
            return False
    except:
        return False


# Fxn for validating location, used after checking if input was valid
def valid(locations):
    validity = []
    for loc in locations:
        if loc == 'O':
            validity.append(True)
        else:
            return False
    return all(validity)


# Fxn to initially check if index is in range for place_ship
# Really repetative, not sure how to shorten it
def index_check(self, row, col, direc):
    if direc == 'east':
         if col + self.length > len(comp_board):
             return False
         else:
             return True
    elif direc == 'west':
        if col - self.length < -1:
            return False
        else:
            return True
    elif direc == 'south':
        if row + self.length > len(comp_board):
            return False
        else:
            return True
    elif direc == 'north':
        if row - self.length < -1:
            return False
        else:
            return True

# Method to check if target_dict is empty
# Slightly involved because rows are always there
def empty_target_dict(target_dict):
    checklist = 0
    for i in target_dict:
        if target_dict[i] != []:
            checklist += 1
    if checklist > 0:
        return False
    else:
        return True

# Define a class of ships with relevant methods
class Ship(object):
    sunk = False
    hits = 0
    def __init__(self, name, symbol, length):
        self.name = name
        self.length = length
        self.symbol = symbol
        
    # Method to determine status of ship
    def is_sunk(self):
        if self.hits == self.length:
            return True
        
    #Method to extend ship. Used in place_ship fxn's
    def extend_ship(self, row, col, direc, board):
        locations = []
        if direc == 'east':
            for i in range(0, self.length):
                locations.append(board[row][col + i])
        elif direc == 'west':
            for i in range(0, self.length):
                locations.append(board[row][col - i])
        elif direc == 'south':
            for i in range(0, self.length):
                locations.append(board[row + i][col])
        elif direc == 'north':
            for i in range(0, self.length):
                locations.append(board[row - i][col])
        return locations

    # Method to randomly place ship on board
    # Checks that placement is valid (on board, no overlap)
    # Will likely have to retry many times, especially with 5 ships
    def comp_place_ship(self):
        valid_location = False
        while valid_location == False:
            row = random_row(comp_board)
            col = random_row(comp_board)
            direc = random_dir()
            if index_check(self, row, col, direc) == False:
                continue
            locations = self.extend_ship(row, col, direc, hidden_board)
            if valid(locations) == True:
                valid_location = True
            else:
                continue
        for i in range(0, self.length):
            if direc == 'east':
                hidden_board[row][col + i] = self.symbol
            elif direc == 'west':
                hidden_board[row][col - i] = self.symbol
            elif direc == 'south':
                hidden_board[row + i][col] = self.symbol
            elif direc == 'north':
                hidden_board[row - i][col] = self.symbol
    
    # Method for player to place boats onto their board
    # Also checks validity of location (formatted as 'b4' or 'D5') and direction
    def player_place_ship(self):
        valid_location = False
        while valid_location == False:
            print("Your %s is %s spaces long."
                  %(str(self.name), str(number_dict[self.length])), end = ' ')
            point = 'Blank'
            while valid_input(point) == False:
                try:
                    point = str(input("Where would you like it to go?: "))
                except:
                    print('\n', "Oops, that's not even in the ocean.",
                        " Try inputing a location like 'B4' or 'd1'.", '\n', sep='')
                    continue
                if valid_input(point) == False:
                    print('\n', "Oops, that's not even in the ocean.",
                        " Try inputing a location like 'B4' or 'd1'.", '\n', sep='')
            direc = 'Blank'
            while direc not in direc_list:
                try:
                    direc = str(input("Facing which direction? (east, west, north or south): ")).lower()
                except:
                    print('\n', "Oops, that's not even in the ocean.", '\n', sep='')
                    continue
            row = int(point[1])-1
            col = letter_dict[point[0].upper()]
            if index_check(self, row, col, direc) == False:
                print('\n', "Oops, that didn't work, try again.", '\n', sep='')
                continue
            locations = self.extend_ship(row, col, direc, player_board)
            if valid(locations) == True:
                valid_location = True
            else:
                print('\n', "Oops, that didn't work, try again.", '\n', sep='')
                continue
        for i in range(self.length):
            if direc == 'east':
                player_board[row][col + i] = self.symbol
            elif direc == 'west':
                player_board[row][col - i] = self.symbol
            elif direc == 'south':
                player_board[row + i][col] = self.symbol
            elif direc == 'north':
                player_board[row - i][col] = self.symbol

    # Method for checking if boat has been hit
    def calculate_hits(self, board):
        self.count = 0
        for i in board:
            for j in i:
                if j == self.symbol:
                    #count == length when boat hasn't been hit
                    self.count += 1
        self.hits = self.length - self.count
        return self.hits


# Create five ships of different length for player and computer
Aircraft_Carrier = Ship('Aircraft Carrier', 'A', 5)
Battleship = Ship('Battleship', 'B', 4)
Submarine = Ship('Submarine', 'S', 3)
Cruiser = Ship('Cruiser', 'C', 3)
Destroyer = Ship('Destroyer', 'D', 2)

#Put in list to make repetative processes easier
all_ships = [Aircraft_Carrier,
             Battleship,
             Submarine,
             Cruiser,
             Destroyer]


# The computer will place their ships
for ship in all_ships:
    ship.comp_place_ship()


# Start game! Give the player a chance to hide their ships

print("Let's play Battleship!", '\n')
print("I've hidden my ships. Now it's your turn!", '\n')
print_board(comp_board, player_board)
print('\n', "You have a total of 5 ships of different lengths.", sep='')
print("Input the location and direction you'd like it to go (ex. 'B4', or 'd1').", '\n')

for ship in all_ships:
    ship.player_place_ship()
    print("Looks good! Here's your board so far!")
    print_board(player_board)

# Instructions for the player
print('\n', '\n', "Now you will take turns with me to find each other's battleships.", sep='')
print("You can go first: Guess where my ship might be by inputting the location (ex. 'H1' or 'a2')!", '\n')
print_board(comp_board, player_board)

# Turn-by-turn gameplay starts here
comp_total_sunk = []
player_total_sunk = []

# Initialize target_dict. Should have lists for each value
# Format should be {col1: row1, col2: row2 .......} so col = key, row = value
# Made slightly too big so that no errors occur when adding new targets
# These out-of-range targets are removed at the end of the turn
target_dict = {}
for i in range(-1,9):
    target_dict[i] = []

game_over = False
while game_over == False:
    # Player inputs guess for where ship might be
    # Checks that input was valid before continuing
    player_input = False
    while valid_input(player_input) == False:
        try:
            player_input = str(input("Your guess:"))
        except:
            print('\n', "Oops, that's not even in the ocean.", '\n', sep='')
            continue
        if valid_input(player_input) == False:
            print('\n', "Oops, that's not even in the ocean.", '\n', sep='')
            continue
    guess_row = int(player_input[1]) - 1
    guess_col = letter_dict[player_input[0].upper()]

    # Check against each possible symbol in place
    ## For X, means its already guessed
    if hidden_board[guess_row][guess_col] == 'X':
        print('\n', "You guessed that one already.", '\n', sep='')
        continue
        
    ## For O, means it was a miss. Update boards
    elif hidden_board[guess_row][guess_col] == 'O':
        print('\n', "You missed my battleship.", '\n', sep='')
        hidden_board[guess_row][guess_col] = 'X'
        comp_board[guess_row][guess_col] = 'X'

    ## For any other symbol, need to see what ship was hit. Update the boards.
    ## And check if any of them have sunk!
    ## Print message with number sunk if a new ship has sunk
    else:
        count_sunk = 0
        hidden_board[guess_row][guess_col] = 'X'
        comp_board[guess_row][guess_col] = 'H'
        print('\n', "You've hit my battleship!", '\n', sep='')
        for ship in all_ships:
            ship.hits = ship.calculate_hits(hidden_board)
            if ship.is_sunk() == True:
                count_sunk += 1
        comp_total_sunk.append(count_sunk)
        if len(comp_total_sunk) == 1 and comp_total_sunk[0] == 1:
            print("You've sunk %s of my ships!"
                  %str(number_dict[player_total_sunk[len(player_total_sunk)-1]]), '\n')
        elif (comp_total_sunk[len(comp_total_sunk)-1] >
              comp_total_sunk[len(comp_total_sunk)-2]):
            print("You've sunk %s of my ships!"
                  %str(number_dict[comp_total_sunk[len(comp_total_sunk)-1]]), '\n')
            # Check if the game is over (player win). If so, break.
            if 5 in comp_total_sunk:
                print('\n', "You win!", sep='')
                break 

    # Now start the computer's turn
    print_board(comp_board) #So player can see where their hit was
    print('\n', end='')
    input('Press any key to continue: ')
    print('\n', "Now it's my turn!", sep='')

    # The ship picks a spot to hit. Must verify that it has not been hit before
    valid_location = False
    while valid_location == False:
        # Picks randomly from board if target_dict is empty ('Hunt' mode)
        # Uses parity to only guess even boxes
        if empty_target_dict(target_dict) == True:
            guess_col = random_col(player_board)
            guess_row = random_row_parity(guess_col)
            if (    player_board[guess_row][guess_col] != 'X'
                and player_board[guess_row][guess_col] != 'H'):
                valid_location = True
        # Picks randomly from target_dict if it is not empty ('Target' mode)
        else:
            # Make list of target_dict cols that aren't empty
            nonempty_target = []
            for col in target_dict:
                if target_dict[col] != []:
                    nonempty_target.append(col)
            guess_col = choice(nonempty_target)
            guess_row = choice(target_dict[guess_col]) # Picks from list within col
            if (    player_board[guess_row][guess_col] != 'X'
                and player_board[guess_row][guess_col] != 'H'):
                valid_location = True

    # Go through steps to check whether the computer has hit a ship
    ## If it's a miss, change spot from 'O' to 'X'
    if player_board[guess_row][guess_col] == 'O':
        print('\n', "I missed!", '\n', sep='')
        player_board[guess_row][guess_col] = 'X'
    
    ## If its a hit, change from 'O' to 'X', calculate hits, and see if any ships have sunk
    else:
        # Change from 'O' to 'X', calculate hits,
        count_sunk = 0
        player_board[guess_row][guess_col] = 'H'
        print('\n', "I've hit your battleship!", '\n', sep='')
        for ship in all_ships:
            ship.hits = ship.calculate_hits(player_board)
            if ship.is_sunk() == True:
                count_sunk += 1
        player_total_sunk.append(count_sunk)
        
        # Add new spots to target_dict
        target_dict[guess_col+1].append(guess_row)
        target_dict[guess_col-1].append(guess_row)
        target_dict[guess_col].append(guess_row+1)
        target_dict[guess_col].append(guess_row-1)
        
        # Check if any ships have sunk
        if len(player_total_sunk) == 1 and player_total_sunk[0] == 1:
            print("I've sunk %s of your ships!"
                  %str(number_dict[player_total_sunk[len(player_total_sunk)-1]]), '\n')
        elif (player_total_sunk[len(player_total_sunk)-1] >
              player_total_sunk[len(player_total_sunk)-2]):
            print("I've sunk %s of your ships!"
                  %str(number_dict[player_total_sunk[len(player_total_sunk)-1]]), '\n')
            # Check if the game is over (computer win). If so, break.
            if 5 in player_total_sunk:
                print('\n', "You've lost the game :(", sep='')
                break

    # Delete any spots from target_dict that have already been tested
    new_dict = {}
    for col in target_dict:
        new_dict[col] = []
        for row in target_dict[col]:
            try:
                if (   player_board[row][col] != 'X'
                   and player_board[row][col] != 'H'):
                    new_dict[col].append(row)
            except:
                new_dict = new_dict # Don't add invalid target back into target_dict
    target_dict = new_dict

    print_board(player_board) #So player can see where computer hit
    input('Press any key to continue: ')
    print_board(comp_board)
