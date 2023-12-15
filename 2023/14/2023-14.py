with open('input.txt') as file:
    lines = file.read().splitlines()


def move_rotate(rows: list[str]) -> tuple[list[str], int]:
    rows_new = []
    load = 0
    # for each column
    for j in range(N):
        col = [r[j] for r in rows]
        i = 0
        avail: int|None = None
        while i < N:
            match col[i]:
                case 'O':   # move to free position, empty position `i` and set `i` to just after that
                    if avail is not None:
                        load += N - avail
                        col[avail] = 'O'
                        col[i] = '.'
                        i = avail + 1
                        avail = None
                    else:
                        load += N - i
                        i += 1
                case '.':
                    if avail is None:
                        avail = i
                    i += 1
                case '#':
                    avail = None
                    i += 1
        rows_new.append(''.join(col[::-1]))
    return rows_new, load


def hash_it(rows: list[str]):
    at = tuple(i for i in range(N**2) if rows[i // N][i % N] == 'O')
    return hash(at)


def load_north(rows: list[str]) -> int:
    return sum(N - i // N for i in range(N**2) if rows[i // N][i % N] == 'O')


N = len(lines)
total = 0

hashes = []
loads = []
current = lines
while True:
    # do one cycle
    for i in range(4):
        current, load = move_rotate(current)
    loads.append(load_north(current))
    h = hash_it(current)
    hashes.append(h)
    if h in hashes[:-1]:
        break

# Where do the first and second repeating sequences start?
first, second = (i for i, h in enumerate(hashes) if h == hashes[-1])
print(f'Part 2: {loads[(10**9 - first - 1) % (second - first) + first]}')