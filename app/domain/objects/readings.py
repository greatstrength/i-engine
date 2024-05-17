from ...core.domain import *
from ..constants import *


class ResultLine(ValueObject):

    position = t.IntType(required=True)
    heaven_line = t.IntType(required=True)
    man_line = t.IntType(required=True)
    earth_line = t.IntType(required=True)
    line_value = t.IntType(required=True, choices=RESULT_LINE_VALUES)


class HexagramResult(ValueObject):

    name = t.StringType(required=True)
    wilhelm_index = t.IntType(required=True)


class ReadingResult(Entity):

    name = t.StringType(required=True)
    dimension = t.StringType(required=True, choices=READING_RESULT_DIMENSIONS)
    frequency = t.StringType(default=READING_RESULT_FREQUENCY_DEFAULT, choices=READING_RESULT_FREQUENCIES)
    type = t.StringType(default=READING_RESULT_TYPE_DEFAULT, choices=READING_RESULT_TYPES)
    date = t.DateType(required=True)
    result_lines = t.ListType(t.ModelType(ResultLine))
    current_or_previous = t.ModelType(HexagramResult)
    next = t.ModelType(HexagramResult)