
import numpy as np
import random
from itertools import product

class P1():
    def __init__(self, board, available_pieces):
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]
        self.board = board
        self.available_pieces = available_pieces

    def select_piece(self):
        worst_score = float('inf')
        candidates = []
        available_locs = [(r, c) for r, c in product(range(4), range(4)) if self.board[r][c] == 0]

        for piece in self.available_pieces:
            max_score = -float('inf')
            for (r, c) in available_locs:
                new_board = self.board.copy()
                piece_idx = self.pieces.index(piece) + 1
                new_board[r][c] = piece_idx
                score = minimax(new_board, 2, True, None, self.pieces, [p for p in self.available_pieces if p != piece], -float('inf'), float('inf'))
                max_score = max(max_score, score)

            if max_score < worst_score:
                worst_score = max_score
                candidates = [piece]
            elif max_score == worst_score:
                candidates.append(piece)

        return random.choice(candidates)

    def place_piece(self, selected_piece):
        best_score = -float('inf')
        candidates = []
        available_locs = [(r, c) for r, c in product(range(4), range(4)) if self.board[r][c] == 0]

        for (r, c) in available_locs:
            new_board = self.board.copy()
            piece_idx = self.pieces.index(selected_piece) + 1
            new_board[r][c] = piece_idx
            score = minimax(new_board, 2, False, None, self.pieces, [p for p in self.available_pieces if p != selected_piece], -float('inf'), float('inf'))

            if score > best_score:
                best_score = score
                candidates = [(r, c)]
            elif score == best_score:
                candidates.append((r, c))

        return random.choice(candidates)

def minimax(board, depth, is_max, selected_piece, pieces, available_pieces, alpha, beta):
    if check_win(board, pieces):
        return 1000 if not is_max else -1000
    if depth == 0 or len(available_pieces) == 0:
        return evaluate_board(board, pieces)

    available_locs = [(r, c) for r, c in product(range(4), range(4)) if board[r][c] == 0]

    if is_max:
        value = -float('inf')
        for (r, c) in available_locs:
            for piece in available_pieces:
                new_board = board.copy()
                piece_idx = pieces.index(piece) + 1
                new_board[r][c] = piece_idx
                remaining = [p for p in available_pieces if p != piece]
                value = max(value, minimax(new_board, depth - 1, False, None, pieces, remaining, alpha, beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        return value
    else:
        value = float('inf')
        for (r, c) in available_locs:
            for piece in available_pieces:
                new_board = board.copy()
                piece_idx = pieces.index(piece) + 1
                new_board[r][c] = piece_idx
                remaining = [p for p in available_pieces if p != piece]
                value = min(value, minimax(new_board, depth - 1, True, None, pieces, remaining, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return value

def evaluate_board(board, pieces):
    score = 0
    for i in range(4):
        score += evaluate_line([board[i][j] for j in range(4)], pieces)
        score += evaluate_line([board[j][i] for j in range(4)], pieces)
    score += evaluate_line([board[i][i] for i in range(4)], pieces)
    score += evaluate_line([board[i][3 - i] for i in range(4)], pieces)
    for r in range(3):
        for c in range(3):
            subgrid = [board[r+i][c+j] for i in range(2) for j in range(2)]
            if 0 not in subgrid:
                attrs = [pieces[idx - 1] for idx in subgrid]
                for i in range(4):
                    if len(set(attr[i] for attr in attrs)) == 1:
                        score += 5
    return score

def evaluate_line(line, pieces):
    if 0 in line:
        return 0
    attrs = [pieces[idx - 1] for idx in line]
    score = 0
    for i in range(4):
        values = [attr[i] for attr in attrs]
        if len(set(values)) == 1:
            score += 20
        elif len(set(values)) == 2:
            score += 5
    return score

def check_win(board, pieces):
    def check_line(line):
        if 0 in line:
            return False
        attrs = [pieces[idx - 1] for idx in line]
        for i in range(4):
            if len(set(attr[i] for attr in attrs)) == 1:
                return True
        return False

    for i in range(4):
        if check_line([board[i][j] for j in range(4)]): return True
        if check_line([board[j][i] for j in range(4)]): return True
    if check_line([board[i][i] for i in range(4)]): return True
    if check_line([board[i][3 - i] for i in range(4)]): return True
    return False
