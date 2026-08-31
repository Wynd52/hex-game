from buttons import vyherca
import numpy as np

def create_board(hexagons): 
    return [ getattr(h, "player", None) for h in hexagons ]

def create_neightbors(n, size_hex=1):

    dx = 1.5 * size_hex + 0.23
    dy = np.sqrt(3) * size_hex

    position = []

    for row in range(n):
        for col in range(n):
            x = col * dx + 0.85 * row
            y = row * dy - 0.24 * row

            position.append((x, y))

    neightbour_map = {}

    for i, (x, y) in enumerate(position):

        neightbour_map[i] = []

        for j, (sx, sy) in enumerate(position):

            if i == j:
                continue

            vzd2 = (sx - x) ** 2 + (sy - y) ** 2

            if vzd2 < (1.8 * size_hex) ** 2:
                neightbour_map[i].append(j)

    return neightbour_map

def winner(board, n, player, neightbour_map):

    if player == 1:

        start = [
            col
            for col in range(n)
            if board[col] == player
        ]

    else:

        start = [
            row * n
            for row in range(n)
            if board[row * n] == player
        ]

    if not start:
        return False

    fronta = start[:]
    visited = set(start)

    while fronta:
        current = fronta.pop()

        row = current // n
        col = current % n

        if player == 2 and col == n - 1:
            return True

        if player == 1 and row == n - 1:
            return True

        for s in neightbour_map[current]:
            if s in visited:
                continue

            if board[s] != player:
                continue

            visited.add(s)
            fronta.append(s)


    return False

def detection(n, hexagons, farba_1, farba_2, neightbour_map):

    board = create_board(hexagons)

    if winner(board, n, 1, neightbour_map):
        vyherca(farba_1)
        return True

    elif winner(board, n, 2, neightbour_map):
        vyherca(farba_2)
        return True

    return False

    