import numpy as np
import random
from itertools import product
import time

class P2():
    def __init__(self, board, available_pieces):
        self.board = board
        self.available_pieces = available_pieces
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]

    def evaluate_board(self, board):
        def check_line(line):
            if 0 in line:
                return 0
            characteristics = np.array([self.pieces[piece_idx - 1] for piece_idx in line])
            for i in range(4):
                if len(set(characteristics[:, i])) == 1:
                    return 100
            return 0

        score = 0
        for i in range(4):
            score += check_line([board[i][j] for j in range(4)])
            score += check_line([board[j][i] for j in range(4)])
        score += check_line([board[i][i] for i in range(4)])
        score += check_line([board[i][3 - i] for i in range(4)])
        return score

    def select_piece(self):
        start_time = time.time()
        # 상대방이 승리할 확률이 높은 조각을 제거하는 방향으로 선택
        max_opponent_risk = -1
        selected = random.choice(self.available_pieces)
        empty_locs = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]

        for piece in self.available_pieces:
            risk_score = 0
            for r, c in empty_locs:
                temp_board = self.board.copy()
                temp_board[r][c] = self.pieces.index(piece) + 1
                score = self.evaluate_board(temp_board)
                risk_score = max(risk_score, score)
            if risk_score > max_opponent_risk:
                max_opponent_risk = risk_score
                selected = piece

        end_time = time.time()
        print(f"[P2 SELECT] Time: {end_time - start_time:.3f}s | Given Piece: {selected} | Risk: {max_opponent_risk}")
        return selected

    def place_piece(self, selected_piece):
        start_time = time.time()
        best_score = -float('inf')
        best_move = None
        empty_locs = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        selected_index = self.pieces.index(selected_piece) + 1

        for r, c in empty_locs:
            temp_board = self.board.copy()
            temp_board[r][c] = selected_index
            score = self.evaluate_board(temp_board)
            if score > best_score:
                best_score = score
                best_move = (r, c)

        if not best_move:
            best_move = random.choice(empty_locs)

        end_time = time.time()
        print(f"[P2 PLACE] Time: {end_time - start_time:.3f}s | Placed at: {best_move} | Score: {best_score} | Piece: {selected_piece}")
        return best_move

    