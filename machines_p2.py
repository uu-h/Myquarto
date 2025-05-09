# import numpy as np
# import random
# from itertools import product

# import time

# class P2():
#     def __init__(self, board, available_pieces):
#         self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]  # All 16 pieces
#         self.board = board # Include piece indices. 0:empty / 1~16:piece
#         self.available_pieces = available_pieces # Currently available pieces in a tuple type (e.g. (1, 0, 1, 0))
#     #기존 코드 
#     def select_piece(self):
#         # Make your own algorithm here

#         time.sleep(0.5) # Check time consumption (Delete when you make your algorithm)

#         return random.choice(self.available_pieces)

#     def place_piece(self, selected_piece):
#         # selected_piece: The selected piece that you have to place on the board (e.g. (1, 0, 1, 0)).
        
#         # Available locations to place the piece
#         available_locs = [(row, col) for row, col in product(range(4), range(4)) if self.board[row][col]==0]

#         # Make your own algorithm here

#         time.sleep(1) # Check time consumption (Delete when you make your algorithm)
        
#         return random.choice(available_locs)

import numpy as np
from itertools import product

class P2():
    def __init__(self, board, available_pieces):
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]
        self.board = board
        self.available_pieces = available_pieces

    def select_piece(self):
        # 상대가 잘 못 쓰도록 → 속성 다양성이 높은 말 위주로 줌
        best_piece = None
        worst_score = float('inf')

        for piece in self.available_pieces:
            diversity = len(set(piece))
            score = diversity  # 속성이 고르게 섞일수록 낮은 점수
            if score < worst_score:
                worst_score = score
                best_piece = piece

        return best_piece

    def place_piece(self, selected_piece):
        best_score = -float('inf')
        best_pos = None
        available_locs = [(r, c) for r, c in product(range(4), range(4)) if self.board[r][c] == 0]

        for (r, c) in available_locs:
            new_board = self.board.copy()
            piece_idx = self.pieces.index(selected_piece) + 1
            new_board[r][c] = piece_idx
            score = minimax(new_board, depth=2, is_max=False,
                            selected_piece=None,
                            pieces=self.pieces,
                            available_pieces=[p for p in self.available_pieces if p != selected_piece],
                            alpha=-float('inf'),
                            beta=float('inf'))
            if score > best_score:
                best_score = score
                best_pos = (r, c)

        return best_pos


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
                        score += 10  # P2는 좀 더 공격적
    return score


def evaluate_line(line, pieces):
    if 0 in line:
        return 0
    attrs = [pieces[idx - 1] for idx in line]
    score = 0
    for i in range(4):
        values = [attr[i] for attr in attrs]
        if len(set(values)) == 1:
            score += 30
        elif len(set(values)) == 2:
            score += 7
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

    for r in range(3):
        for c in range(3):
            subgrid = [board[r+i][c+j] for i in range(2) for j in range(2)]
            if 0 not in subgrid:
                attrs = [pieces[idx - 1] for idx in subgrid]
                for i in range(4):
                    if len(set(attr[i] for attr in attrs)) == 1:
                        return True
    return False
