f = open("input.txt", "r")
s = 0
for line in f:
    digits = [c for c in line if c.isdigit()]
    s += int(digits[0] + digits[-1])
print(s)