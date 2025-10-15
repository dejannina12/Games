#!/usr/bin/env python3
"""
Console Chess Game (human vs AI) using python-chess
---------------------------------------------------
Features
- Full legal chess rules via python-chess (castling, en passant, promotion, checkmate/stalemate detection)
- Play as White or Black
- Adjustable AI depth (1-4 plies by default)
- Input moves in SAN (e.g., Nf3, exd5, O-O) or UCI (e2e4). Promotion like e7e8q or e8=Q
- Board printed after every move with unicode pieces

Requirements
- Python 3.9+
- Install dependency:  pip install python-chess

Run
  python3 python_chess_game.py

Tips
- Type 'help' during the game for commands
- Type 'moves' to list all legal moves for the side to move
- Type 'fen' to copy the current FEN
- Type 'undo' to take back a half-move
- Type 'quit' to exit

Testing
- Run quick non-interactive tests:  python3 python_chess_game.py --test
"""
from __future__ import annotations
import sys
import time
from dataclasses import dataclass

try:
    import chess
    import chess.polyglot
except Exception as e:
    print("This program requires the 'python-chess' library.\nInstall with: pip install python-chess")
    sys.exit(1)

# ------------------------------ Rendering -----------------------------------
UNICODE_PIECES = {
    chess.PAWN:   ("♙", "♟"),
    chess.KNIGHT: ("♘", "♞"),
    chess.BISHOP: ("♗", "♝"),
    chess.ROOK:   ("♖", "♜"),
    chess.QUEEN:  ("♕", "♛"),
    chess.KING:   ("♔", "♚"),
}

FILES = "abcdefgh"
RANKS = "12345678"

def print_board(board: chess.Board) -> None:
    def piece_symbol(square: int) -> str:
        piece = board.piece_at(square)
        if not piece:
            return "."
        sym_w, sym_b = UNICODE_PIECES[piece.piece_type]
        return sym_w if piece.color == chess.WHITE else sym_b

    print("\n   a b c d e f g h")
    print("  ┌────────────────┐")
    for r in range(7, -1, -1):
        row_syms = []
        for f in range(8):
            sq = chess.square(f, r)
            row_syms.append(piece_symbol(sq))
        print(f"{r+1} │ {' '.join(row_syms)} │ {r+1}")
    print("  └────────────────┘")
    print("   a b c d e f g h\n")
    print(f"Side to move: {'White' if board.turn == chess.WHITE else 'Black'}")
    if board.is_check():
        print("Check!")

# ------------------------------ Evaluation ----------------------------------
# Simple material-only evaluation with piece-square tables for a tiny bit of shape.
# Scores are from White's perspective. Positive is good for White.
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

# PSTs are mirrored for Black by python-chess when using square_mirror.
# These are light-touch and not crucial; they just help the AI make non-silly choices.
PST_PAWN = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

PST_KNIGHT = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

PST_BISHOP = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

PST_ROOK = [
     0,  0,  5, 10, 10,  5,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     5, 10, 10, 10, 10, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

PST_QUEEN = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0,  0,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

PST_KING_MG = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20,
]

PST_KING_EG = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50,
]

PSTS = {
    chess.PAWN: PST_PAWN,
    chess.KNIGHT: PST_KNIGHT,
    chess.BISHOP: PST_BISHOP,
    chess.ROOK: PST_ROOK,
    chess.QUEEN: PST_QUEEN,
}

@dataclass
class EvalConfig:
    mg_phase_weight: int = 24  # material threshold to switch MG/EG for king PST

EVAL_CFG = EvalConfig()


def evaluate(board: chess.Board) -> int:
    """Return a centipawn evaluation from White's perspective."""
    if board.is_game_over():
        if board.is_checkmate():
            return -99999 if board.turn == chess.WHITE else 99999
        return 0  # draw

    score = 0

    # Material + PSTs
    white_material = 0
    black_material = 0

    for piece_type in PIECE_VALUES.keys():
        for sq in board.pieces(piece_type, chess.WHITE):
            white_material += PIECE_VALUES[piece_type]
            if piece_type in PSTS:
                score += PSTS[piece_type][sq]
        for sq in board.pieces(piece_type, chess.BLACK):
            black_material += PIECE_VALUES[piece_type]
            if piece_type in PSTS:
                score -= PSTS[piece_type][chess.square_mirror(sq)]

    score += (white_material - black_material)

    # Phase for king tables: crude based on total material
    phase = (white_material + black_material) // 100
    if phase >= EVAL_CFG.mg_phase_weight:
        # middlegame
        for sq in board.pieces(chess.KING, chess.WHITE):
            score += PST_KING_MG[sq]
        for sq in board.pieces(chess.KING, chess.BLACK):
            score -= PST_KING_MG[chess.square_mirror(sq)]
    else:
        # endgame
        for sq in board.pieces(chess.KING, chess.WHITE):
            score += PST_KING_EG[sq]
        for sq in board.pieces(chess.KING, chess.BLACK):
            score -= PST_KING_EG[chess.square_mirror(sq)]

    # Mobility (very light)
    score += 2 * len(list(board.legal_moves)) if board.turn == chess.WHITE else -2 * len(list(board.legal_moves))

    return score

# ------------------------------ Search --------------------------------------

def search_best_move(board: chess.Board, max_depth: int = 3, use_book: bool = True) -> chess.Move:
    # Try opening book first (if available). We'll use python-chess's simple polyglot with the default book if found.
    if use_book:
        try:
            # Attempt to use any available polyglot book shipped by user; silently ignore if missing.
            with chess.polyglot.open_reader(chess.polyglot.find_book()) as reader:  # type: ignore[arg-type]
                entry = reader.find(board)
                if entry:
                    return entry.move
        except Exception:
            pass

    def negamax(b: chess.Board, depth: int, alpha: int, beta: int) -> tuple[int, chess.Move | None]:
        if depth == 0 or b.is_game_over():
            return (evaluate(b), None)

        best_score = -10**9
        best_move = None

        # Move ordering: captures first, then others
        moves = list(b.legal_moves)
        moves.sort(key=lambda m: (not b.is_capture(m), b.is_check()), reverse=False)

        for move in moves:
            b.push(move)
            score, _ = negamax(b, depth - 1, -beta, -alpha)
            score = -score
            b.pop()

            if score > best_score:
                best_score = score
                best_move = move
            if best_score > alpha:
                alpha = best_score
            if alpha >= beta:
                break
        return best_score, best_move

    _, move = negamax(board, max_depth, -10**9, 10**9)
    return move or chess.Move.null()

# ------------------------------ CLI Loop ------------------------------------

def parse_move(user_input: str, board: chess.Board) -> chess.Move | None:
    s = user_input.strip()
    if not s:
        return None
    # Try UCI first
    try:
        move = chess.Move.from_uci(s)
        if move in board.legal_moves:
            return move
    except Exception:
        pass
    # Try SAN
    try:
        move = board.parse_san(s)
        if move in board.legal_moves:
            return move
    except Exception:
        pass
    return None


def list_legal_moves(board: chess.Board) -> str:
    san_moves = []
    for m in board.legal_moves:
        try:
            san_moves.append(board.san(m))
        except Exception:
            san_moves.append(m.uci())
    san_moves.sort()
    return ", ".join(san_moves)


def prompt_side_and_depth() -> tuple[bool, int]:
    # Using input prompts directly for compatibility (avoid print(..., end="")).
    side = input("Choose your side: [w]hite / [b]lack (default: w): ").strip().lower()
    human_is_white = True if side in ("", "w", "white") else False if side in ("b", "black") else True

    try:
        d_str = input("AI depth (plies, 1-5, default 3): ").strip()
        d = int(d_str) if d_str else 3
        depth = max(1, min(5, d))
    except Exception:
        depth = 3
    return human_is_white, depth


def main() -> None:
    print("\n=== Console Chess (python-chess) ===")
    print("Type 'help' for commands. Moves in SAN (e.g., Nf3) or UCI (e2e4).\n")

    board = chess.Board()
    human_is_white, depth = prompt_side_and_depth()

    while not board.is_game_over():
        print_board(board)

        if (board.turn == chess.WHITE and human_is_white) or (board.turn == chess.BLACK and not human_is_white):
            # Human move
            while True:
                user = input("Your move> ").strip()
                if user.lower() in ("q", "quit", "exit"):
                    print("Goodbye!")
                    return
                if user.lower() in ("h", "help"):
                    print("Commands: help, moves, fen, undo, quit. Enter a move like 'e2e4' or 'Nf3'.")
                    continue
                if user.lower() == "moves":
                    print(list_legal_moves(board))
                    continue
                if user.lower() == "fen":
                    print(board.fen())
                    continue
                if user.lower() == "undo":
                    if board.move_stack:
                        board.pop()
                        break
                    else:
                        print("Nothing to undo.")
                        continue

                move = parse_move(user, board)
                if move is None:
                    print("Unrecognized or illegal move. Try again (type 'moves' to list legal moves).")
                    continue
                board.push(move)
                break
        else:
            # AI move
            print(f"AI thinking (depth {depth})...")
            start = time.time()
            move = search_best_move(board, max_depth=depth)
            elapsed = time.time() - start
            if move and move in board.legal_moves:
                print(f"AI plays: {board.san(move)} ({move.uci()})  [{elapsed:.2f}s]\n")
                board.push(move)
            else:
                # Fallback: pick first legal move
                move = next(iter(board.legal_moves))
                print(f"AI fallback plays: {board.san(move)} ({move.uci()})\n")
                board.push(move)

    print_board(board)
    if board.is_checkmate():
        print("Checkmate!", "White wins." if board.outcome().winner == chess.WHITE else "Black wins.")
    elif board.is_stalemate():
        print("Stalemate.")
    elif board.is_insufficient_material():
        print("Draw by insufficient material.")
    elif board.can_claim_threefold_repetition():
        print("Draw by threefold repetition (claimable).")
    else:
        print("Game over.")


# ------------------------------ Tests ---------------------------------------

def _run_tests() -> int:
    import unittest

    class ChessGameTests(unittest.TestCase):
        def test_parse_uci_basic(self):
            b = chess.Board()
            self.assertEqual(parse_move("e2e4", b), chess.Move.from_uci("e2e4"))

        def test_parse_san_basic(self):
            b = chess.Board()
            self.assertEqual(parse_move("e4", b), chess.Move.from_uci("e2e4"))

        def test_illegal_move_returns_none(self):
            b = chess.Board()
            self.assertIsNone(parse_move("e5", b))

        def test_ai_returns_legal_move(self):
            b = chess.Board()
            mv = search_best_move(b, max_depth=1, use_book=False)
            self.assertIn(mv, b.legal_moves)

        def test_evaluate_material_advantage(self):
            b_equal = chess.Board()
            b_white_up_pawn = chess.Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1")
            self.assertGreater(evaluate(b_white_up_pawn), evaluate(b_equal))

        def test_list_legal_moves_nonempty(self):
            b = chess.Board()
            s = list_legal_moves(b)
            self.assertTrue(len(s) > 0)

        def test_game_over_checkmate_detection(self):
            # Fool's mate position after 1.f3 e5 2.g4 Qh4#
            b = chess.Board()
            b.push_san("f3")
            b.push_san("e5")
            b.push_san("g4")
            b.push_san("Qh4#")
            self.assertTrue(b.is_checkmate())

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ChessGameTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    # Return non-zero on failure to help CI shells
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.exit(_run_tests())
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")
