import argparse

from iching import *

parser = argparse.ArgumentParser('I-Ching Engine')
parser.add_argument('-d', '--dimension', default='8')
parser.add_argument('-i', '--input', nargs='+', required=True)

args = parser.parse_args()
transform = get_yarrow_transform(args.dimension)

data = []
input = args.input
for i in range(0, 18, 3):
    row = [input[i], input[i + 1], input[i + 2]]
    data.append(row)

yarrow = input_to_yarrow(data, transform)
composite = yarrow_to_composite(yarrow)
is_changing, previous, next = composite_to_composite_2d(composite)

print('\n')
if is_changing:
    print_changing_hexagran(composite, previous, next)
else:
    print_single_hexagram(previous)
