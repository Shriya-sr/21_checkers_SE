SIZE = 8

KING_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
MAN_DIRS = {"R": [(-1, -1), (-1, 1)], "B": [(1, -1), (1, 1)]}


def in_bounds(pos):
    return 0 <= pos[0] < SIZE and 0 <= pos[1] < SIZE


def owns(player, piece):
    """True if the piece ("R", "RK", "B", "BK") belongs to player."""
    return piece != "." and piece[0] == player


def piece_directions(piece):
    """(row, col) steps this piece may use. Kings: all four; men: forward only."""
    if piece == ".":
        return []
    if len(piece) == 2:
        return KING_DIRS
    return MAN_DIRS[piece]


def simple_move(board, player, start, end):
    if not (in_bounds(start) and in_bounds(end)):
        return False
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    return (
        owns(player, piece) and
        board[er][ec] == "." and
        (er - sr, ec - sc) in piece_directions(piece)
    )


def capture_move(board, player, start, end):
    if not (in_bounds(start) and in_bounds(end)):
        return False
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if not owns(player, piece) or board[er][ec] != ".":
        return False
    jumps = [(2 * dr, 2 * dc) for dr, dc in piece_directions(piece)]
    if (er - sr, ec - sc) not in jumps:
        return False
    middle = board[(sr + er) // 2][(sc + ec) // 2]
    return middle != "." and not owns(player, middle)


def pieces_of(board, player):
    return [
        (r, c)
        for r in range(SIZE)
        for c in range(SIZE)
        if owns(player, board[r][c])
    ]


def captures_from(board, player, pos):
    """Landing squares of every capture available to the piece at pos."""
    r, c = pos
    ends = []
    for dr, dc in piece_directions(board[r][c]):
        end = (r + 2 * dr, c + 2 * dc)
        if capture_move(board, player, pos, end):
            ends.append(end)
    return ends


def all_captures(board, player):
    """List of (start, end) for every capture any of player's pieces can make."""
    result = []
    for pos in pieces_of(board, player):
        for end in captures_from(board, player, pos):
            result.append((pos, end))
    return result


def has_legal_move(board, player):
    if all_captures(board, player):
        return True
    for r, c in pieces_of(board, player):
        for dr, dc in piece_directions(board[r][c]):
            if simple_move(board, player, (r, c), (r + dr, c + dc)):
                return True
    return False


def promote(board):
    """Promote men on their back row. Returns True if a promotion happened."""
    promoted = False
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted = True
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted = True
    return promoted