import re


def to_digit(word):
    match word:
        case "one":
            return "1"
        case "two":
            return "2"
        case "three":
            return "3"
        case "four":
            return "4"
        case "five":
            return "5"
        case "six":
            return "6"
        case "seven":
            return "7"
        case "eight":
            return "8"
        case "nine":
            return "9"


f = open("input.txt", "r")
s = 0
for line in f:
    digits_tmp = re.findall(
        "(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))", line)
    digits = [c if c.isdigit() else to_digit(c) for c in digits_tmp]
    s += int(digits[0] + digits[-1])
print(s)
