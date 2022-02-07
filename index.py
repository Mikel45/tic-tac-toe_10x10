PLAY_BOARD = [" " for x in range(100)]
POSSIBLE_COMMANDS = ["A", "B", "exit"]
START_MARK = "X"


def display_board(board):
    """Prints the tic-tac-toe board"""
    print("     1 2 3 4 5 6 7 8 9 10")
    print("   -----------------------")
    for i in range(10):
        num_str = str(i + 1)
        if i < 9:
            num_str += " "
        line = [board[i*10+j] for j in range(10)]
        print(num_str, "|", *line, "|")
    print("   -----------------------")


def cell_check(board, pos):
    """Checks if position is free"""
    return board[pos] == " "


def check_five(five, mark):
    """Checks if 5 elements in a row have same mark"""
    return five.count(mark) == 5


def check_line(row, mark):
    """Applies check function to lines(from length 5 to 10)"""
    for i in range(len(row)-4):
        if check_five(row[i:i+5], mark):
            return True
    return False


def empty_indexes(board):
    """Creates new list with indexes where field is empty"""
    return [x for x, val in enumerate(board) if val == " "]


def check_board(board, mark):
    """Checks full board for 5 in row marks"""
    for i in range(10):
        if check_line(board[i*10:i*10+10], mark) or \
                check_line(board[i::10], mark) or \
                check_line(board[i:100-i*10:11], mark) or \
                check_line(board[i*10:100-i:11], mark) or \
                check_line(board[i*10+9:90+i+1:9], mark) or \
                check_line(board[i:i*10+1:9], mark):
            return True
    return False


def minimax(board, mark, depth, is_max):
    """Returns score for empty index"""
    opos_mark = "O" if mark == "X" else "X"
    if depth == 2:
        return 0
    if check_board(board, mark):
        return -40
    elif check_board(board, opos_mark):
        return 40
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
            print("There should be 2 numbers with space between them!")
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
    if check_board(board, "X"):
        print("O wins")
    elif check_board(board, "O"):
        print("X wins")
    elif not check_board(board, "X") and not check_board(board, "O") and " " not in board:
        print("Draw")
    else:
        return True
    return False


def game_mode():
    """Reads commands"""
    while True:
        print('To start game type: "A" to play user vs bot, "B" to play bot vs bot, or "exit" if you want to finish.')
        input_command = input("Input command: ")
        if input_command == "exit":
            return "exit"
        if input_command in POSSIBLE_COMMANDS[:2]:
            return input_command
        print("Bad parameters!")


def game_process(board_orig, curr_mark_orig):
    """Runs game"""
    while True:
        board = board_orig[:]
        curr_mark = curr_mark_orig
        command = game_mode()
        if command == "exit":
            break
        display_board(board)
        while game_status(board):
            if command == "A" and curr_mark == "X":
                player_position = user_choice(board)
            else:
                player_position = cord_bot(board, curr_mark)
            board[player_position] = curr_mark
            curr_mark = "O" if curr_mark == "X" else "X"
            display_board(board)


game_process(PLAY_BOARD, START_MARK)
