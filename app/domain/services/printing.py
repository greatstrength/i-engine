from .. import *


def composite_to_composite_2d(result_lines: List[ResultLine]):
    is_changing = False
    composite = [line.line_value for line in result_lines]
    current = []
    changing = []
    for value in composite:
        if value in [6, 9]:
            is_changing = True
        if value == 6:
            current.append(8)
            changing.append(7)
        elif value == 9:
            current.append(7)
            changing.append(8)
        else:
            current.append(value)
            changing.append(value)
        return (is_changing, composite, current, changing)


def get_hexagram_number(composite: list) -> Hexagram:
    value = ''.join([str(i) for i in composite])
    number = YARROW_TO_HEXAGRAM_NUMBER[value]
    return number


def print_single_hexagram(composite: List[int], hexagram: Hexagram):

    print('{}. {}'.format(hexagram.number, hexagram.name))
    print('')
    print_lines(composite)
    print_judgement(hexagram)
    print_image(hexagram)


def print_changing_hexagran(
    composite: List[int],
    hexagram: Hexagram,
    changing_hexagram: Hexagram
):

    print('{}. {} -> {}. {}'.format(
        hexagram.number,
        hexagram.name,
        changing_hexagram.number,
        changing_hexagram.name
    ))
    print('')

    print_lines(composite, True, next)

    print('Previous:\n')
    print_judgement(hexagram, True)
    print_image(hexagram, True)
    print_changing_lines(composite, hexagram)

    print('Next:\n')
    print_judgement(changing_hexagram, True)
    print_image(changing_hexagram, True)


def print_lines(composite: list, is_changing: bool = False, next: list = None):
    if not is_changing:
        for sum in composite:
            print(TRANSFORM_SUM_TO_LINES[sum])
        print('')
        return
    line_format = '{}{}{}'
    for i in range(6):
        previous_line = TRANSFORM_SUM_TO_LINES[composite[i]]
        next_line = TRANSFORM_SUM_TO_LINES[next[i]]
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
