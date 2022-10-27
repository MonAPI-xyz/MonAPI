def try_parse_int(string):
    try:
        return int(string)
    except ValueError:
        return False