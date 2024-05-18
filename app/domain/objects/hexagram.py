from ...core.domain import *
from ..constants import *


class Hexagram(ValueObject):

    class Line(ValueObject):

        text = t.ListType(t.StringType())
        yarrow_value = t.IntType(choices=HEXAGRAM_YARROW_VALUES)
        line_number = t.IntType(choices=HEXAGRAM_LINE_NUMBERS)

    name = t.StringType(required=True)
    secondary_names = t.ListType(t.StringType())
    number = t.IntType(required=True)
    judgement = t.ListType(t.StringType())
    image = t.ListType(t.StringType())
    changing_lines = t.ListType(t.ModelType(Line))