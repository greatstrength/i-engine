from ...core import *
from ...domain import *


def handle(context: MessageContext):
    from ...constants import YARROW_SUM_TO_LINES

    # Unpack request
    name = context.data.name
    reading_date = context.data.date
    frequency = context.data.frequency
    dimension = context.data.dimension
    input = context.data.input

    # Load reading cache repository.
    reading_cache: ReadingCache = context.services.reading_cache()

    # Load reading repository.
    reading_repo: ReadingRepository = context.services.reading_repo()

    # Load the hexagram repository.
    hexagram_repo: HexagramRepository = context.services.hexagram_repo()

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
            changing_line: ChangingLine = hex.changing_lines[line - 1]
            
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
    
    # Calculate summed transform.
    transform = reading_service.calculate_sum_transform(dimension, input)

    # Create reading result.
    reading_result = reading_service.create_reading_result(name, input, dimension, transform, reading_date, frequency)

    # Save reading result to cache.
    try:
        reading_repo.save(reading_result)
    except Exception as e:
        reading_cache.save(reading_result)
        raise e

    # Get reading hexagram.
    hex_number = hexagram_service.get_hexagram_number(reading_result)
    hexagram = hexagram_repo.get(hex_number)

    # Get changing hexagram.
    changing_hex_number = hexagram_service.get_changing_hexagram_number(reading_result)
    if changing_hex_number:
        changing_hexagram = hexagram_repo.get(changing_hex_number)
    else:
        changing_hexagram = None

    # Set hexagrams to reading result.
    reading_repo.set_hexagrams(
        reading_result.id, 
        hexagram.id, 
        changing_hexagram.id if changing_hexagram else None
    )

    # Old Printing Method
    is_changing, previous, next = composite_to_composite_2d(transform)
    print('\n')
    if is_changing:
        print_changing_hexagran(transform, previous, next)
    else:
        print_single_hexagram(previous)