from ...core import *
from ...domain import *


def handle(context: MessageContext):
    from datetime import datetime, date
    from ...constants import TWO_D_YARROW_TRANSFORM, TRANSFORM, YARROW_SUM_TO_LINES

    # Unpack request
    name = context.data.name
    reading_date = context.data.date
    frequency = context.data.frequency
    dimension = context.data.dimension
    input = context.data.input

    # Load reading cache repository.
    reading_cache: ReadingCache = context.services.reading_cache()

    # Load the hexagram repository.
    hexagram_repo: HexagramRepository = context.services.hexagram_repo()

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

    def get_hexagram_value(composite: list) -> Hexagram:
        value = ''.join([str(i) for i in composite])
        number = YARROW_TO_HEXAGRAM_NUMBER[value]
        return hexagram_repo.get(number)

    def print_single_hexagram(composite):
        hex = get_hexagram_value(composite)

        print('{}. {}'.format(hex.number, hex.name))
        print('')
        print_lines(composite)
        print_judgement(hex)
        print_image(hex)

    def print_changing_hexagran(composite: list, previous: list, next: list):
        previous_hex = get_hexagram_value(previous)
        next_hex = get_hexagram_value(next)

        print('{}. {} -> {}. {}'.format(previous_hex.number, previous_hex.name, next_hex.number, next_hex.name))
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
            line = 6 - i
            changing_line: Hexagram.Line = hex.changing_lines[line - 1]
            
            print('\t{} in {} says:\n'.format(value, line))
            
            for line in changing_line.text.split('\n'):
                print('\t' + line)
            print('')
        print('')

    def print_judgement(hex: Hexagram, is_changing: bool = False):
        title = 'Judgement:'
        if is_changing:
            title = '\t' + title
        print(title)
        print('')
        for line in hex.judgement.split('\n'):
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
        for line in hex.image.split('\n'):
            if is_changing:
                line = '\t' + line
            print(line)
        print('\n')

    def create_reading_result(name, composite, previous, next, reading_date: date = None, frequency: str = READING_RESULT_FREQUENCY_DEFAULT) -> ReadingResult:
        # Format data
        position = 6
        input_data = []
        for i in range(0, 18, 3):
            input_data.append(dict(
                position=position,
                heaven_line=input[i],
                man_line=input[i + 1],
                earth_line=input[i + 2],
                line_value=composite[0 if i == 0 else int(i/3)]
            ))
            position -= 1
            
        previous_hex = get_hexagram_value(previous)
        previous_hex_data = dict(
            name=previous_hex.name,
            wilhelm_index=previous_hex.number,
        )
        if next:
            next_hex = get_hexagram_value(next)
            next_hex_data = dict(
                name=next_hex.name,
                wilhelm_index=next_hex.number,
            )
        else:
            next_hex_data = None

        # Set date to today if not provided
        if not reading_date:
            reading_date = datetime.now().date()

        return ReadingResult(dict(
            id=name,
            name=name,
            date=datetime.strptime(reading_date, '%Y-%m-%d'),
            dimension=dimension,
            frequency=frequency,
            result_lines=input_data,
            current_or_previous=previous_hex_data,
            next=next_hex_data
        ))
    
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

    reading_result = create_reading_result(name, composite, previous, next, reading_date, frequency)

    # Save reading result to cache.
    # reading_cache.save(reading_result)

    print('\n')
    if is_changing:
        print_changing_hexagran(composite, previous, next)
    else:
        print_single_hexagram(previous)