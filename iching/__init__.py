from schematics import Model, types as t

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


def print_lines(y_composite: list):
    for sum in y_composite:
        print(YARROW_SUM_TO_LINES[sum])

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
    composite_2d = composite_to_composite_2d(composite)
    print(composite)
    print_lines(composite)
    print(composite_2d)

read_data('mad_bladder_2022_09_03', '8d')
