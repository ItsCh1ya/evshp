def type_validation(data: dict, format: dict):
    return all([type(value) is format[key] for key, value in data.items()])

def strings_validation(strings: list):    
    for string in strings:
        if len(string) == 0:
            return False
        if "$" in string:
            return False
    return True