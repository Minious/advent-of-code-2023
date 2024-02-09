import re

f = open("input.txt", "r")

s = 0

for line in f:
    no_whitespace_line = "".join(c for c in line if c != " ")
    game_id_str, games_str = no_whitespace_line.split(":")
    game_id = int(re.search("[0-9]+", game_id_str).group())
    games = games_str.split(";")
    draws = [re.findall("[0-9]+|green|red|blue", draw)
             for game in games for draw in game.split(",")]
    green = 0
    red = 0
    blue = 0
    for draw in draws:
        match draw[1]:
            case "red":
                if int(draw[0]) > red:
                    red = int(draw[0])
            case "blue":
                if int(draw[0]) > blue:
                    blue = int(draw[0])
            case "green":
                if int(draw[0]) > green:
                    green = int(draw[0])
    power = red * green * blue
    s += power
print(s)
