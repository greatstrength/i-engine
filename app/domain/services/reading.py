from ..constants import *
from ..objects import *

from datetime import date, datetime


def create_transform(dimension: str):
    if dimension == '2':
        return TWO_D_TRANSFORM
    if dimension == '2.1':
        return TWO_D_EXT_1_TRANSFORM
    if dimension == '2.2':
        return TWO_D_EXT_2_TRANSFORM
    if dimension == '6':
        return SIX_D_TRANSFORM
    if dimension == '8':
        return EIGHT_D_TRANSFORM
    if dimension == '49':
        return FORTY_NINE_D_TRANSFORM
    return None


def calculate_sum_transform(dimension: str, input_data: list):

    # Default transform strategy.
    def default_transform_strategy(
            input_data: list,
            transform: dict = TWO_D_TRANSFORM
    ):
        y_transform = []
        for H, M, E in input_data:
            y_transform.append((transform[H], transform[M], transform[E]))
        return y_transform

    # Traditional transform strategy based on the 50-yarrow-rod method.
    def traditional_transform_strategy(
        input_data: list,
        transform: dict = FORTY_NINE_D_TRANSFORM
    ):

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
            y_transform.append((transform[H], transform[M], transform[E]))
        return y_transform

    # Create transform based on dimension.
    transform = create_transform(dimension)

    # If transform is None, return None.
    if transform is None:
        return None

    # Calculate transform based on dimension.
    if dimension == '49':
        transform = traditional_transform_strategy(input_data)
    else:
        transform = default_transform_strategy(input_data, transform)

    # Return the sum of the transform.
    return [sum(row) for row in transform]


def create_reading_result(
    name,
    dimension: str,
    reading_date: date = None,
    frequency: str = READING_RESULT_FREQUENCY_DEFAULT,
    **kwargs
) -> ReadingResult:

    # Set date to today if not provided
    if not reading_date:
        reading_date = datetime.now().date()

    result = ReadingResult(dict(
        id=name,
        name=name,
        date=datetime.strptime(
            reading_date, '%Y-%m-%d') if isinstance(reading_date, str) else reading_date,
        dimension=dimension,
        frequency=frequency,
    ))

    return result


def create_result_lines(input: List[List[int]], transform: List[int]) -> List[ResultLine]:
    
    # Format data
    position = 6
    result_lines = []
    for i in range(0, 6):
        result_line = ResultLine(dict(
            position=position,
            heaven_value=input[i][0],
            man_value=input[i][1],
            earth_value=input[i][2],
            line_value=transform[i]
        ))
        result_lines.append(result_line)
        position -= 1
    return result_lines
