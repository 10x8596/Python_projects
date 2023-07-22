import sys # to quit the application
import pygame
from constants import *
import numpy as np

# --------------------------PYGAME Setup--------------------------- #
# these first lines of code are always the same for pygame
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)

# --------------------------Classes-------------------------------- #
# Creating the console board
class Board:
    # init method
    def __init__(self): 
        # 3x3 Grid, 2-dimensional arrays of zeroes
        # [[0. 0. 0.]
        #  [0. 0. 0.]
        #  [0. 0. 0.]]
        self.squares = np.zeros((ROWS, COLS))
        # list of empty squares
        # self.empty_squares = self.squares # [squares] #######################---------
        # increment the number of squares that have been marked
        self.marked_squares = 0

    # when a player marks a square, that square will contain the number
    # of the player / ai. This will prevent the same square from being
    # selected / marked again by the player or more importantly the ai.
    def mark_squares(self, row, col, player):
        '''
        This function allows players to mark squares they click on
        and assigns that square with the player's number.
        '''
        self.squares[row][col] = player
        self.marked_squares += self.marked_squares
    # Checks if the square is empty
    def empty_square(self, row, col):
        '''
        This function checks if a square on the board is unmarked
        '''
        return self.squares[row][col] == 0
    # get number of empty squares for AI
    def get_empty_squares(self):
        '''
        This function returns the remaining squares on the board that can be marked
        as a list
        '''
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares
    # when the board is full (will help call tie function)
    def is_full(self):
        '''
        This function tells us when all the squares on the board have been filled
        '''
        return self.marked_squares == 9
    # Check if board is empty and/or not full
    def is_empty_not_full(self):
        '''
        This function tells us if the board is empty or all the squares have 
        not been marked yet.
        '''
        return self.marked_squares == 0 or self.marked_squares < 9
    
    def final_state(self):
        '''
            @return 0 if the game has not ended yet
            @return 1 if player wins
            @return 2 if AI wins
        This function checks the final state of the game board to determine the winner
        '''
        # vertical wins (loop through all the columns)
        for col in range(COLS):
            # if the column are not equal to 0, then there's no winner in that column
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        # horizontal wins (loop through all the rows)
        for row in range(ROWS):
            # if the rows are not equal to 0, then there's no winner in that row
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
        # descending diagonal win check
        for row in range(ROWS):
            for col in range(COLS):
                if row == col and (self.squares[row][col] != 0):
                    return self.squares[row][col]
        # ascending diagonal win check
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        # no win yet then return 0
        return 0

class Game:
    # init method (going to be called each time a Game object is created)
    # self represents a Game object (the class). Meaning to reference the Game
    # class directly, we use self 
    def __init__(self): 
        self.board = Board()
        # player1 = crosses and player2 (AI) = circles
        # Player attribute (shows the next player to mark a square)
        self.player = 1
        # AI attribute
        # self.ai = AI()
        # pvp or ai gamemode
        self.gamemode = 'ai'
        # if there is no winner or draw yet, game is still running
        self.game_running = True
        # call show_lines method in init 
        self.show_lines()

    def show_lines(self):
        '''
        This function draws the grid on the tictactoe board
        '''
        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), 
                         (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), 
                         (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), 
                        (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), 
                        (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)
    def next_player(self):
        '''
        This function switches turns between players
        '''
        self.player = self.player % 2 + 1
    def draw_figure(self, row, col):
        '''
        This function draws a figure ( x and o ) when the player clicks on board
        take row and col coordinate:
        # [[(0,0) (1,0) (2,0)]
        #  [(0,1) (1,1) (2,1)]
        #  [(0,2) (1,2) (2,2)]]
        into center coordinates (row(pos), col(pos)):
        [[(100,100), (300,100), (500, 100)]
         [(100,300), (300,300), (500, 300)]
         [(100,500), (300,500), (500, 500)]]
        '''
        if self.player == 1:
            # draw a cross
            # descending line
            start_desc = (row * SQUARE_SIZE + OFFSET, col * SQUARE_SIZE + OFFSET)
            end_desc   = (row * SQUARE_SIZE + SQUARE_SIZE - OFFSET,
                          col * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            # ascending line
            start_asc = (row * SQUARE_SIZE + OFFSET, 
                         col * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (row * SQUARE_SIZE + SQUARE_SIZE - OFFSET, 
                       col * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSSES_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSSES_WIDTH)
        elif self.player == 2:
            # draw a circle
            center = (row * SQUARE_SIZE + SQUARE_SIZE // 2, 
                      col * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)