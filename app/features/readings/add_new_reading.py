from ...core import *
from ...domain import *

def handle(context: MessageContext):
    from ...constants import TWO_D_YARROW_TRANSFORM, TRANSFORM, YARROW_SUM_TO_LINES

    # Unpack request
    name = context.data.name
    dimension = context.data.dimension
    input = context.data.input

    def load_hexagrams():
        import yaml
        with open('app/hexagrams.yml') as hex_file:
            hex_data = yaml.safe_load(hex_file)
            hex_list = [Hexagram(hex) for _, hex in hex_data.items()]
            return { hex.yarrow_value: hex for hex in hex_list}

    def get_yarrow_transform(transform_name: str):
        return TRANSFORM[transform_name]

    def input_to_yarrow(input_data: list, transform: dict = TWO_D_YARROW_TRANSFORM):
        y_transform = []
        for H, M, E in input_data:
            y_transform.append((transform[H], transform[M], transform[E]))
        return y_transform

    def input_to_yarrow_traditional(input_data: list, transform: dict):
        import math

        def get_value(pile: int):
            value = pile % 4
            if value == 0:
                value = 4
            return value

        y_transform = []
        for row in input_data:
            counter = 49
            new_row = [1, 1, 1]
            for i in range(len(row)):
                split = int(row[i])
                left = abs(counter - split)
                if counter > split:
                    right = split - 1
                else:
                    right = counter - left - 1
                new_row[i] += get_value(left) + get_value(right)
                counter -= new_row[i]
            H, M, E = new_row
            y_transform.append((transform[str(H)], transform[str(M)], transform[str(E)]))
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
        
    hex_lookup = load_hexagrams()

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

    def print_changing_lines(composite: list, hex: Hexagram):
        print('Changing Lines:\n')
        for i in reversed(range(6)):
            value = composite[i]
            if value not in [6, 9]:
                continue
            elif value == 6:
                value = 'Six'
            else:
                value = 'Nine'
            line = str(6 - i)
            changing_line: Hexagram.Line = hex.changing_lines[line]
            
            print('\t{} in {} is a {}:\n'.format(value, line, changing_line.type))
            
            for line in changing_line.text:
                print('\t' + line)
            print('')
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

    transform = get_yarrow_transform(dimension)

    data = []
    for i in range(0, 18, 3):
        row = [input[i], input[i + 1], input[i + 2]]
        data.append(row)

    if dimension == '49':
        yarrow = input_to_yarrow_traditional(data, transform)
    else:
        yarrow = input_to_yarrow(data, transform)
    composite = yarrow_to_composite(yarrow)
    is_changing, previous, next = composite_to_composite_2d(composite)

    def save_reading_result()

    print('\n')
    if is_changing:
        print_changing_hexagran(composite, previous, next)
    else:
        print_single_hexagram(previous)