def limitDecimals(number, decimals):
    return int(number * 10 ** decimals) / 10 ** decimals

def convert(raw):
    return raw / 10 ** 30
