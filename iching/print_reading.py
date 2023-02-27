from .models import *
from .constants import *

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