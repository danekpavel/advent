import math
import queue

INF = math.inf

with open('input.txt') as file:
    blocks = file.read().splitlines()
blocks = [[int(b) for b in row] for row in blocks]
M = len(blocks)
N = len(blocks[0])

# current minimum heat loss for row/column/dir/dir_left
block_min = [[[[INF for dir_left in range(3)] for dir in range(4)] for j in range(N)] for i in range(M)]
todo = queue.PriorityQueue()
# start with the two neighbours of the top left block
# i, j, dir (direction we came from), dir_left (steps left in direction dir), heat loss so far
todo.put((0, (0, 1, 0, 2, 0)))
todo.put((0, (1, 0, 3, 2, 0)))

while not todo.empty():
    i, j, dir, dir_left, heat = todo.get()[1]
    heat += blocks[i][j]

    if i == M - 1 and j == N - 1:
        break  # bottom right reached

    # steps left in all four directions
    dir_left_all = [dir_left if d == dir else 3 for d in range(4)]
    # don't allow opposite direction
    dir_left_all[(dir + 2) % 4] = 0
    # don't allow destinations outside the area
    if i == 0:
        dir_left_all[1] = 0
    elif i == N - 1:
        dir_left_all[3] = 0
    if j == 0:
        dir_left_all[2] = 0
    elif j == M - 1:
        dir_left_all[0] = 0

    # Is the state we are in better than the previous best one?
    for d in range(len(dir_left_all)):
        d_left = dir_left_all[d]
        if d_left and block_min[i][j][d][d_left - 1] > heat:
            # update current d_left and all smaller ones which have a larger value
            for dl in range(d_left, 0, -1):
                if block_min[i][j][d][dl - 1] > heat:
                    block_min[i][j][d][dl - 1] = heat
                else:
                    break
            i_next = i
            j_next = j
            match d:
                case 0:
                    j_next = j + 1
                case 1:
                    i_next = i - 1
                case 2:
                    j_next = j - 1
                case 3:
                    i_next = i + 1
            todo.put((heat, (i_next, j_next, d, d_left - 1, heat)))

print(f'Part 1: {heat}')


block_min = [[[[INF for dir_left in range(7)] for dir in range(4)] for j in range(N)] for i in range(M)]
todo = queue.PriorityQueue()
# start with the two neighbours of the top left block
# i, j, dir (direction we came from), dir_left (steps left in direction dir), heat loss so far
todo.put((0, (0, 4, 0, 6, sum(blocks[0][j] for j in range(1, 4)), [0, 0])))
todo.put((0, (4, 0, 3, 6, sum(blocks[i][0] for i in range(1, 4)), [0, 0])))

while not todo.empty():
    i, j, dir, dir_left, heat, path = todo.get()[1]
    heat += blocks[i][j]

    if i == M - 1 and j == N - 1:
        # print(path + [i, j])
        break  # bottom right reached

    # steps left in all four directions; 7 represents 10 (7, 8, 9 are not possible)
    dir_left_all = [dir_left if d == dir else 7 for d in range(4)]
    # don't allow opposite direction
    dir_left_all[(dir + 2) % 4] = 0

    # Is the state we are in better than the previous best one?
    for d in range(4):
        d_left = dir_left_all[d]
        if d_left and block_min[i][j][d][d_left - 1] > heat:
            # maximum d_left has to be treated differently because of lower flexibility caused by the 4-block jump
            if d_left == 7:
                block_min[i][j][d][d_left - 1] = heat
            else:
                # update current d_left and all smaller ones which have a larger value
                for dl in range(d_left, 0, -1):
                    if block_min[i][j][d][dl - 1] > heat:
                        block_min[i][j][d][dl - 1] = heat
                    else:
                        break
            i_next = i
            j_next = j
            # "jump" through four or go to a neighbour
            diff = 4 if d_left == 7 else 1
            match d:
                case 0:
                    j_next = j + diff
                case 1:
                    i_next = i - diff
                case 2:
                    j_next = j - diff
                case 3:
                    i_next = i + diff
            # stop for this direction when we would continue outside the area
            if not (0 <= i_next < M) or not (0 <= j_next < N):
                continue
            # heat loss when reaching the destination
            heat_next = heat
            if diff == 4:
                match d:
                    case 0:
                        heat_next += sum(blocks[i][jj] for jj in range(j + 1, j + 4))
                    case 1:
                        heat_next += sum(blocks[ii][j] for ii in range(i - 1, i - 4, -1))
                    case 2:
                        heat_next += sum(blocks[i][jj] for jj in range(j - 1, j - 4, -1))
                    case 3:
                        heat_next += sum(blocks[ii][j] for ii in range(i + 1, i + 4))
            todo.put((heat_next, (i_next, j_next, d, d_left - 1, heat_next, path + [i, j])))

print(f'Part 2: {heat}')
