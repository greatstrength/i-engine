from ...core.domain import *
from ..constants import *


class ChangingLine(ValueObject):

    text = t.StringType()
    value = t.IntType(choices=HEXAGRAM_YARROW_VALUES)
    position = t.IntType(choices=HEXAGRAM_LINE_NUMBERS)


class Hexagram(Entity):

    name = t.StringType(required=True)
    number = t.IntType(required=True)
    secondary_names = t.ListType(t.StringType())
    judgement = t.StringType()
    image = t.StringType()
    changing_lines = t.ListType(t.ModelType(ChangingLine), default=[])