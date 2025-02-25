from piece import Bishop
from piece import King
from piece import Rook
from piece import Pawn
from piece import Queen
from piece import Knight
import time
import pygame


class Board:
    __rect = (113, 113, 525, 525)
    __startX = __rect[0]
    __startY = __rect[1]

    def ____init____(self, rows, cols):
        self.__rows = rows
        self.__cols = cols

        self.__ready = False

        self.__last = None

        self.__copy = True

        self.__board = [[0 for x in range(8)] for __ in range(rows)]

        self.__board[0][0] = Rook(0, 0, "b")
        self.__board[0][1] = Knight(0, 1, "b")
        self.__board[0][2] = Bishop(0, 2, "b")
        self.__board[0][3] = Queen(0, 3, "b")
        self.__board[0][4] = King(0, 4, "b")
        self.__board[0][5] = Bishop(0, 5, "b")
        self.__board[0][6] = Knight(0, 6, "b")
        self.__board[0][7] = Rook(0, 7, "b")

        self.__board[1][0] = Pawn(1, 0, "b")
        self.__board[1][1] = Pawn(1, 1, "b")
        self.__board[1][2] = Pawn(1, 2, "b")
        self.__board[1][3] = Pawn(1, 3, "b")
        self.__board[1][4] = Pawn(1, 4, "b")
        self.__board[1][5] = Pawn(1, 5, "b")
        self.__board[1][6] = Pawn(1, 6, "b")
        self.__board[1][7] = Pawn(1, 7, "b")

        self.__board[7][0] = Rook(7, 0, "w")
        self.__board[7][1] = Knight(7, 1, "w")
        self.__board[7][2] = Bishop(7, 2, "w")
        self.__board[7][3] = Queen(7, 3, "w")
        self.__board[7][4] = King(7, 4, "w")
        self.__board[7][5] = Bishop(7, 5, "w")
        self.__board[7][6] = Knight(7, 6, "w")
        self.__board[7][7] = Rook(7, 7, "w")

        self.__board[6][0] = Pawn(6, 0, "w")
        self.__board[6][1] = Pawn(6, 1, "w")
        self.__board[6][2] = Pawn(6, 2, "w")
        self.__board[6][3] = Pawn(6, 3, "w")
        self.__board[6][4] = Pawn(6, 4, "w")
        self.__board[6][5] = Pawn(6, 5, "w")
        self.__board[6][6] = Pawn(6, 6, "w")
        self.__board[6][7] = Pawn(6, 7, "w")

        self.__p1Name = "Player 1"
        self.__p2Name = "Player 2"

        self.__turn = "w"

        self.__time1 = 900
        self.__time2 = 900

        self.__storedTime1 = 0
        self.__storedTime2 = 0

        self.__winner = None

        self.__startTime = time.time()

    def update__moves(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__board[i][j] != 0:
                    self.__board[i][j].update__valid__moves(self.__board)

    def draw(self, win, color):
        if self.__last and color == self.turn:
            y, x = self.__last[0]
            y1, x1 = self.__last[1]

            xx = (4 - x) +round(self.__startX + (x * self.__rect[2] / 8))
            yy = 3 + round(self.__startY + (y * self.__rect[3] / 8))
            pygame.draw.circle(win, (0,0,255), (xx+32, yy+30), 34, 4)
            xx1 = (4 - x) + round(self.__startX + (x1 * self.__rect[2] / 8))
            yy1 = 3+ round(self.__startY + (y1 * self.__rect[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)

        s = None
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__board[i][j] != 0:
                    self.__board[i][j].draw(win, color)
                    if self.__board[i][j].isSelected:
                        s = (i, j)


    def get__danger__moves(self, color):
        danger__moves = []
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__board[i][j] != 0:
                    if self.__board[i][j].color != color:
                        for move in self.__board[i][j].move__list:
                            danger__moves.append(move)

        return danger__moves

    def is__checked(self, color):
        self.update__moves()
        danger__moves = self.get__danger__moves(color)
        king__pos = (-1, -1)
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__board[i][j] != 0:
                    if self.__board[i][j].king and self.__board[i][j].color == color:
                        king__pos = (j, i)

        if king__pos in danger__moves:
            return True

        return False

    def select(self, col, row, color):
        changed = False
        prev = (-1, -1)
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__board[i][j] != 0:
                    if self.__board[i][j].selected:
                        prev = (i, j)

        # if piece
        if self.__board[row][col] == 0 and prev!=(-1,-1):
            moves = self.__board[prev[0]][prev[1]].move__list
            if (col, row) in moves:
                changed = self.move(prev, (row, col), color)

        else:
            if prev == (-1,-1):
                self.reset__selected()
                if self.__board[row][col] != 0:
                    self.__board[row][col].selected = True
            else:
                if self.__board[prev[0]][prev[1]].color != self.__board[row][col].color:
                    moves = self.__board[prev[0]][prev[1]].move__list
                    if (col, row) in moves:
                        changed = self.move(prev, (row, col), color)

                    if self.__board[row][col].color == color:
                        self.__board[row][col].selected = True

                else:
                    if self.__board[row][col].color == color:
                        #castling
                        self.reset__selected()
                        if self.__board[prev[0]][prev[1]].moved == False and self.__board[prev[0]][prev[1]].rook and self.__board[row][col].king and col != prev[1] and prev!=(-1,-1):
                            castle = True
                            if prev[1] < col:
                                for j in range(prev[1]+1, col):
                                    if self.__board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 3), color)
                                    changed = self.move((row,col), (row, 2), color)
                                if not changed:
                                    self.__board[row][col].selected = True

                            else:
                                for j in range(col+1,prev[1]):
                                    if self.__board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 6), color)
                                    changed = self.move((row,col), (row, 5), color)
                                if not changed:
                                    self.__board[row][col].selected = True
                            
                        else:
                            self.__board[row][col].selected = True

        if changed:
            if self.turn == "w":
                self.turn = "b"
                self.reset__selected()
            else:
                self.turn = "w"
                self.reset__selected()

    def reset__selected(self):
        for i in range(self.__rows):
            for j in range(self.__cols):
                if self.__board[i][j] != 0:
                    self.__board[i][j].selected = False

    def check__mate(self, color):
        '''if self.is__checked(color):
            king = None
            for i in range(self.__rows):
                for j in range(self.__cols):
                    if self.__board[i][j] != 0:
                        if self.__board[i][j].king and self.__board[i][j].color == color:
                            king = self.__board[i][j]
            if king is not None:
                valid__moves = king.valid__moves(self.__board)

                danger__moves = self.get__danger__moves(color)

                danger__count = 0

                for move in valid__moves:
                    if move in danger__moves:
                        danger__count += 1
                return danger__count == len(valid__moves)'''

        return False

    def move(self, start, end, color):
        checkedBefore = self.is__checked(color)
        changed = True
        nBoard = self.__board[:]
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False

        nBoard[start[0]][start[1]].change__pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.__board = nBoard

        if self.is__checked(color) or (checkedBefore and self.is__checked(color)):
            changed = False
            nBoard = self.__board[:]
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True

            nBoard[end[0]][end[1]].change__pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.__board = nBoard
        else:
            self.reset__selected()

        self.update__moves()
        if changed:
            self.__last = [start, end]
            if self.turn == "w":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed



