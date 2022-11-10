import math
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

import numpy as np
import pygame

import engine

win = tk.Tk()
win.withdraw()

#   Window Dimensions   #
WIDTH = 1050
HEIGHT = 700
WINDOW_SIZE = (WIDTH, HEIGHT)

#   Color Values    #
WHITE = (255, 255, 255)
LIGHTGREY = (170, 170, 170)
GREY = (85, 85, 85)
DARKGREY = (50, 50, 50)
DARKER_GREY = (35, 35, 35)
BLACK = (0, 0, 0)
RED = (230, 30, 30)
DARKRED = (150, 0, 0)
GREEN = (30, 230, 30)
DARKGREEN = (0, 190, 0)
BLUE = (30, 30, 122)
CYAN = (30, 230, 230)
GOLD = (225, 185, 0)
DARKGOLD = (165, 125, 0)

#   Component Colors   #
BOARD_LAYOUT_BACKGROUND = DARKGREY
SCREEN_BACKGROUND = LIGHTGREY
FOREGROUND = WHITE
CELL_BORDER_COLOR = BLUE
EMPTY_CELL_COLOR = GREY

#   Board Dimensions #
ROW_COUNT = 6
COLUMN_COUNT = 7

#   Component Dimensions    #
SQUARE_SIZE = 100
PIECE_RADIUS = int(SQUARE_SIZE / 2 - 5)

#   Board Coordinates   #
BOARD_BEGIN_X = 30
BOARD_BEGIN_Y = SQUARE_SIZE
BOARD_END_X = BOARD_BEGIN_X + (COLUMN_COUNT * SQUARE_SIZE)
BOARD_END_Y = BOARD_BEGIN_Y + (ROW_COUNT * SQUARE_SIZE)

BOARD_LAYOUT_END_X = BOARD_END_X + 2 * BOARD_BEGIN_X

#   Board Dimensions    #
BOARD_WIDTH = BOARD_BEGIN_X + COLUMN_COUNT * SQUARE_SIZE
BOARD_LENGTH = ROW_COUNT * SQUARE_SIZE

#   Player Variables    #
PIECE_COLORS = (GREY, RED, GREEN)
PLAYER1 = 1
PLAYER2 = 2
EMPTY_CELL = 0

#   Game-Dependent Global Variables    #
TURN = 1
GAME_OVER = False
PLAYER_SCORE = [0, 0, 0]
GAME_BOARD = [[]]
usePruning = True
screen = pygame.display.set_mode(WINDOW_SIZE)
GAME_MODE = -1

#   Game Modes  #
SINGLE_PLAYER = 1
TWO_PLAYERS = 2

# Developer Mode: facilitates debugging during GUI development
DEVMODE = False


class GameWindow:
    def setupGameWindow(self):
        """
        Initializes the all components in the frame
        """
        global GAME_BOARD
        GAME_BOARD = self.initGameBoard(EMPTY_CELL)
        pygame.display.set_caption('Smart Connect4 :)')
        self.refreshGameWindow()

    def refreshGameWindow(self):
        """
        Refreshes the screen and all the components
        """
        pygame.display.flip()
        refreshBackground()
        self.drawGameBoard()
        self.drawGameWindowButtons()
        self.drawGameWindowLabels()

    ######   Labels    ######

    def drawGameWindowLabels(self):
        """
        Draws all labels on the screen
        """
        titleFont = pygame.font.SysFont("Sans Serif", 40, False, True)
        mainLabel = titleFont.render("Smart Connect4", True, WHITE)
        screen.blit(mainLabel, (BOARD_LAYOUT_END_X + 20, 30))

        if not GAME_OVER:
            captionFont = pygame.font.SysFont("Arial", 15)
            player1ScoreCaption = captionFont.render("Player1", True, BLACK)
            player2ScoreCaption = captionFont.render("Player2", True, BLACK)
            screen.blit(player1ScoreCaption, (BOARD_LAYOUT_END_X + 48, 210))
            screen.blit(player2ScoreCaption, (BOARD_LAYOUT_END_X + 170, 210))

            depthFont = pygame.font.SysFont("Serif", 23 - len(str(engine.getDepth())))
            depthLabel = depthFont.render("k = " + str(engine.getDepth()), True, BLACK)
            screen.blit(depthLabel, (WIDTH - 100, 294))

            depthFont = pygame.font.SysFont("Arial", 16)
            depthLabel = depthFont.render("Use alpha-beta pruning", True, BLACK)
            screen.blit(depthLabel, (BOARD_LAYOUT_END_X + 65, 340))

        else:
            if PLAYER_SCORE[PLAYER1] == PLAYER_SCORE[PLAYER2]:
                verdict = 'DRAW :)'
            elif PLAYER_SCORE[PLAYER1] > PLAYER_SCORE[PLAYER2]:
                verdict = 'Player 1 Wins!'
            else:
                verdict = 'Player 2 Wins!'

            verdictFont = pygame.font.SysFont("Serif", 40)
            verdictLabel = verdictFont.render(verdict, True, GOLD)
            screen.blit(verdictLabel, (BOARD_BEGIN_X + BOARD_END_X / 3, BOARD_BEGIN_Y / 3))

        self.refreshScores()
        self.refreshStats()

    def refreshScores(self):
        """
        Refreshes the scoreboard
        """
        if GAME_OVER:
            scoreBoard_Y = BOARD_BEGIN_Y
        else:
            scoreBoard_Y = 120

        pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 9, scoreBoard_Y - 1, 117, 82), 0)
        player1ScoreSlot = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                            (BOARD_LAYOUT_END_X + 10, scoreBoard_Y, 115, 80))

        pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 134, scoreBoard_Y - 1, 117, 82), 0)
        player2ScoreSlot = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                            (BOARD_LAYOUT_END_X + 135, scoreBoard_Y, 115, 80))

        scoreFont = pygame.font.SysFont("Sans Serif", 80)
        player1ScoreCounter = scoreFont.render(str(PLAYER_SCORE[PLAYER1]), True, PIECE_COLORS[1])
        player2ScoreCounter = scoreFont.render(str(PLAYER_SCORE[PLAYER2]), True, PIECE_COLORS[2])

        player1ScoreLength = player2ScoreLength = 2.7
        if PLAYER_SCORE[PLAYER1] > 0:
            player1ScoreLength += math.log(PLAYER_SCORE[PLAYER1], 10)
        if PLAYER_SCORE[PLAYER2] > 0:
            player2ScoreLength += math.log(PLAYER_SCORE[PLAYER2], 10)

        screen.blit(player1ScoreCounter,
                    (player1ScoreSlot.x + player1ScoreSlot.width / player1ScoreLength, scoreBoard_Y + 15))
        screen.blit(player2ScoreCounter,
                    (player2ScoreSlot.x + player2ScoreSlot.width / player2ScoreLength, scoreBoard_Y + 15))

    def mouseOverMainLabel(self):
        return 30 <= pygame.mouse.get_pos()[1] <= 55 and 810 <= pygame.mouse.get_pos()[0] <= 1030

    def refreshStats(self):
        """
        Refreshes the analysis section
        """
        pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 9, 369, WIDTH - BOARD_LAYOUT_END_X - 18, 267), 0)
        pygame.draw.rect(screen, GREY, (BOARD_LAYOUT_END_X + 10, 370, WIDTH - BOARD_LAYOUT_END_X - 20, 265))

    ######   Buttons    ######

    def drawGameWindowButtons(self):
        """
        Draws all buttons on the screen
        """
        global showStatsButton, contributorsButton, modifyDepthButton, playAgainButton, pruningCheckbox
        contributorsButton = Button(
            screen, color=LIGHTGREY,
            x=BOARD_LAYOUT_END_X + 10, y=650,
            width=WIDTH - BOARD_LAYOUT_END_X - 20, height=30, text="Contributors")
        contributorsButton.draw(BLACK)

        if not GAME_OVER:
            modifyDepthButton = Button(
                screen, color=LIGHTGREY,
                x=BOARD_LAYOUT_END_X + 10, y=290,
                width=WIDTH - BOARD_LAYOUT_END_X - 120, height=30, text="Modify depth k")
            modifyDepthButton.draw(BLACK)

            pruningCheckbox = Button(
                screen, color=WHITE,
                x=BOARD_LAYOUT_END_X + 35, y=340,
                width=20, height=20, text="",
                gradCore=usePruning, coreLeftColor=DARKGOLD, coreRightColor=GOLD,
                gradOutline=True, outLeftColor=LIGHTGREY, outRightColor=GREY)

            self.togglePruningCheckbox(toggle=False)

            showStatsButton_Y = 250
        else:
            showStatsButton_Y = 330

            playAgainButton = Button(
                window=screen, color=GOLD, x=BOARD_LAYOUT_END_X + 10, y=BOARD_BEGIN_Y + 100,
                width=WIDTH - BOARD_LAYOUT_END_X - 20, height=120, text="Play Again")
            playAgainButton.draw()

        showStatsButton = Button(
            screen, color=LIGHTGREY,
            x=BOARD_LAYOUT_END_X + 10, y=showStatsButton_Y,
            width=WIDTH - BOARD_LAYOUT_END_X - 20, height=30, text="Show nerdy stats :D")
        showStatsButton.draw(BLACK)

    def togglePruningCheckbox(self, toggle=True):
        global usePruning
        if toggle:
            usePruning = pruningCheckbox.isChecked = pruningCheckbox.gradCore = not usePruning

        if usePruning:
            pruningCheckbox.draw(WHITE, outlineThickness=4)
        else:
            pruningCheckbox.draw(WHITE, outlineThickness=2)

    ######   Game Board  ######

    def initGameBoard(self, initialCellValue):
        """
        Initializes the game board with the value given.
        :param initialCellValue: Value of initial cell value
        :return: board list with all cells initialized to initialCellValue
        """
        global GAME_BOARD
        GAME_BOARD = np.full((ROW_COUNT, COLUMN_COUNT), initialCellValue)
        return GAME_BOARD

    def printGameBoard(self):
        """
        Prints the game board to the terminal
        """
        print('\n-\n' +
              str(GAME_BOARD) +
              '\n Player ' + str(TURN) + ' plays next')

    def drawGameBoard(self):
        """
        Draws the game board on the interface with the latest values in the board list
        """
        pygame.draw.rect(screen, BLACK, (0, 0, BOARD_LAYOUT_END_X, HEIGHT), 0)
        boardLayout = pygame.draw.rect(
            screen, BOARD_LAYOUT_BACKGROUND, (0, 0, BOARD_LAYOUT_END_X - 1, HEIGHT))
        gradientRect(screen, DARKER_GREY, DARKGREY, boardLayout)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                col = BOARD_BEGIN_X + (c * SQUARE_SIZE)
                row = BOARD_BEGIN_Y + (r * SQUARE_SIZE)
                piece = GAME_BOARD[r][c]
                pygame.draw.rect(
                    screen, CELL_BORDER_COLOR, (col, row, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(
                    screen, PIECE_COLORS[piece], (int(col + SQUARE_SIZE / 2), int(row + SQUARE_SIZE / 2)), PIECE_RADIUS)
        pygame.display.update()

    def hoverPieceOverSlot(self):
        """
        Hovers the piece over the game board with the corresponding player's piece color
        """
        boardLayout = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                       (0, BOARD_BEGIN_Y - SQUARE_SIZE, BOARD_WIDTH + SQUARE_SIZE / 2, SQUARE_SIZE))
        gradientRect(screen, DARKER_GREY, DARKGREY, boardLayout)
        posx = pygame.mouse.get_pos()[0]
        if BOARD_BEGIN_X < posx < BOARD_END_X:
            pygame.mouse.set_visible(False)
            pygame.draw.circle(screen, PIECE_COLORS[TURN], (posx, int(SQUARE_SIZE / 2)), PIECE_RADIUS)
        else:
            pygame.mouse.set_visible(True)

    def dropPiece(self, col, piece) -> tuple:
        """
        Drops the given piece in the next available cell in slot 'col'
        :param col: Column index where the piece will be dropped
        :param piece: Value of the piece to be put in array.
        :returns: tuple containing the row and column of piece position
        """
        row = self.getNextOpenRow(col)
        GAME_BOARD[row][col] = piece

        return row, col

    def hasEmptyCell(self, col) -> bool:
        """
        Checks if current slot has an empty cell. Assumes col is within array limits
        :param col: Column index representing the slot
        :return: True if slot has an empty cell. False otherwise.
        """
        return GAME_BOARD[0][col] == EMPTY_CELL

    def getNextOpenRow(self, col):
        """
        Gets the next available cell in the slot
        :param col: Column index
        :return: If exists, the row of the first available empty cell in the slot. None otherwise.
        """
        for r in range(ROW_COUNT - 1, -1, -1):
            if GAME_BOARD[r][col] == EMPTY_CELL:
                return r
        return None

    def boardIsFull(self) -> bool:
        """
        Checks if the board game is full
        :return: True if the board list has no empty slots, False otherwise.
        """
        for slot in range(COLUMN_COUNT):
            if self.hasEmptyCell(slot):
                return False
        return True

    def getBoardColumnFromPos(self, posx):
        """
        Get the index of the board column corresponding to the given position
        :param posx: Position in pixels
        :return: If within board bounds, the index of corresponding column, None otherwise
        """
        column = int(math.floor(posx / SQUARE_SIZE))
        if 0 <= column < COLUMN_COUNT:
            return column
        return None

    def buttonResponseToMouseEvent(self, event):
        """
        Handles button behaviour in response to mouse events influencing them
        """
        if event.type == pygame.MOUSEMOTION:
            if showStatsButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(showStatsButton, WHITE, BLACK)
            elif contributorsButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(contributorsButton, WHITE, BLACK)
            elif not GAME_OVER and modifyDepthButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(modifyDepthButton, WHITE, BLACK)
            elif not GAME_OVER and pruningCheckbox.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif GAME_OVER and playAgainButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(playAgainButton, WHITE, BLACK, True, WHITE, GOLD, 22)
            elif self.mouseOverMainLabel():
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                alterButtonAppearance(showStatsButton, LIGHTGREY, BLACK)
                alterButtonAppearance(contributorsButton, LIGHTGREY, BLACK)
                if not GAME_OVER:
                    alterButtonAppearance(modifyDepthButton, LIGHTGREY, BLACK)
                else:
                    alterButtonAppearance(playAgainButton, GOLD, BLACK)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if showStatsButton.isOver(event.pos):
                alterButtonAppearance(showStatsButton, CYAN, BLACK)
            elif contributorsButton.isOver(event.pos):
                alterButtonAppearance(contributorsButton, CYAN, BLACK)
            elif not GAME_OVER and modifyDepthButton.isOver(event.pos):
                alterButtonAppearance(modifyDepthButton, CYAN, BLACK)
            elif not GAME_OVER and pruningCheckbox.isOver(event.pos):
                self.togglePruningCheckbox()
            elif GAME_OVER and playAgainButton.isOver(event.pos):
                alterButtonAppearance(playAgainButton, GOLD, BLACK, True, GOLD, CYAN)
            elif self.mouseOverMainLabel():
                self.resetEverything()
                mainMenu.setupMainMenu()
                mainMenu.show()

        if event.type == pygame.MOUSEBUTTONUP:
            if showStatsButton.isOver(event.pos):
                alterButtonAppearance(showStatsButton, LIGHTGREY, BLACK)
            elif contributorsButton.isOver(event.pos):
                alterButtonAppearance(contributorsButton, LIGHTGREY, BLACK)
                self.showContributors()
            elif not GAME_OVER and modifyDepthButton.isOver(event.pos):
                alterButtonAppearance(modifyDepthButton, LIGHTGREY, BLACK)
                self.takeNewDepth()
            elif GAME_OVER and playAgainButton.isOver(event.pos):
                alterButtonAppearance(playAgainButton, GOLD, BLACK, True, WHITE, GOLD)
                self.resetEverything()

        if DEVMODE:
            pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 20, 70, WIDTH - BOARD_LAYOUT_END_X - 40, 40))
            pygame.mouse.set_visible(True)
            titleFont = pygame.font.SysFont("Sans Serif", 20, False, True)
            coordinates = titleFont.render(str(pygame.mouse.get_pos()), True, WHITE)
            screen.blit(coordinates, (BOARD_LAYOUT_END_X + 100, 80))

    def takeNewDepth(self):
        """
        Invoked at pressing modify depth button. Displays a simple dialog that takes input depth from user
        """
        temp = simpledialog.askinteger('Enter depth', 'Enter depth k')
        if temp is not None and temp > 0:
            engine.setDepth(temp)
        self.refreshGameWindow()

    def showContributors(self):
        """
        Invoked at pressing the contributors button. Displays a message box Containing names and IDs of contributors
        """
        messagebox.showinfo('Contributors', "6744   -   Adham Mohamed Aly\n"
                                            "6905   -   Mohamed Farid Abdelaziz\n"
                                            "7140   -   Yousef Ashraf Kotp\n")

    def gameSession(self):
        """
        Runs the game session
        """
        global GAME_OVER, TURN, GAME_BOARD
        while True:
            if not GAME_OVER:
                self.hoverPieceOverSlot()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                self.buttonResponseToMouseEvent(event)

                if not GAME_OVER and event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0] - BOARD_BEGIN_X
                    column = self.getBoardColumnFromPos(posx)

                    if column is not None:
                        if self.hasEmptyCell(column):
                            self.dropPiece(column, TURN)
                            self.computeScore()
                            switchTurn()
                            self.refreshGameWindow()

                            self.player2Play()
                            if self.boardIsFull():
                                GAME_OVER = True
                                pygame.mouse.set_visible(True)
                                self.refreshGameWindow()
                                break
                            self.printGameBoard()

    def player2Play(self):
        if GAME_MODE == SINGLE_PLAYER:
            self.computerPlay()
        elif GAME_MODE == TWO_PLAYERS:
            pass

    def computerPlay(self):
        global GAME_BOARD
        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                GAME_BOARD[i][j] -= 1

        flippedGameBoard = np.flip(m=GAME_BOARD, axis=0)
        numericState = engine.convertToNumber(flippedGameBoard)
        boardState = engine.nextMove(alphaBetaPruning=usePruning, state=numericState)
        flippedNewState = engine.convertToTwoDimensions(boardState)
        newState = np.flip(m=flippedNewState, axis=0)

        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                GAME_BOARD[i][j] += 1
                newState[i][j] += 1

        GAME_BOARD = newState
        # move = self.getNewMove(newState, GAME_BOARD)
        # self.dropPiece(move, TURN)
        self.computeScore()

        switchTurn()
        self.refreshGameWindow()

    def resetEverything(self):
        """
        Resets everything back to default values
        """
        global GAME_BOARD, PLAYER_SCORE, GAME_OVER, TURN
        PLAYER_SCORE = [0, 0, 0]
        GAME_OVER = False
        TURN = 1
        self.setupGameWindow()

    def getNewMove(self, newState, oldState) -> int:
        """
        :return: New move made by the AI
        """
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if newState[r][c] != oldState[r][c]:
                    return c

    def computeScore(self):
        """
        Computes every player's score and stores it in the global PLAYER_SCORES list
        :returns: values in PLAYER_SCORES list
        """
        global PLAYER_SCORE
        PLAYER_SCORE = [0, 0, 0]
        for r in range(ROW_COUNT):
            consecutive = 0
            for c in range(COLUMN_COUNT):
                consecutive += 1
                if c > 0 and GAME_BOARD[r][c] != GAME_BOARD[r][c - 1]:
                    consecutive = 1
                if consecutive >= 4:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        for c in range(COLUMN_COUNT):
            consecutive = 0
            for r in range(ROW_COUNT):
                consecutive += 1
                if r > 0 and GAME_BOARD[r][c] != GAME_BOARD[r - 1][c]:
                    consecutive = 1
                if consecutive >= 4:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                if GAME_BOARD[r][c] == GAME_BOARD[r + 1][c + 1] \
                        == GAME_BOARD[r + 2][c + 2] == GAME_BOARD[r + 3][c + 3]:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 1, 2, -1):
                if GAME_BOARD[r][c] == GAME_BOARD[r + 1][c - 1] \
                        == GAME_BOARD[r + 2][c - 2] == GAME_BOARD[r + 3][c - 3]:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        return PLAYER_SCORE

    def isWithinBounds(self, mat, r, c) -> bool:
        """
        :param mat: 2D matrix to check in
        :param r: current row
        :param c: current column
        :return: True if coordinates are within matrix bounds, False otherwise
        """
        return 0 <= r <= len(mat) and 0 <= c <= len(mat[0])


class MainMenu:
    def show(self):
        while GAME_MODE == -1:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                self.buttonResponseToMouseEvent(event)

        startGameSession()

    def setupMainMenu(self):
        """
        Initializes the all components in the frame
        """
        global GAME_MODE
        GAME_MODE = -1
        pygame.display.flip()
        pygame.display.set_caption('Smart Connect4 :) - Main Menu')
        self.refreshMainMenu()

    def refreshMainMenu(self):
        """
        Refreshes the screen and all the components
        """
        pygame.display.flip()
        refreshBackground(BLACK, GREY)
        self.drawMainMenuButtons()
        self.drawMainMenuLabels()

    def drawMainMenuButtons(self):
        global singlePlayerButton, multiPlayerButton
        singlePlayerButton = Button(
            window=screen, color=LIGHTGREY, x=WIDTH / 3, y=HEIGHT / 2.5, width=WIDTH / 3, height=HEIGHT / 5,
            gradCore=True, coreLeftColor=GREEN, coreRightColor=BLUE, text='PLAY AGAINST AI')

        multiPlayerButton = Button(
            window=screen, color=LIGHTGREY, x=WIDTH / 3, y=HEIGHT / 2.5 + HEIGHT / 4, width=WIDTH / 3,
            height=HEIGHT / 5,
            gradCore=True, coreLeftColor=GREEN, coreRightColor=BLUE, text='TWO-PLAYERS')

        singlePlayerButton.draw(BLACK, 2)
        multiPlayerButton.draw(BLACK, 2)

    def drawMainMenuLabels(self):
        titleFont = pygame.font.SysFont("Sans Serif", 65, False, True)
        mainLabel = titleFont.render("Welcome to Smart Connect4 :)", True, WHITE)
        screen.blit(mainLabel, (WIDTH / 5, HEIGHT / 5))

    def buttonResponseToMouseEvent(self, event):
        """
        Handles button behaviour in response to mouse events influencing them
        """
        if event.type == pygame.MOUSEMOTION:
            if singlePlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(singlePlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=WHITE, gradRightColor=BLUE)
            elif multiPlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(multiPlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=WHITE, gradRightColor=BLUE)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                alterButtonAppearance(singlePlayerButton, LIGHTGREY, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                alterButtonAppearance(multiPlayerButton, LIGHTGREY, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if singlePlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(singlePlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GOLD, gradRightColor=BLUE)
            elif multiPlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(multiPlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GOLD, gradRightColor=BLUE)

        if event.type == pygame.MOUSEBUTTONUP:
            global GAME_MODE
            if singlePlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(singlePlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                setGameMode(SINGLE_PLAYER)
            elif multiPlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(multiPlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                setGameMode(TWO_PLAYERS)


def setGameMode(mode):
    global GAME_MODE
    GAME_MODE = mode


class Button:
    def __init__(self, window, color, x, y, width, height, text='', isChecked=False, gradCore=False, coreLeftColor=None,
                 coreRightColor=None, gradOutline=False, outLeftColor=None, outRightColor=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.screen = window
        self.isChecked = isChecked
        self.gradCore = gradCore
        self.coreLeftColor = coreLeftColor
        self.coreRightColor = coreRightColor
        self.gradOutline = gradOutline
        self.outLeftColor = outLeftColor
        self.outRightColor = outRightColor

    def draw(self, outline=None, outlineThickness=2, font='comicsans', fontSize=15, ):
        """
        Draws the button on screen
        :param outline: Outline color
        :param font: Font Name
        :param fontSize: Font Size
        """
        if outline:
            rectOutline = pygame.draw.rect(self.screen, outline, (self.x, self.y,
                                                                  self.width, self.height), 0)
            if self.gradOutline:
                gradientRect(self.screen, self.outLeftColor, self.outRightColor, rectOutline)
        button = pygame.draw.rect(self.screen, self.color, (self.x + outlineThickness, self.y + outlineThickness,
                                                            self.width - 2 * outlineThickness,
                                                            self.height - 2 * outlineThickness), 0)
        if self.gradCore:
            gradientRect(self.screen, self.coreLeftColor, self.coreRightColor, button, self.text, font, fontSize)

        if self.text != '':
            font = pygame.font.SysFont(font, fontSize)
            text = font.render(self.text, True, (0, 0, 0))
            self.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return self, button

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def gradientRect(window, left_colour, right_colour, target_rect, text=None, font='comicsans', fontSize=15):
    """
    Draw a horizontal-gradient filled rectangle covering <target_rect>
    """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)

    if text:
        font = pygame.font.SysFont(font, fontSize)
        text = font.render(text, True, (0, 0, 0))
        window.blit(text, (
            target_rect.x + (target_rect.width / 2 - text.get_width() / 2),
            target_rect.y + (target_rect.height / 2 - text.get_height() / 2)))


def alterButtonAppearance(button, color, outline,
                          hasGradBackground=False, gradLeftColor=None, gradRightColor=None, fontSize=15):
    """
    Alter button appearance with given colors
    :param hasGradBackground: Flag which indicates if the button background should be a gradient
    """
    button.color = color
    thisButton, buttonRect = button.draw(outline)
    if hasGradBackground:
        gradientRect(screen, gradLeftColor, gradRightColor, buttonRect, thisButton.text, 'comicsans', fontSize)


def refreshBackground(leftColor=BLACK, rightColor=GREY):
    """
    Refreshes screen background
    """
    gradientRect(screen, leftColor, rightColor, pygame.draw.rect(screen, SCREEN_BACKGROUND, (0, 0, WIDTH, HEIGHT)))


def switchTurn():
    """
    Switch turns between player 1 and player 2
    """
    global TURN
    if TURN == 1:
        TURN = 2
    else:
        TURN = 1


def startGameSession():
    gameWindow = GameWindow()
    gameWindow.setupGameWindow()
    gameWindow.gameSession()


if __name__ == '__main__':
    pygame.init()
    mainMenu = MainMenu()
    mainMenu.setupMainMenu()
    mainMenu.show()
