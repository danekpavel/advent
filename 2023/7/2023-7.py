from collections import Counter

# card strengths as characters -- '2': 'a', ..., 'A': 'l'
tmp = ''.join(str(i) for i in range(2, 10)) + 'TJQKA'
STRENGTH = {c: chr(s + 97) for s, c in enumerate(tmp)}

# part 2: Joker is the weakest one
tmp = 'J' + ''.join(str(i) for i in range(2, 10)) + 'TQKA'
STRENGTH_JOKER = {c: chr(s + 97) for s, c in enumerate(tmp)}


def hand_type_strength(hand: str, use_joker: bool = False) -> int:
    """Returns hand type strength 1--7, weakest to strongest"""

    # replace Jokers with the most common other card
    if use_joker and ('J' in hand) and (hand != 'JJJJJ'):
        # find the most common non-Joker
        tab = Counter(c for c in hand if c != 'J')
        most_common = tab.most_common(1)[0][0]
        hand = ''.join(most_common if c == 'J' else c for c in hand)

    tab = Counter(hand)

    match len(tab):
        case 1:  # five of a kind
            return 7
        case 2:  # four of a kind  /  full house
            return 6 if max(tab.values()) == 4 else 5
        case 3:  # three of a kind  /  two pair
            return 4 if max(tab.values()) == 3 else 3
        case 4:  # one pair
            return 2
        case 5:  # high card
            return 1


def hand_strength(hand: str, use_joker: bool = False) -> str:
    strength = STRENGTH_JOKER if use_joker else STRENGTH
    return str(hand_type_strength(hand, use_joker)) + ''.join(strength[c] for c in hand)


with open('input.txt') as file:
    lines = file.readlines()

# list of [hand, bid] lists
hands_bids = [line.split() for line in lines]

for use_joker in False, True:
    # sort hands and bids by hand strength
    hb_sorted = sorted(hands_bids, key=lambda hb: hand_strength(hb[0], use_joker))
    # bid ranking
    rank_bid = list(enumerate((bid for _, bid in hb_sorted), 1))
    print(f'Part {2 if use_joker else 1}: {sum(rank * int(bid) for rank, bid in rank_bid)}')