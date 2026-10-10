from board import initial_board, move_piece, SIZE
from rules import (
    simple_move, capture_move, promote,
    captures_from, all_captures, has_legal_move, pieces_of,
)

NAMES = {"R": "Red", "B": "Black"}


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.chain = None  # square of the piece that must keep capturing

    def print_board(self):
        print("\n   " + " ".join(f"{c:<2}" for c in range(SIZE)).rstrip())
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(f"{cell:<2}" for cell in row).rstrip())

    def game_over(self):
        opponent = "B" if self.player == "R" else "R"
        if not pieces_of(self.board, self.player):
            print(f"{NAMES[opponent]} wins: {NAMES[self.player]} has no pieces left.")
            return True
        if not has_legal_move(self.board, self.player):
            print(f"{NAMES[opponent]} wins: {NAMES[self.player]} has no legal moves.")
            return True
        return False

    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            self.print_board()
            if self.game_over():
                return

            prompt = f"{self.player}> "
            if self.chain is not None:
                prompt = f"{self.player} (continue from {self.chain[0]} {self.chain[1]})> "
            raw = input(prompt).strip().lower().split()
            if raw == ["q"]:
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start, end = (sr, sc), (er, ec)

            if self.chain is not None and start != self.chain:
                print(f"You must keep capturing with the piece at ({self.chain[0]},{self.chain[1]}).")
                continue

            if capture_move(self.board, self.player, start, end):
                captured = True
            elif self.chain is not None:
                print("Invalid capture. You must continue capturing with that piece.")
                continue
            elif simple_move(self.board, self.player, start, end):
                options = all_captures(self.board, self.player)
                if options:
                    listing = ", ".join(
                        f"{s[0]} {s[1]} -> {e[0]} {e[1]}" for s, e in options
                    )
                    print(f"Capture is mandatory. Available: {listing}")
                    continue
                captured = False
            else:
                print("Invalid move.")
                continue

            # The move is accepted. Gather what the result line needs
            # before the board changes.
            was_man = len(self.board[sr][sc]) == 1
            if captured:
                mr, mc = (sr + er) // 2, (sc + ec) // 2
                victim = self.board[mr][mc]

            move_piece(self.board, start, end)
            promote(self.board)
            promoted = was_man and len(self.board[er][ec]) == 2

            # Exactly one result line per accepted move.
            if captured:
                result = (f"{self.player} captured {victim} at ({mr},{mc}): "
                          f"({sr},{sc}) -> ({er},{ec})")
            else:
                result = f"{self.player} moved ({sr},{sc}) -> ({er},{ec})"
            if promoted:
                result += ", promoted to king"
            print(result)

            if captured and not promoted and captures_from(self.board, self.player, end):
                self.chain = end  # same piece must jump again; turn does not pass
                print(f"{self.player} must continue capturing with the piece at ({er},{ec})")
            else:
                self.chain = None
                self.player = "B" if self.player == "R" else "R"