from ...core import *
from ..constants import *


class ResultLine(ValueObject):

    position = t.IntType(required=True)
    heaven_value = t.IntType(required=True)
    man_value = t.IntType(required=True)
    earth_value = t.IntType(required=True)
    line_value = t.IntType(required=True, choices=RESULT_LINE_VALUES)


class ReadingResult(Entity):

    name = t.StringType(required=True)
    date = t.DateType(required=True)
    dimension = t.StringType(required=True, choices=READING_RESULT_DIMENSIONS)
    frequency = t.StringType(default=READING_RESULT_FREQUENCY_DEFAULT, choices=READING_RESULT_FREQUENCIES)
    type = t.StringType(default=READING_RESULT_TYPE_DEFAULT, choices=READING_RESULT_TYPES)
    result_lines = t.ListType(t.ModelType(ResultLine))