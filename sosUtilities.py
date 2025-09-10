from typing import List

def is_sos(line: str) -> bool:
    return line is not None and len(line) == 3 and line.upper() == "SOS"


def count_sos_in_board(board: List[List[str]]) -> int:
    if not board:
        return 0

    n = len(board)

    def cell(r, c):
        v = board[r][c] if 0 <= r < n and 0 <= c < n else None
        return (v or "").strip().upper()[:1]

    total = 0

#row and column
    for r in range(n):
        for c in range(n - 2):
            row_str = cell(r, c) + cell(r, c + 1) + cell(r, c + 2)
            if is_sos(row_str):
                total += 1
    for c in range(n):
        for r in range(n - 2):
            col_str = cell(r, c) + cell(r + 1, c) + cell(r + 2, c)
            if is_sos(col_str):
                total += 1

# Diagonal
    for r in range(n - 2):
        for c in range(n - 2):
            dr = cell(r, c) + cell(r + 1, c + 1) + cell(r + 2, c + 2)
            if is_sos(dr):
                total += 1
    for r in range(n - 2):
        for c in range(2, n):
            dl = cell(r, c) + cell(r + 1, c - 1) + cell(r + 2, c - 2)
            if is_sos(dl):
                total += 1

    return total

