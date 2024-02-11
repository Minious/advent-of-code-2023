def hash(s):
    r = 0
    for c in s:
        r += ord(c)
        r *= 17
        r %= 256
    return r


f = open("input.txt", "r")

print(sum(hash(s) for s in f.read().split(",")))
