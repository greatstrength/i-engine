from .constants import *
from .print_reading import *

def load_hexagrams():
    import yaml
    with open('iching/hexagrams.yml') as hex_file:
        hex_data = yaml.safe_load(hex_file)
        hex_list = [Hexagram(hex) for _, hex in hex_data.items()]
        return { hex.yarrow_value: hex for hex in hex_list}

hex_lookup = load_hexagrams()

def get_yarrow_transform(transform_name: str):
    return TRANSFORM[transform_name]

def input_to_yarrow(input_data: list, transform: dict = TWO_D_YARROW_TRANSFORM):
    y_transform = []
    for H, M, E in input_data:
        y_transform.append((transform[H], transform[M], transform[E]))
    return y_transform

def yarrow_to_composite(y_transform: list):
    composite = [sum(row) for row in y_transform]
    return composite

def composite_to_composite_2d(composite):
    previous = []
    next = []
    for value in composite:
        if value == 6:
            previous.append(8)
            next.append(7)
        elif value == 9:
            previous.append(7)
            next.append(8)
        else:
            previous.append(value)
            next.append(value)
    if previous == next:
        return (False, previous, next)
    else:
        return (True, previous, next)

def print_single_hexagram(composite):
    yarrow_value = ''.join([str(i) for i in composite])
    hex = hex_lookup[yarrow_value]

    print('{}. {}'.format(hex.wilhelm_index, hex.name))
    print('')
    print_lines(composite)
    print_judgement(hex)
    print_image(hex)

def print_changing_hexagran(composite: list, previous: list, next: list):
    previous_value = ''.join([str(i) for i in previous])
    previous_hex = hex_lookup[previous_value]

    next_value = ''.join([str(i) for i in next])
    next_hex = hex_lookup[next_value]

    print('{}. {} -> {}. {}'.format(previous_hex.wilhelm_index, previous_hex.name, next_hex.wilhelm_index, next_hex.name))
    print('')

    print_lines(composite, True, next)

    print('Previous:\n')
    print_judgement(previous_hex, True)
    print_image(previous_hex, True)
    print_changing_lines(composite, previous_hex)

    print('Next:\n')
    print_judgement(next_hex, True)
    print_image(next_hex, True)
