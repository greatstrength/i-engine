from schematics import Model, types as t
import argparse

class Trigram(Model):
    id = t.StringType()
    name = t.StringType()
    element = t.StringType()
    yarrow_value = t.StringType()
    position = t.IntType()

class Hexagram(Model):

    class Line(Model):
        text = t.ListType(t.StringType())
        type = t.StringType(choices=['reminder', 'warning'])
        yarrow_value = t.IntType(choices=[6, 9])

    name = t.StringType(required=True)
    secondary_names = t.ListType(t.StringType())
    wilhelm_index = t.IntType(required=True)
    yarrow_value = t.StringType(required=True)
    judgement = t.ListType(t.StringType())
    image = t.ListType(t.StringType())
    changing_lines = t.DictType(t.ModelType(Line))


HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})
HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})
HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})
HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})
HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})
HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})
HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})
HEAVEN = Trigram({
    'id': 'heaven',
    'name': 'The Creative',
    'element': 'heaven',
    'yarrow_value': '777',
    'position': 1
})

TWO_D_YARROW_TRANSFORM = {
    False: 2,
    True: 3
}

SIX_D_YARROW_TRANSFORM = {
    '1': 3,
    '2': 2,
    '3': 3,
    '4': 2,
    '5': 3,
    '6': 2
}

EIGHT_D_YARROW_TRANSFORM = {
    '1': 3,
    '2': 2,
    '3': 3,
    '4': 2,
    '5': 3,
    '6': 2,
    '7': 3,
    '8': 2
} 

YARROW_SUM_TO_LINES = {
    6: '--- X ---',
    7: '---------',
    8: '---   ---',
    9: '---( )---'
}

def load_hexagrams():
    import yaml
    with open('iching/hexagrams.yml') as hex_file:
        hex_data = yaml.safe_load(hex_file)
        hex_list = [Hexagram(hex) for _, hex in hex_data.items()]
        return { hex.yarrow_value: hex for hex in hex_list}

hex_lookup = load_hexagrams()

def get_yarrow_transform(transform_name: str):
    TRANSFORM = {
        '2d': TWO_D_YARROW_TRANSFORM,
        '6d': SIX_D_YARROW_TRANSFORM,
        '8d': EIGHT_D_YARROW_TRANSFORM
    }
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


def print_lines(composite: list, is_changing: bool = False, next: list = None):
    if not is_changing:
        for sum in composite:
            print(YARROW_SUM_TO_LINES[sum])
        print('')
        return
    line_format = '{}{}{}'
    for i in range(6):
        previous_line = YARROW_SUM_TO_LINES[composite[i]]
        next_line = YARROW_SUM_TO_LINES[next[i]]
        if i == 2:
            middle = '     ---------\\     '
        elif i == 3:
            middle = '     ---------/     '
        else:
            middle = ' ' * 20
        print(line_format.format(previous_line, middle, next_line))
    print('')

def print_judgement(hex: Hexagram, is_changing: bool = False):
    title = 'Judgement:'
    if is_changing:
        title = '\t' + title
    print(title)
    print('')
    for line in hex.judgement:
        if is_changing:
            line = '\t' + line
        print(line)   
    print('\n')

def print_image(hex: Hexagram, is_changing: bool = False):
    title = 'Image:'
    if is_changing:
        title = '\t' + title
    print(title)
    print('')
    for line in hex.image:
        if is_changing:
            line = '\t' + line
        print(line)
    print('\n')

def print_changing_lines(composite: list, hex: Hexagram):
    print('Changing Lines:\n')
    for i in reversed(range(6)):
        value = composite[i]
        if value not in [6, 9]:
            continue
        line = str(6 - i)
        changing_line: Hexagram.Line = hex.changing_lines[line]
        
        print('\t{} in {} is a {}:'.format(value, line, changing_line.type))
        
        for line in changing_line.text:
            print('\t' + line)
        print('')
    print('')

def print_single_hexagram(composite):
    yarrow_value = ''.join([str(i) for i in composite])
    hex = hex_lookup[yarrow_value]

    print(hex.name)
    print('')
    print_lines(composite)
    print_judgement(hex)
    print_image(hex)

def print_changing_hexagran(composite: list, previous: list, next: list):
    previous_value = ''.join([str(i) for i in previous])
    previous_hex = hex_lookup[previous_value]

    next_value = ''.join([str(i) for i in next])
    next_hex = hex_lookup[next_value]

    print('{} -> {}'.format(previous_hex.name, next_hex.name))
    print('')

    print_lines(composite, True, next)

    print('Previous:\n')
    print_judgement(previous_hex, True)
    print_image(previous_hex, True)
    print_changing_lines(composite, previous_hex)

    print('Next:\n')
    print_judgement(next_hex, True)
    print_image(next_hex, True)
          
def read_test_data(test_data_name: str):
    import yaml
    with open('test/input_data.yml', 'r') as file:
        data = yaml.safe_load(file)
        try:
            return [data.split(', ') for data in data[test_data_name]]
        except:
            raise Exception('No test data!, {}'.format(test_data_name))

def read_data(test_data_name: str, transform_type: str = '2d'): 
    
    data = read_test_data(test_data_name)
    y_transform = get_yarrow_transform(transform_type)
    yarrow = input_to_yarrow(data, y_transform)
    composite = yarrow_to_composite(yarrow)
    is_changing, previous, next = composite_to_composite_2d(composite)

    if is_changing:
        print_changing_hexagran(composite, previous, next)
    else:
        print_single_hexagram(previous)


read_data('mad_bladder_2022_09_03', '8d')