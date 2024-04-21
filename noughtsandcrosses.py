import random
import os.path
import json
random.seed()

def draw_board(board):
    row_border = " ----------- "
    print(row_border)
    for row in board:
        print(f"| {row[0]} | {row[1]} | {row[2]} |")
        print(row_border)


def welcome(board):
    print("Welcome to the'Unbeatable Noughts and Crosses'game!\n")
    print("The board layout is shown below:")
    draw_board(board)# displays the current state of the board .

def initialise_board(board):
    for row in range(3):
        board[row] = [" ", " ", " "]
    return board

def get_player_move(board):
    while True:
        try:
            player_move = int(input("Enter your move on the board [1-9]: ")) - 1 #allows move on the board
            if 0 <= player_move <= 8:
                col = 0 if player_move % 3 == 0 else (1 if player_move % 3 == 1 else 2)#calculates the coloumn. If 0=col1,1=col2,2=col3
                row = 0 if 0 <= player_move <=2 else (1 if 3 <= player_move <=5 else 2)#calculate the row. 1-3=0,4-6=1,7-9=2
                if board[row][col] != " ":
                    print("Position already occupied")
                    continue
                break
            raise ValueError("Number must be between 1 to 9")
        except ValueError:
            print("Enter a valid number only. Between 1 to 9.")
    return row, col

def choose_computer_move(board):
    clone_board = board.copy()
    row, col = 0,0

    #check if computer can win in the next move
    for i in range(3):
        for j in range(3):
            if clone_board[i][j] == " ":
                clone_board[i][j] = "O"
                if check_for_win(board, "O"):
                    row, col = i, j
                    return row, col
                clone_board[i][j] = " "

    #check if player can win in the next move, then block
    for i in range(3):
        for j in range(3):
            if clone_board[i][j] == " ":
                clone_board[i][j] = "X"
                if check_for_win(board, "X"):
                    row, col = i, j
                    return row, col
                clone_board[i][j] = " "

    if clone_board[1][1] == " ":
        row, col = 1, 1
        return row, col

    # check empty 4 corners
    for i in [0,2]:
        for j in [0,2]:
            if clone_board[i][j] == " ":
                row, col = i, j
                return row, col

    for i in range(3):
        for j in range(3):
            if clone_board[i][j] == " ":
                row, col = i, j
                return row, col


def check_for_win(board, mark):
    win_conditions = [
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]
    for win in win_conditions:    #checks the condition fir win and loops the list of win conditions
        cell0_r, cell0_c = win[0]
        cell1_r, cell1_c = win[1]
        cell2_r, cell2_c = win[2]
        if (
            board[cell0_r][cell0_c] == mark and #if match true=win false=no win
            board[cell1_r][cell1_c] == mark and
            board[cell2_r][cell2_c] == mark
        ):
            return True
    return False

def check_for_draw(board):#checks if the game has ended in a draw 
    for row in board:#loops through the board and checks if there is any empty cell in a row
        if row[0] == " " or row[1] == " " or row[2] == " ":
            return False#indicates game is not over
    return True# indicates the game has ended in a draw

def play_game(board):#function between a player and the computer
    board = initialise_board(board)
    draw_board(board)
    while True:
        row, col = get_player_move(board) #player's move is recorded and displayed using draw board
        board[row][col] = "X"
        draw_board(board)
        if check_for_win(board, "X"):
            return 1
        if check_for_draw(board):
            return 0
        row, col = choose_computer_move(board)#Computer's move is recorded and displayed using draw board
        board[row][col] = "O"
        draw_board(board)
        if check_for_win(board, "O"):
            return -1
        if check_for_draw(board):
            return 0

def menu():
    choice = ""
    while True:
        try:
            display_message = """Enter one of the following options: 
                        1 - play the game
                        2 - Save your score in the leaderboard
                        3 - Load and display the leaderboard
                        q - End the program"""
            print(display_message)
            choice = input("1, 2, 3, or q? ")
            if choice in ["1", "2", "3", "q", "Q"]:
                break
            raise ValueError("invalid input")
        except ValueError:
            print("user choice invalid")
    return choice

def load_scores(): #this function loads the scores from the leaderboard stored in the file leaderboard.txt
   
    leaders = {}
    try:
        with open("leaderboard.txt", "r", encoding="utf8") as file:
            file_content = file.read()
            leaders = json.loads(file_content)
    except IOError: #files doesnot exist
        print("Error reading leaderboard.txt")
    return leaders #return the dict leaders containing the scores from the leaderboard

def save_score(score): #saves the user's score to the leaderboard file named leaderboard
    leaders = load_scores()
    while True:
        try:
            user_name = input("Enter your name: ")
            if user_name == "":
                raise EOFError #if empty string is entered it shows error.
            with open("leaderboard.txt", "w", encoding="utf8") as file:#write mode using with
                leaders[user_name] = score
                file_content = json.dumps(leaders)#converts JSON string 
                file.write(file_content)#writes the JSON string to the file
                break
        except EOFError:
            print("invalid input")
    return


def display_leaderboard(leaders):#takes a dictionary of the leaders as input and displays the leaderboard to the console
    print("Leaderboard")
    for key, value in leaders.items(): 
        print(f"{key}: {value}")# for each item. the function uses and f string to print the leader's name and score

board1 = [ ['1','2','3'],
              ['4','5','6'],
              ['7','8','9']]
print(play_game(board1))

display_leaderboard(load_scores())
