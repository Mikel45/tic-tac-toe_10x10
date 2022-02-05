PLAY_BOARD = [" " for x in range(100)]
POSSIBLE_COMMANDS = ["user", "bot", "exit"]
START_MARK = "X"


def display_board(board):
    """Prints the tic-tac-toe board"""
    print("     1 2 3 4 5 6 7 8 9 10")
    print("   -----------------------")
    for i in range(10):
        num_str = str(i + 1)
        if i < 9:
            num_str += " "
        print(num_str, "|",
              board[i*10],
              board[i*10+1],
              board[i*10+2],
              board[i*10+3],
              board[i*10+4],
              board[i*10+5],
              board[i*10+6],
              board[i*10+7],
              board[i*10+8],
              board[i*10+9],
              "|")
    print("   -----------------------")


def cell_check(board, pos):
    """Checks if position is free"""
    return board[pos] == " "


def check_two(five, mark):
    """Checks if five elements in a row contains 2 same mark and 3 empty"""
    return five.count(mark) == 2 and five.count(" ") == 3


def check_three(five, mark):
    """Checks if five elements in a row contains 3 same mark and 2 empty"""
    return five.count(mark) == 3 and five.count(" ") == 2


def check_four(five, mark):
    """Checks if 5 elements in a row contains 4 same mark and 1 empty"""
    return five.count(mark) == 4 and five.count(" ") == 1


def check_five(five, mark):
    """Checks if 5 elements in a row have same mark"""
    return five.count(mark) == 5


def check_line(row, mark, check_func):
    """Applies check function to lines(from length 5 to 10)"""
    for i in range(len(row)-4):
        if check_func(row[i:i+5], mark):
            return True
    return False


def empty_indexes(board):
    """Creates new list with indexes where field is empty"""
    return [x for x, val in enumerate(board) if val == " "]


def check_board(board, mark, check_func):
    """Checks full board for 5 in row marks"""
    for i in range(10):
        if check_line(board[i*10:i*10+10], mark, check_func) or \
                check_line(board[i::10], mark, check_func) or \
                check_line(board[i:100-i*10:11], mark, check_func) or \
                check_line(board[i*10:100-i:11], mark, check_func) or \
                check_line(board[i*10+9:90+i+1:9], mark, check_func) or \
                check_line(board[i:i*10+1:9], mark, check_func):
            return True
    return False


def minimax(board, mark, depth, is_max):
    """Returns score for empty index"""
    opos_mark = "O" if mark == "X" else "X"
    if board.count(" ") > 35 and depth == 2:
        return 0
    if check_board(board, mark, check_five):
        return -40
    elif check_board(board, opos_mark, check_five):
        return 40
    elif check_board(board, mark, check_four):
        return -30
    elif check_board(board, opos_mark, check_four):
        return 30
    elif check_board(board, mark, check_three):
        return -20
    elif check_board(board, opos_mark, check_three):
        return 20
    elif check_board(board, mark, check_two):
        return -10
    elif check_board(board, opos_mark, check_two):
        return 10
    elif len(empty_indexes(board)) == 0:
        return 1

    if is_max:
        best_score = -1000
        for i in empty_indexes(board):
            board[i] = mark
            score = minimax(board, mark, depth + 1, False)
            board[i] = " "
            best_score = max(best_score, score)
    else:
        best_score = 1000
        for i in empty_indexes(board):
            board[i] = opos_mark
            score = minimax(board, mark, depth + 1, True)
            board[i] = " "
            best_score = min(best_score, score)
    return best_score


def cord_bot(board, mark):
    """Goes through empty indexes and finds best one to make move"""
    move = None
    best_score = -1000
    for i in empty_indexes(board):
        board[i] = mark
        score = minimax(board, mark, 0, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i
    print("Bot making move")
    return move


def user_choice(board):
    """Validates user's input"""
    while True:
        user_cord = input("Enter the coordinates(y(row), x(column)): ").split()
        try:
            x = int(user_cord[0])
            y = int(user_cord[1])
        except ValueError:
            print("You should enter numbers!")
            continue
        except IndexError:
            print("You should enter at least something!")
            continue
        if 0 < x < 11 and 0 < y < 11:
            pos = (x - 1) * 10 + y - 1
            if cell_check(board, pos):
                return pos
            print("This cell is occupied! Choose another one!")
        else:
            print("Coordinates should be from 1 to 10!")


def game_status(board):
    """Prints games status and returns state"""
    if check_board(board, "X", check_five):
        print("O wins")
    elif check_board(board, "O", check_five):
        print("X wins")
    elif not check_board(board, "X", check_five) and not check_board(board, "O", check_five) and " " not in board:
        print("Draw")
    else:
        return True
    return False


def game_mode():
    """Reads commands"""
    while True:
        print("To start game type: start user(or bot) user(or bot). If you want to exit type: exit")
        input_command = input("Input command: ")
        if input_command == POSSIBLE_COMMANDS[-1]:
            return "exit"
        input_command = input_command.split()
        if len(input_command) == 3:
            if input_command[0] == "start" and \
                    input_command[1] in POSSIBLE_COMMANDS[:2] and \
                    input_command[2] in POSSIBLE_COMMANDS[:2]:
                return input_command[1], input_command[2]
        print("Bad parameters!")


def game_process(board_orig, curr_mark_orig):
    """Runs game"""
    while True:
        board = board_orig[:]
        curr_mark = curr_mark_orig
        commands = game_mode()
        if commands == "exit":
            break
        display_board(board)
        while game_status(board):
            if curr_mark == "X":
                if commands[0] == "user":
                    player_position = user_choice(board)
                else:
                    player_position = cord_bot(board, curr_mark)
            else:
                if commands[1] == "user":
                    player_position = user_choice(board)
                else:
                    player_position = cord_bot(board, curr_mark)
            board[player_position] = curr_mark
            curr_mark = "O" if curr_mark == "X" else "X"
            display_board(board)


game_process(PLAY_BOARD, START_MARK)
