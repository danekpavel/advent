import re

tmp = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
]
tmp = dict(enumerate(tmp, 1))
DIGITS = dict(zip(tmp.values(), tmp.keys()))
DIGITS_RE = '|'.join(DIGITS.keys())  # 'one|two|three|...'


def insert_numeric_digit(text: str, first: bool) -> str:
    # first: True -- first digit, False -- last digit

    regex = '(' + DIGITS_RE + ')'
    if not first:
        # 'eat' everything before the last digit
        regex = '.*' + regex

    res = re.search(regex, text)
    if res:
        # insert the numeric digit at the digit word's beginning/end
        i = res.span()[0 if first else 1]
        text = text[:i] + str(DIGITS[res.group(1)]) + text[i:]

    return text


def outer_digits(text: str, use_text: bool = False) -> int:
    # add numeric digits for the first and the last text digits
    if use_text:
        text = insert_numeric_digit(text, True)
        text = insert_numeric_digit(text, False)

    d = re.findall(r'\d', text)
    return int(d[0] + d[-1])


with open('input.txt', 'r') as file:
    lines = file.readlines()

# use_t: False -- part 1, True -- part 2
for use_t in [False, True]:
    total = sum([outer_digits(line, use_t) for line in lines])
    print(f'Part {use_t + 1}: {total}')
