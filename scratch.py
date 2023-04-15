def print_path_to_value(d, value, path = ''):
    for k, v in d.items():
        current_path = f"{path}.{k}" if path else k
        if v == value or k == value:
            print(current_path)
            return
        elif isinstance(v, dict):
            print_path_to_value(v, value, current_path)

data = {
    'a': {
        'b': {
            'c': {
                'd': 4
            },
            'e': 5
        },
        'f': {
            'g': 6
        }
    },
    'h': {
        'i': 7
    }
}
value = 7
print_path_to_value(data, value, 'parameters')
