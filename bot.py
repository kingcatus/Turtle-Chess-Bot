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

def minimax(board, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    Cuts off calculation branches that are guaranteed to be worse.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_position(board)

    if is_maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # Beta cutoff: Stop searching this branch
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Alpha cutoff: Stop searching this branch
        return min_eval

def choose_best_move(board, depth):
    """
    Coordinates the main search using initialized alpha and beta constraints.
    """
    best_move = None
    alpha = -float('inf')
    beta = float('inf')
    
    if board.turn == chess.WHITE:
        best_score = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
    else:
        best_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)

    return best_move

# --- Let's test its new optimized vision! ---
board = chess.Board()
print("--- NEW GAME STARTED ---")
print(board) 

# Now we can comfortably look 4 or 5 moves deep without our machine freezing!
SEARCH_DEPTH = 4
print(f"\nThinking deeply... (Looking {SEARCH_DEPTH} moves ahead with Alpha-Beta Pruning)")

bot_move = choose_best_move(board, SEARCH_DEPTH)
print(f"\nThe bot looks ahead and calmly chooses: {bot_move}")

board.push(bot_move)
print("\nThe board after the bot's move:")
print(board)