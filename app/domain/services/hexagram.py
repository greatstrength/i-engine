from ..constants import *
from ..objects import *


def get_hexagram_number(result_lines: List[ResultLine]) -> int:
    transform = []
    for line in result_lines:
        if line.line_value == 6:
            transform.append(8)
        elif line.line_value == 9:
            transform.append(7)
        else:
            transform.append(line.line_value)
    return YARROW_TO_HEXAGRAM_NUMBER[''.join([str(i) for i in transform])]


def get_changing_hexagram_number(result_lines: List[ResultLine]) -> int:
    transform = []
    for line in result_lines:
        if line.line_value == 6:
            transform.append(7)
        elif line.line_value == 9:
            transform.append(8)
        else:
            transform.append(line.line_value)
    return YARROW_TO_HEXAGRAM_NUMBER[''.join([str(i) for i in transform])]
