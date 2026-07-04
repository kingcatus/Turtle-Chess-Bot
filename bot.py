import chess

# This table gives extra points for knights being in the center, and heavy penalties for being on the rim!
KNIGHT_HOME_MAP = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

# London players love controlling the center with pawns!
PAWN_HOME_MAP = [
      0,   0,   0,   0,   0,   0,   0,   0,
     50,  50,  50,  50,  50,  50,  50,  50,
     10,  10,  20,  30,  30,  20,  10,  10,
      5,   5,  10,  25,  25,  10,   5,   5,
      0,   0,   0,  20,  20,   0,   0,   0,
      5,  -5, -10,   0,   0, -10,  -5,   5,
      5,  10,  10, -20, -20,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0
]

def evaluate_position(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = piece_values[piece.piece_type]
            
            # --- POSITIONAL STRATEGY BONUS ---
            # Python-chess counts squares 0 to 63 from White's perspective (a1 to h8)
            position_bonus = 0
            if piece.piece_type == chess.KNIGHT:
                # Flip the map if it's black so it mirrors correctly
                sq_index = square if piece.color == chess.WHITE else chess.square_mirror(square)
                position_bonus = KNIGHT_HOME_MAP[sq_index]
            elif piece.piece_type == chess.PAWN:
                sq_index = square if piece.color == chess.WHITE else chess.square_mirror(square)
                position_bonus = PAWN_HOME_MAP[sq_index]

            # Add piece value + positional bonus
            total_worth = val + position_bonus

            if piece.color == chess.WHITE:
                score += total_worth
            else:
                score -= total_worth
    return score

def minimax(board, depth, is_maximizing):
    """
    Simulates the game back-and-forth up to a certain 'depth' (number of turns).
    """
    # Base case: if we hit our maximum depth or the game is over, evaluate the board
    if depth == 0 or board.is_game_over():
        return evaluate_position(board)

    if is_maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, evaluation)
        return min_eval

def choose_best_move(board, depth):
    """
    The main coordinator that calls minimax to find the absolute best move.
    """
    best_move = None
    
    # White wants to maximize, Black wants to minimize
    if board.turn == chess.WHITE:
        best_score = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move

    return best_move

# --- Let's test its new vision! ---
board = chess.Board()
print("--- NEW GAME STARTED ---")
print(board) 

# We tell it to look 3 moves deep (Depth 3)
SEARCH_DEPTH = 3
print(f"\nThinking... (Looking {SEARCH_DEPTH} moves ahead)")

bot_move = choose_best_move(board, SEARCH_DEPTH)
print(f"\nThe bot looks ahead and calmly chooses: {bot_move}")

board.push(bot_move)
print("\nThe board after the bot's move:")
print(board)