import re

f = open("input.txt", "r")

red = 12
green = 13
blue = 14

s = 0

for line in f:
    no_whitespace_line = "".join(c for c in line if c != " ")
    game_id_str, games_str = no_whitespace_line.split(":")
    game_id = int(re.search("[0-9]+", game_id_str).group())
    games = games_str.split(";")
    draws = [re.findall("[0-9]+|green|red|blue", draw)
             for game in games for draw in game.split(",")]
    possible = True
    for draw in draws:
        match draw[1]:
            case "red":
                if int(draw[0]) > red:
                    possible = False
                    break
            case "blue":
                if int(draw[0]) > blue:
                    possible = False
                    break
            case "green":
                if int(draw[0]) > green:
                    possible = False
                    break
    if possible:
        s += game_id
print(s)
