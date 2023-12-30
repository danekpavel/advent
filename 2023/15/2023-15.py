with open('input.txt') as file:
    inp = file.read().splitlines()[0]


def hash_it(str: str) -> int:
    val = 0
    for c in str:
        val += ord(c)
        val = (val * 17) % 256
    return val


boxes = [dict() for _ in range(256)]

total1 = 0
for str in inp.split(','):
    total1 += hash_it(str)
    if str[-1] == '-':
        label = str[:-1]
        removing = True
    else:
        label = str[:-2]
        removing = False
    box = hash_it(label)
    if removing:
        if label in boxes[box].keys():
            boxes[box].pop(label)
    else:
        boxes[box][label] = int(str[-1])

total2 = 0
for i, box in enumerate(boxes):
    for j, focal in enumerate(box.values()):
        total2 += (i + 1) * (j + 1) * focal

print(f'Part 1: {total1}')
print(f'Part 2: {total2}')
