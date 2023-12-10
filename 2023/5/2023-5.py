import re

Rule = list[int, int, int]
Mapping = list[Rule]
InputRange = list[int, int]


def map_one_level(source: int, mapping: Mapping) -> int:
    for src_start, src_end, diff in mapping:  # all rules within the level
        if src_start <= source <= src_end:
            return source + diff
    return source


def map_all_levels(source: int) -> int:
    for m in mappings:
        source = map_one_level(source, m)
    return source


def read_numbers(text: str) -> list[int]:
    # Returns all numbers from a string as a list of integers
    return [int(n) for n in re.findall('[0-9]+', text)]


def read_rule(text: str) -> Rule:
    # Returns source range _start_ and _end_ and the _difference_ to destination range
    numbers = read_numbers(text)
    return [numbers[1],
            numbers[1] + numbers[2] - 1,
            numbers[0] - numbers[1]]


def apply_rule(input_range: InputRange, rule: Rule) -> tuple[InputRange, list[InputRange]]:
    """
    Applies the rule to appropriate parts of the given range

    Args:
        input_range: input range: [from, to]
        rule: [range from, range to, difference]

    Returns:
        A tuple containing:
           Transformed input range (empty list in the case of no intersection)
           Remaining untransformed ranges: a list with 0-2 items
    """

    # three parts of the seed range relative to rule range []    0[1]2
    parts = [[input_range[0], min(input_range[1], rule[0] - 1)],
             [max(input_range[0], rule[0]), min(input_range[1], rule[1])],
             [max(input_range[0], rule[1] + 1), input_range[1]]]
    # empty nonsensical (i.e. not present) parts
    parts = [p if p[0] <= p[1] else [] for p in parts]

    return ([n + rule[2] for n in parts[1]],  # transformed intersection (part 1)
            # non-empty outer parts (0 & 2)
            [parts[i] for i in range(len(parts)) if i != 1 and parts[i]])


def apply_mapping(input_ranges: list[InputRange], mapping: Mapping) -> list[InputRange]:
    # Changes input ranges to output ranges for one mapping
    output_ranges = []
    for rule in mapping:
        remaining_input_ranges = []
        for input_range in input_ranges:
            out, inp = apply_rule(input_range, rule)
            if out:
                output_ranges.append(out)
            remaining_input_ranges += inp
        input_ranges = remaining_input_ranges
    # return all transformed input ranges + input ranges not covered by a rule
    return output_ranges + remaining_input_ranges


with open('input.txt') as file:
    lines = file.readlines()

# read seeds
seeds = read_numbers(lines[0])
# read mappings
mappings = []
for l in lines[2:]:
    if re.match('[a-z]', l):
        mapping = []
    elif re.match('[0-9]', l):
        mapping.append(read_rule(l))
    else:
        mappings.append(mapping)
else:  # the last line
    mappings.append(mapping)

# reinterpret seeds as seed ranges
ranges = [[seeds[i], seeds[i] + seeds[i + 1] - 1]
          for i in range(len(seeds)) if not i % 2]

for mapping in mappings:
    ranges = apply_mapping(ranges, mapping)

print(f'Part 1: {min(map_all_levels(s) for s in seeds)}')
print(f'Part 2: {min(ir[0] for ir in ranges)}')


