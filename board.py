from piece import Bishop
from piece import King
from piece import Rook
from piece import Pawn
from piece import Queen
from piece import Knight
import time
import pygame


class Board:
    _rect = (113, 113, 525, 525)
    _startX = _rect[0]
    _startY = _rect[1]

    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols

        self._ready = False

        self._last = None

        self._copy = True

        self._board = [[0 for x in range(8)] for _ in range(rows)]

        self._board[0][0] = Rook(0, 0, "b")
        self._board[0][1] = Knight(0, 1, "b")
        self._board[0][2] = Bishop(0, 2, "b")
        self._board[0][3] = Queen(0, 3, "b")
        self._board[0][4] = King(0, 4, "b")
        self._board[0][5] = Bishop(0, 5, "b")
        self._board[0][6] = Knight(0, 6, "b")
        self._board[0][7] = Rook(0, 7, "b")

        self._board[1][0] = Pawn(1, 0, "b")
        self._board[1][1] = Pawn(1, 1, "b")
        self._board[1][2] = Pawn(1, 2, "b")
        self._board[1][3] = Pawn(1, 3, "b")
        self._board[1][4] = Pawn(1, 4, "b")
        self._board[1][5] = Pawn(1, 5, "b")
        self._board[1][6] = Pawn(1, 6, "b")
        self._board[1][7] = Pawn(1, 7, "b")

        self._board[7][0] = Rook(7, 0, "w")
        self._board[7][1] = Knight(7, 1, "w")
        self._board[7][2] = Bishop(7, 2, "w")
        self._board[7][3] = Queen(7, 3, "w")
        self._board[7][4] = King(7, 4, "w")
        self._board[7][5] = Bishop(7, 5, "w")
        self._board[7][6] = Knight(7, 6, "w")
        self._board[7][7] = Rook(7, 7, "w")

        self._board[6][0] = Pawn(6, 0, "w")
        self._board[6][1] = Pawn(6, 1, "w")
        self._board[6][2] = Pawn(6, 2, "w")
        self._board[6][3] = Pawn(6, 3, "w")
        self._board[6][4] = Pawn(6, 4, "w")
        self._board[6][5] = Pawn(6, 5, "w")
        self._board[6][6] = Pawn(6, 6, "w")
        self._board[6][7] = Pawn(6, 7, "w")

        self._p1Name = "Player 1"
        self._p2Name = "Player 2"

        self._turn = "w"

        self._time1 = 900
        self._time2 = 900

        self._storedTime1 = 0
        self._storedTime2 = 0

        self._winner = None

        self._startTime = time.time()

    def update_moves(self):
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    self._board[i][j].update_valid_moves(self._board)

    def draw(self, win, color):
        if self._last and color == self.turn:
            y, x = self._last[0]
            y1, x1 = self._last[1]

            xx = (4 - x) +round(self._startX + (x * self._rect[2] / 8))
            yy = 3 + round(self._startY + (y * self._rect[3] / 8))
            pygame.draw.circle(win, (0,0,255), (xx+32, yy+30), 34, 4)
            xx1 = (4 - x) + round(self._startX + (x1 * self._rect[2] / 8))
            yy1 = 3+ round(self._startY + (y1 * self._rect[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)

        s = None
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    self._board[i][j].draw(win, color)
                    if self._board[i][j].isSelected:
                        s = (i, j)


    def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    if self._board[i][j].color != color:
                        for move in self._board[i][j].move_list:
                            danger_moves.append(move)

        return danger_moves

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    if self._board[i][j].king and self._board[i][j].color == color:
                        king_pos = (j, i)

        if king_pos in danger_moves:
            return True

        return False

    def select(self, col, row, color):
        changed = False
        prev = (-1, -1)
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    if self._board[i][j].selected:
                        prev = (i, j)

        # if piece
        if self._board[row][col] == 0 and prev!=(-1,-1):
            moves = self._board[prev[0]][prev[1]].move_list
            if (col, row) in moves:
                changed = self.move(prev, (row, col), color)

        else:
            if prev == (-1,-1):
                self.reset_selected()
                if self._board[row][col] != 0:
                    self._board[row][col].selected = True
            else:
                if self._board[prev[0]][prev[1]].color != self._board[row][col].color:
                    moves = self._board[prev[0]][prev[1]].move_list
                    if (col, row) in moves:
                        changed = self.move(prev, (row, col), color)

                    if self._board[row][col].color == color:
                        self._board[row][col].selected = True

                else:
                    if self._board[row][col].color == color:
                        #castling
                        self.reset_selected()
                        if self._board[prev[0]][prev[1]].moved == False and self._board[prev[0]][prev[1]].rook and self._board[row][col].king and col != prev[1] and prev!=(-1,-1):
                            castle = True
                            if prev[1] < col:
                                for j in range(prev[1]+1, col):
                                    if self._board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 3), color)
                                    changed = self.move((row,col), (row, 2), color)
                                if not changed:
                                    self._board[row][col].selected = True

                            else:
                                for j in range(col+1,prev[1]):
                                    if self._board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed = self.move(prev, (row, 6), color)
                                    changed = self.move((row,col), (row, 5), color)
                                if not changed:
                                    self._board[row][col].selected = True
                            
                        else:
                            self._board[row][col].selected = True

        if changed:
            if self.turn == "w":
                self.turn = "b"
                self.reset_selected()
            else:
                self.turn = "w"
                self.reset_selected()

    def reset_selected(self):
        for i in range(self._rows):
            for j in range(self._cols):
                if self._board[i][j] != 0:
                    self._board[i][j].selected = False

    def check_mate(self, color):
        '''if self.is_checked(color):
            king = None
            for i in range(self._rows):
                for j in range(self._cols):
                    if self._board[i][j] != 0:
                        if self._board[i][j].king and self._board[i][j].color == color:
                            king = self._board[i][j]
            if king is not None:
                valid_moves = king.valid_moves(self._board)

                danger_moves = self.get_danger_moves(color)

                danger_count = 0

                for move in valid_moves:
                    if move in danger_moves:
                        danger_count += 1
                return danger_count == len(valid_moves)'''

        return False

    def move(self, start, end, color):
        checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self._board[:]
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False

        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self._board = nBoard

        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            changed = False
            nBoard = self._board[:]
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True

            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self._board = nBoard
        else:
            self.reset_selected()

        self.update_moves()
        if changed:
            self._last = [start, end]
            if self.turn == "w":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed



