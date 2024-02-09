f = open("input.txt", "r")

s = 0

for line in f:
    winning_number = [int(n) for n in line[10:].split('|')[
        0].split(" ") if n != ""]
    numbers_i_have = [int(n) for n in line[10:].split('|')[
        1].split(" ") if n != ""]
    points = len([n for n in numbers_i_have if n in winning_number])
    if points > 0:
        s += pow(2, points - 1)
print(s)
