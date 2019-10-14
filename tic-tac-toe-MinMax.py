from math import inf as infinity
from os import system, name
from time import sleep

game_state = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]
players = ['X', 'O']


def MinMax(state, player):
    '''
    Minimax Algorithm
    '''
    # Base conditions for recursion
    winner_loser, done = check_current_state(state)
    if done == "Done" and winner_loser == 'O':  # If AI won
        return 1
    elif done == "Done" and winner_loser == 'X':  # If Human won
        return -1
    elif done == "Draw":    # Draw condition
        return 0

    moves = []
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if state[i][j] is ' ':
                empty_cells.append(i*3 + (j+1))

    for empty_cell in empty_cells:
        move = {}
        move['index'] = empty_cell
        new_state = copy_game_state(state)
        play_move(new_state, player, empty_cell)

        if player == 'O':    # If AI
            # make more depth tree with next turn as human
            result = MinMax(new_state, 'X')
            move['score'] = result
        else:                # If Human
            # make more depth tree with next turn as AI
            result = MinMax(new_state, 'O')
            move['score'] = result

        moves.append(move)

    # Find best move
    best_move = None
    if player == 'O':   # If AI
        best = -infinity
        for move in moves:
            if move['score'] > best:
                best = move['score']
                best_move = move['index']
    else:               # If Human
        best = infinity
        for move in moves:
            if move['score'] < best:
                best = move['score']
                best_move = move['index']

    # return best move
    return best_move


def play_move(state, player, block_num):
    '''
    Checks if the next move is valid or not.
    If next move is not vaid then again take a valid input from the user
    '''
    if state[int((block_num-1)/3)][(block_num-1) % 3] is ' ':
        state[int((block_num-1)/3)][(block_num-1) % 3] = player
    else:
        block_num = int(
            input("Block is not empty! Choose again: "))
        play_move(state, player, block_num)


def copy_game_state(state):
    '''
    Returns a copy of current game state.
    '''
    new_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state


def clear():
    '''
    Clears the terminal window.
    '''
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def check_current_state(game_state):
    '''
    Check the current state of the game and if there is winner return it
    return the winner otherwise returns None.
    '''
    draw_flag = 0        # flag to check later for a Draw
    for i in range(3):
        for j in range(3):
            if game_state[i][j] is ' ':
                draw_flag = 1     # if there is an empty block it raises a flag which means no Draw
                break

    # Check diagonals
    if (game_state[0][0] == game_state[1][1] and game_state[1][1] == game_state[2][2] and game_state[0][0] is not ' '):
        return game_state[1][1], "Done"
    elif (game_state[2][0] == game_state[1][1] and game_state[1][1] == game_state[0][2] and game_state[2][0] is not ' '):
        return game_state[1][1], "Done"

    # Check horizontals
    elif (game_state[0][0] == game_state[0][1] and game_state[0][1] == game_state[0][2] and game_state[0][0] is not ' '):
        return game_state[0][0], "Done"
    elif (game_state[1][0] == game_state[1][1] and game_state[1][1] == game_state[1][2] and game_state[1][0] is not ' '):
        return game_state[1][0], "Done"
    elif (game_state[2][0] == game_state[2][1] and game_state[2][1] == game_state[2][2] and game_state[2][0] is not ' '):
        return game_state[2][0], "Done"

    # Check verticals
    elif (game_state[0][0] == game_state[1][0] and game_state[1][0] == game_state[2][0] and game_state[0][0] is not ' '):
        return game_state[0][0], "Done"
    elif (game_state[0][1] == game_state[1][1] and game_state[1][1] == game_state[2][1] and game_state[0][1] is not ' '):
        return game_state[0][1], "Done"
    elif (game_state[0][2] == game_state[1][2] and game_state[1][2] == game_state[2][2] and game_state[0][2] is not ' '):
        return game_state[0][2], "Done"
    # Check Draws
    elif draw_flag is 0:
        return None, "Draw"  # if flag is not raised it means a Draw

    return None, "Not Done"


def print_board(game_state):
    '''
    Prints the board on the terminal
    '''
    clear()
    print('----------------')
    print('| ' + str(game_state[0][0]) + ' || ' +
          str(game_state[0][1]) + ' || ' + str(game_state[0][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[1][0]) + ' || ' +
          str(game_state[1][1]) + ' || ' + str(game_state[1][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[2][0]) + ' || ' +
          str(game_state[2][1]) + ' || ' + str(game_state[2][2]) + ' |')
    print('----------------')


play_again = 'Y'
while play_again == 'Y' or play_again == 'y':
    game_state = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
    current_state = "Not Done"
    print("Starting Tic Tac Toe")
    sleep(1)
    print_board(game_state)
    player_choice = input(
        "Choose which player goes first - X (You) or O (AI): ")
    winner = None

    if player_choice == 'X' or player_choice == 'x':
        current_player_idx = 0
    elif player_choice == 'O' or player_choice == 'o':
        current_player_idx = 1
    else:
        print("Wrong choice!")
        continue

    while current_state == "Not Done":
        if current_player_idx == 0:  # Human's turn
            block_choice = int(
                input("Oye Human, your turn! Choose where to place (1 to 9): "))
            play_move(game_state, players[current_player_idx], block_choice)
        else:   # AI's turn
            block_choice = MinMax(game_state, players[current_player_idx])
            play_move(game_state, players[current_player_idx], block_choice)
            print("\nAI's move is: " + str(block_choice))
            sleep(1)

        print_board(game_state)
        winner, current_state = check_current_state(game_state)

        if winner is not None:
            print(str(winner) + " won!")
        else:
            current_player_idx = (current_player_idx + 1) % 2

        if current_state is "Draw":
            print("Draw!")

    play_again = input('Wanna try again?(Y/N) : ')
    if play_again == 'N' or play_again == 'n':
        print('Thanks for Playing')
        sleep(1.5)
