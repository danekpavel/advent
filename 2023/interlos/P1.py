with open('losi-plotr.txt') as file:
    lines = file.read().splitlines()


def plot_it(lines: list[str]) -> list[list[int, int]]:
    i, j = 0, 0
    out = []
    for l in lines:
        if l[0] == '#':
            out.append([i, j])
        match l[1]:
            case 'U':
                i += 1
            case 'D':
                i -= 1
            case 'L':
                j -= 1
            case 'R':
                j += 1

    i_min = min(o[0] for o in out)
    i_max = max(o[0] for o in out)
    j_min = min(o[1] for o in out)
    j_max = max(o[1] for o in out)

    out_mat = [[' ' for _ in range(j_max + 1)] for __ in range(abs(i_min) + 1)]
    print(j_max)
    print(i_min)

    for i, j in out:
        out_mat[abs(i)][j] = '#'

    return out_mat

out_mat = plot_it(lines)

"""
with open('plotr.txt', 'w') as f:
    f.write('\n'.join([''.join(row) for row in out_mat]))
"""
def n_to_command(n):
    match n:
        case 4:
            return 'R'
        case 5:
            return 'D'
        case 2:
            return 'U'
        case 1:
            return 'L'


commands = [sum(out_mat[i][j] == '#' for j in range(9, 16)) for i in range(len(out_mat)) if not i % 6]
commands = [n_to_command(c) for c in commands]
dashes = [out_mat[i][3] == '#' for i in range(len(out_mat)) if not i % 6]
dashes = ['#' if dashes[i] else ' ' for i in range(len(commands))]

second_output = plot_it([dashes[i] + commands[i] for i in range(len(dashes))])
print(second_output)
with open('plotr2.txt', 'w') as f:
    f.write('\n'.join([''.join(row) for row in second_output]))
