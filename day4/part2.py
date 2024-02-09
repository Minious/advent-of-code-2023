f = open("input.txt", "r")

s = 0

lines = list(f)
scratchcards = [1 for _ in range(len(lines))]

for i, line in enumerate(lines):
    winning_number = [int(n) for n in line[10:].split('|')[
        0].split(" ") if n != ""]
    numbers_i_have = [int(n) for n in line[10:].split('|')[
        1].split(" ") if n != ""]
    points = len([n for n in numbers_i_have if n in winning_number])
    for j in range(i + 1, i + points + 1):
        scratchcards[j] += scratchcards[i]

print(sum(scratchcards))
