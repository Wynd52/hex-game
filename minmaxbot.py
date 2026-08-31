import heapq
from system import winner, create_board

def conections(board, player, neightbour_map):

    score = 0

    for i in range(len(board)):

        if board[i] != player:
            continue

        for s in neightbour_map[i]:

            if board[s] == player:
                score += 1

    return score

def distance(board, n, player, neightbour_map):

    INF = 10**9
    dist = [INF] * len(board)
    heap = []

    if player == 1:
        start = range(n)

        def finish(i):
            return i // n == n - 1

    else:
        start = range(0, n*n ,n)

        def finish(i):
            return i % n == n - 1

    for i in start:

        if board[i] == 3 - player:
            continue

        price = 0 if board[i] == player else 1

        dist[i] = price
        heapq.heappush(heap, (price, i))

    while heap:

        d, current = heapq.heappop(heap)

        if d != dist[current]:
            continue

        if finish(current):
            return d

        for s in neightbour_map[current]:

            if board[s] == 3 - player:
                continue

            price = 0 if board[s] == player else 1
            new_price = d + price

            if new_price < dist[s]:
                dist[s] = new_price
                heapq.heappush(heap, (new_price, s))

    return INF

def danger(board, player, neightbour_map):

    score = 0

    for i in range(len(board)):

        if board[i] != player:
            continue

        free = 0
        mine = 0

        for s in neightbour_map[i]:

            if board[s] is None:
                free += 1

            elif board[s] == player:
                mine += 1

        if free >= 2 and mine >= 1:
            score += 2

        if free >= 2 and mine >= 2:
            score += 4

    return score

def bridges(board, player, neightbour_map):

    score = 0

    for i in range(len(board)):

        if board[i] != player:
            continue

        for j in range(i + 1, len(board)):

            if board[j] != player:
                continue

            both = []

            for s in neightbour_map[i]:

                if s in neightbour_map[j]:
                    both.append(s)

            if len(both) >= 2:

                free = sum(
                    board[s] is None
                    for s in both
                )

                if free:
                    score += free
    return score

def heuristika(board, n, neightbour_map):

    if winner(board, n, 2, neightbour_map):
        return 100000

    if winner(board, n, 1, neightbour_map):
        return -100000

    bot_path = distance(board, n, 2, neightbour_map)
    player_path = distance(board, n, 1, neightbour_map)

    bot_connection = conections(board, 2, neightbour_map)
    player_connection = conections(board, 1, neightbour_map)

    bot_danger = danger(board, 2, neightbour_map)
    player_danger = danger(board, 1, neightbour_map)

    bot_bridges = bridges(board, 2, neightbour_map)
    player_bridges = bridges(board, 1, neightbour_map)

    score = 0

    score += (player_path - bot_path) * 10

    score += (bot_connection - player_connection) * 3

    score += (bot_danger - player_danger) * 4

    score += (bot_bridges - player_bridges) * 6

    return score

def candidates(board, neightbour_map):
    blocked = [ 
        i for i, x in enumerate(board) 
        if x is not None
    ]
    if not blocked: 
        return [len(board) // 2]
    
    candidate = set()

    for i in blocked:

        for s in neightbour_map[i]:

            if board[s] is None:
                candidate.add(s)
    return list(candidate)

def move_sort(board, n, moves, player, neightbour_map):

    rated = []

    for move in moves:

        board[move] = player

        score = heuristika(board, n, neightbour_map)

        board[move] = None

        rated.append((score, move))

    if player == 2:
        rated.sort(reverse=True)

    else:
        rated.sort()

    return[
        move
        for _, move in rated
    ]

def minmax(board, n, depth, alpha, beta, maximizing, cache, neightbour_map):

    key = (
        tuple(board), 
        depth, 
        maximizing
    )

    if key in cache:
        return cache[key]
    

    if winner(board, n, 2, neightbour_map):
        return 100000 + depth

    if winner(board, n, 1, neightbour_map):
        return -100000 - depth

    if depth == 0:
        return heuristika(board, n, neightbour_map)

    moves = candidates(board, neightbour_map)

    if not moves:
        return heuristika(board, n, neightbour_map)

    if maximizing:

        best = -float("inf")

        moves = move_sort(board, n, moves, 2, neightbour_map)

        for move in moves:

            board[move] = 2

            score = minmax(
                board,
                n,
                depth - 1,
                alpha,
                beta,
                False, 
                cache,
                neightbour_map
            )

            board[move] = None

            best = max(best, score)
            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:

        best = float("inf")

        moves = move_sort(board, n, moves, 1, neightbour_map)

        for move in moves:

            board[move] = 1

            score = minmax(
                board,
                n,
                depth - 1,
                alpha,
                beta,
                True,
                cache,
                neightbour_map
            )

            board[move] = None

            best = min(best, score)
            beta = min(beta, best)

            if beta <= alpha:
                break

        cache[key] = best

        return best

def minmax_bot(hexagons, n, neightbour_map, depth=2):

    board = create_board(hexagons)

    moves = candidates(board, neightbour_map)

    if not moves:
        return None

    cache = {}

    moves = move_sort(board, n, moves, 2, neightbour_map)

    best_move = moves[0]
    best_score = -float("inf")

    alpha = -float("inf")
    beta = float("inf")

    for move in moves:

        board[move] = 2

        score = minmax(
            board,
            n,
            depth - 1,
            alpha,
            beta,
            False, 
            cache,
            neightbour_map
        )

        board[move] = None

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, best_score)

    return best_move