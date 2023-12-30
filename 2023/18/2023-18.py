from copy import deepcopy

with open('input.txt') as file:
    lines = file.read().splitlines()

# naive solution (1st part only)
"""
points = [(0, 0, None)]
i = 0
j = 0

# process trench coordinates and colors
for line in lines:
    dir, n, col = line.split()
    col = col[1:-1]
    for _ in range(int(n)):
        match dir:
            case 'R':
                j += 1
            case 'U':
                i -= 1
            case 'L':
                j -= 1
            case 'D':
                i += 1
        points.append((i, j, col))

i_min = min(p[0] for p in points)
i_max = max(p[0] for p in points)
j_min = min(p[1] for p in points)
j_max = max(p[1] for p in points)
M = i_max - i_min + 1
N = j_max - j_min + 1
trench = [[False for _ in range(N)] for __ in range(M)]

# fill in trench border
for p in points:
    trench[p[0] - i_min][p[1] - j_min] = True

trench_filled = deepcopy(trench)

# fill in the interior
for i in range(M):
    first_up = None
    inside = False
    for j in range(N):
        if trench[i][j]:
            if (first_up is None) and (i not in [0, M - 1]):
                first_up = trench[i - 1][j]
        else:
            if first_up is not None:  # first trench continues up and the last one down or vice versa
                if trench[i + 1][j - 1] == first_up:
                     inside = not inside
                first_up = None
            if inside:
                trench_filled[i][j] = True

#print('\n'.join(''.join('#' if t else '.' for t in row) for row in trench_filled))
# print(points)
print(sum(trench_filled[i][j] for i in range(M) for j in range(N)))
"""

for first in True, False:
    horiz = []
    i = 0
    j = 0
    for line in lines:
        if first:
            dir, n, col = line.split()
            match dir:
                case 'R':
                    col = '0'
                case 'D':
                    col = '1'
                case 'L':
                    col = '2'
                case 'U':
                    col = '3'
            dist = int(n)
        else:
            col = line[-7:-1]
            dist = int(col[:-1], 16)
        match col[-1]:
            case '0':
                horiz.append([i, j, j + dist])
                j += dist
            case '1':
                i += dist
            case '2':
                horiz.append([i, j - dist, j])
                j -= dist
            case '3':
                i -= dist

    # sort by vertical coordinate
    horiz.sort(key=lambda x: x[0])

    active = []
    area = 0
    for h in horiz:
        touching = []
        for i in range(len(active)):
            a = active[i]
            if a[1] == h[1]:
                if a[2] == h[2]:  # exactly matching `active` and `horiz`
                    area += (a[2] - a[1] + 1) * (h[0] - a[0] + 1)
                    del active[i]
                    break
                else:             # only left endpoints matching
                    area += (h[2] - h[1]) * (h[0] - a[0] + 1)
                    active[i][1] = h[2]
                    break
            elif a[2] == h[2]:    # only right endpoints matching
                area += (h[2] - h[1]) * (h[0] - a[0] + 1)
                active[i][2] = h[1]
                break
            elif a[1] < h[1] < a[2] and a[1] < h[2] < a[2]:  # `horiz` within `active`
                area += (h[2] - h[1] - 1) * (h[0] - a[0] + 1)
                active.append([a[0], h[2], a[2]])
                active[i][2] = h[1]
                break
            elif h[2] == a[1]:   # `horiz` touching the left side of `active`
                touching.append(i)
                area += (a[2] - a[1] + 1) * (h[0] - a[0])
                active[i][0] = h[0]
                active[i][1] = h[1]
            elif h[1] == a[2]:   # `horiz` touching the right side of `active`
                touching.append(i)
                area += (a[2] - a[1] + 1) * (h[0] - a[0])
                active[i][0] = h[0]
                active[i][2] = h[2]
        else:   # for:
            if len(touching) == 2:  # `horiz` had `active` on both sides
                active[touching[0]][1] = min(active[i][1] for i in touching)
                active[touching[0]][2] = max(active[i][2] for i in touching)
                del active[touching[1]]
            elif not touching:   # no match at all -- new active
                active.append([h[0], h[1], h[2]])

    print(f'Part {1 if first else 2}: {area}')
