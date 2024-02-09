import functools

f = open("input.txt", "r")

s = 0

lines = list(f)
times = [int(t) for t in lines[0].split(" ")[1:] if t != ""]
distances = [int(d) for d in lines[1].split(" ")[1:] if d != ""]

wins = []
for time, best_distance in zip(times, distances):
    win_count = 0
    for held_time in range(time):
        moving_time = time - held_time
        distance = moving_time * held_time
        if distance > best_distance:
            win_count += 1
    wins.append(win_count)

res = functools.reduce(lambda a, b: a * b, wins, 1)
print(res)
