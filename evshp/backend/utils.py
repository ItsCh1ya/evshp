def type_validation(data, format):
    return all([type(value) is format[key] for key, value in data.items()])