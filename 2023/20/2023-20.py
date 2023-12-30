from collections import deque

with open('input.txt') as file:
    lines = file.read().splitlines()

broadcaster = None
modules = dict()
conj = []

for l in lines:
    name, outputs = l.split(' -> ')
    outputs = outputs.split(', ')
    if name == 'broadcaster':
        modules[name] = [None, outputs]
    else:
        # [state, [outputs]]
        if name[0] == '%':
            val = [False, outputs]
        # [inputs: dict, [outputs]]
        else:
            val = [dict(), outputs]
            conj.append(name[1:])

        modules[name[1:]] = val

# store inputs for conjunctions
for m_name in modules.keys():
    module = modules[m_name]
    for output in module[1]:
        if output in conj:
            modules[output][0][m_name] = False

def add_task(pulse: bool, mod: str, source: str | None):
    global tasks
    global n_low
    global n_high
    #print(f'Processing {pulse}, {mod}, {source}')
    tasks.append([pulse, mod, source])
    if pulse:
        n_high += 1
    else:
        n_low += 1

print(modules)

tasks = deque()
n_low = 0
n_high = 0
rxs = []
# for i in range(20):
i = 0
while True:
    rx = []
    n_low += 1  # button click
    for o in modules['broadcaster'][1]:
        add_task(False, o, 'broadcaster')
    while tasks:
        pulse, m_name, source = tasks.popleft()
        if m_name not in modules.keys():  # output-only module
            rx.append(pulse)
            continue
        module = modules[m_name]
        if isinstance(module[0], bool):  # flip-flop
            if not pulse:  # low pulse
                module[0] = not module[0]
                for o in module[1]:
                    add_task(module[0], o, m_name)
        else:   # conjunction
            module[0][source] = pulse
            for o in module[1]:
                add_task(not all(module[0].values()), o, m_name)
    if len(rx) < 4:
        print(i, rx)
        break
    i += 1
    if i % 10e6 == 0:
        print(i)
    #rxs.append(rx)

print(n_low * n_high)
print(min(len(rx) for rx in rxs))