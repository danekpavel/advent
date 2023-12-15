
with open('input.txt') as file:
    lines = file.read().splitlines()
lines.append('')

def transpose(l: list[str]) -> list[str]:
    return [''.join(row[i] for row in l) for i in range(len(l[0]))]


def reflects_after(row: str, after: int) -> bool:
    # use reflection when `after` is after half
    if after >= len(row) / 2:
        row = row[::-1]
        after = len(row) - after
    return row[:after] == row[2 * after - 1:after - 1:-1]


def find_reflection(pattern: list[str], ignore: int = None) -> int:
    for j in range(1, len(pattern[0])):
        if j != ignore:
            for row in pattern:
                if not reflects_after(row, j):
                    break
            else:
                return j
    return 0


def smudge_at(pattern: list[str], at: int):
    n = len(pattern[0])
    i = at // n
    j = at % n
    smudged = pattern.copy()
    tmp = list(smudged[i])
    tmp[j] = '.' if tmp[j] == '#' else '#'
    smudged[i] = ''.join(tmp)
    return smudged


total_orig = 0
total_smug = 0
pattern = []
j = 0
for i in range(len(lines)):
    line = lines[i]

    if not line:
        # process pattern
        if not (orig := find_reflection(pattern)):
            orig = 100 * find_reflection(transpose(pattern))
        total_orig += orig

        for at in range(len(pattern) * len(pattern[0])):
            smudged = smudge_at(pattern, at)
            smug = find_reflection(smudged, orig % 100)
            if not smug or smug == orig:
                smug = 100 * find_reflection(transpose(smudged), orig // 100)
            if smug and smug != orig:
                total_smug += smug
                break
        pattern = []
    else:
        # grow pattern
        pattern += [lines[i]]

print(f'Part 1: {total_orig}')
print(f'Part 2: {total_smug}')