def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False