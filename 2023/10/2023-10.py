
def mat_ind(i, j):
    return i * N + j


def go_through(through: int, origin: int|None, first: bool = True) -> int:
    """
    Goes through the pipe into its neighbor other than `origin`.
    When `origin` is None, first or second neighbor is selected according to `first`.
    """
    nei = neighb[through]
    if origin is None:
        return nei[0 if first else 1]
    return nei[0] if origin == nei[1] else nei[1]


def maze_str(fill_inside: bool = False) -> list[str]:
    m = ''.join([maze[i] if is_loop[i] else '.'for i in range(M * N)])
    if fill_inside:
        m = ''.join(['I' if is_inside[i] else m[i] for i in range(M * N)])
    return [m[i:i+N] for i in range(0, M * N, N)]


with open('input.txt') as file:
    lines = file.read().splitlines()
M = len(lines)
N = len(lines[0])

maze = ''.join(lines)
# list of 2-item lists of neighbours
neighb = [[] for _ in range(M * N)]
start = None
for i in range(M):
    for j in range(N):
        ind = mat_ind(i, j)
        match maze[ind]:
            case '.':
                continue
            case '|':
                neighb[ind] = [mat_ind(i - 1, j), mat_ind(i + 1, j)]
            case '-':
                neighb[ind] = [mat_ind(i, j - 1), mat_ind(i, j + 1)]
            case 'L':
                neighb[ind] = [mat_ind(i - 1, j), mat_ind(i, j + 1)]
            case 'J':
                neighb[ind] = [mat_ind(i - 1, j), mat_ind(i, j - 1)]
            case '7':
                neighb[ind] = [mat_ind(i, j - 1), mat_ind(i + 1, j)]
            case 'F':
                neighb[ind] = [mat_ind(i, j + 1), mat_ind(i + 1, j)]
            case 'S':
                start = ind

# find tiles connected to 'start'
neighb[start] = [i for i in range(len(neighb)) if start in neighb[i]]


def mark_inside(i: int, j: int, dis: list[int], djs: list[int]) -> None:
    global is_inside
    for di, dj in zip(dis, djs):
        if 0 <= i + di < M and 0 <= j + dj < N:
            ind = mat_ind(i + di, j + dj)
            is_inside[ind] = True


# find the main loop
is_loop = [False for _ in range(M * N)]
is_inside = is_loop.copy()
current = start
prev = None
i = 0
while True:
    is_loop[current] = True
    # the last argument may need to be negated to mark inside tiles correctly
    next = go_through(current, prev, True)
    if next == start:
        break
    prev = current
    current = next

    # 'look left' and mark everything as inside
    up = current > prev   # Did we come from a lower-numbered tile?
    di = []
    dj = []
    match maze[current]:
        case '|':
            di = [0]
            dj = [1 if up else -1]
        case '-':
            di = [-1 if up else 1]
            dj = [0]
        case 'L':
            if not up:
                di = [1, 0]
                dj = [0, -1]
        case 'J':
            if abs(current - prev) > 1:
                di = [0, 1]
                dj = [1, 0]
        case '7':
            if up:
                di = [-1, 0]
                dj = [0, 1]
        case 'F':
            if abs(current - prev) > 1:
                di = [0, -1]
                dj = [-1, 0]
    mark_inside(current // N, current % N, di, dj)
print(f'Part 1: {round(sum(is_loop) / 2)}')

for i in range(len(is_loop)):
    # remove false insides
    if is_loop[i]:
        is_inside[i] = False
    else:
        # fill holes, i.e. sequences of 'not inside' after in 'inside'
        if not is_inside[i] and is_inside[i - 1]:
            is_inside[i] = True

print(f'Part 2: {sum(is_inside)}')