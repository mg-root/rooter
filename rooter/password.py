import re

def getStrenghPassword(password):
    symbols = 0
    length = len(password)

    if re.search(r'[01]', password):
        symbols += 2

    if re.search(r'[0-9]', password):
        symbols += 10

    if re.search(r'[0-9A-F]', password):
        symbols += 16

    if re.search(r'[A-Z]', password):
        symbols += 26

    if re.search(r'[0-9A-Za-z]', password):
        symbols += 36

    if re.search(r'[A-Za-z]', password):
        symbols += 52

    if re.search(r'[0-9A-Za-z!#$*%?]', password):
        symbols += 62

    if re.search(r'[0-9A-Za-z!#$*%?&[|]@^µ§:/;.,<>°²³]', password):
        symbols += 70

    if length < 8:
        return 0
    elif length < 12:
        if symbols >= 52:
            return 2
        else:
            return 1
    elif length < 16:
        if symbols >= 62:
            return 2
        else:
            return 1
    else:
        if symbols >= 70:
            return 3
        else:
            return 2