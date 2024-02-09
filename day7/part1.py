import functools
import re


card_to_value = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def hand_type(hand):
    sorted_hand = "".join(sorted(hand))
    # Five of a kind
    if re.search("([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\1{4}", sorted_hand) != None:
        return 1
    # Four of a kind
    if re.search("([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\1{3}", sorted_hand) != None:
        return 2
    # Full house
    if re.search("([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\1{1}([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\2{2}|([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\3{2}([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\4{1}", sorted_hand) != None:
        return 3
    # Three of a kind
    if re.search("([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\1{2}", sorted_hand) != None:
        return 4
    # Two pair
    if re.search("([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\1{1}.*([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\2{1}", sorted_hand) != None:
        return 5
    # One pair
    if re.search("([A|K|Q|J|T|9|8|7|6|5|4|3|2])\\1{1}", sorted_hand) != None:
        return 6
    return 7


def compare(h1, h2):
    h1_type = hand_type(h1[0])
    h2_type = hand_type(h2[0])
    if h1_type != h2_type:
        return h1_type - h2_type
    for i in range(5):
        if h1[0][i] != h2[0][i]:
            return card_to_value[h2[0][i]] - card_to_value[h1[0][i]]
    return 0


f = open("input.txt", "r")

hands = [line.split(" ") for line in f.read().splitlines()]
sorted_hands = list(reversed(sorted(hands, key=functools.cmp_to_key(compare))))

s = sum(int(hand[1]) * (i + 1) for i, hand in enumerate(sorted_hands))
print(s)
