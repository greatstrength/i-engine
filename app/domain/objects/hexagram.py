from ...core.domain import *
from ..constants import *


class Hexagram(ValueObject):

    class Line(ValueObject):

        text = t.StringType()
        yarrow_value = t.IntType(choices=HEXAGRAM_YARROW_VALUES)
        line_number = t.IntType(choices=HEXAGRAM_LINE_NUMBERS)

    name = t.StringType(required=True)
    number = t.IntType(required=True)
    external_id = t.StringType()
    secondary_names = t.ListType(t.StringType())
    judgement = t.StringType()
    image = t.StringType()
    changing_lines = t.ListType(t.ModelType(Line), default=[])