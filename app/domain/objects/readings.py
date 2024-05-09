from ...core.domain import *
from ..constants import *

class HexagramLine(ValueObject):

    text = t.ListType(t.StringType())
    type = t.StringType(choices=HEXAGRAM_LINE_TYPES)
    yarrow_value = t.IntType(choices=HEXAGRAM_YARROW_VALUES)
    line_number = t.IntType(choices=HEXAGRAM_LINE_NUMBERS)


class ResultLine(ValueObject):

    position = t.IntType(required=True)
    heaven_line = t.IntType(required=True)
    man_line = t.IntType(required=True)
    earth_line = t.IntType(required=True)
    line_value = t.IntType(required=True, choices=RESULT_LINE_VALUES)


class Hexagram(ValueObject):

    name = t.StringType(required=True)
    secondary_names = t.ListType(t.StringType())
    wilhelm_index = t.IntType(required=True)
    yarrow_value = t.StringType(required=True)
    judgement = t.ListType(t.StringType())
    image = t.ListType(t.StringType())
    changing_lines = t.ListType(t.ModelType(HexagramLine))


class HexagramResult(ValueObject):

    name = t.StringType(required=True)
    wilhelm_index = t.IntType(required=True)


class ReadingResult(Entity):

    name = t.StringType(required=True)
    dimension = t.StringType(required=True, choices=READING_RESULT_DIMENSIONS)
    frequency = t.StringType(default=READING_RESULT_FREQUENCY_DAILY, choices=READING_RESULT_FREQUENCIES)
    type = t.StringType(default=READING_RESULT_TYPE_GENERAL, choices=READING_RESULT_TYPES)
    date = t.DateType(required=True)
    result_lines = t.ListType(t.ModelType(ResultLine))
    current_or_previous = t.ModelType(HexagramResult)
    next = t.ModelType(HexagramResult)