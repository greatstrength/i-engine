from ..core.domain import *
from .constants import *


class HexagramLine(ValueObject):
	pass


class Hexagram(ValueObject):
	name = t.StringType(required=True)
	secondary_names = t.ListType(t.StringType())
	wilhelm_index = t.IntType(required=True)
	yarrow_value = t.StringType(required=True)
	judgement = t.ListType(t.StringType())
	image = t.ListType(t.StringType())
	changing_lines = t.ListType(t.ModelType(HexagramLine))


class ResultLine(ValueObject):
	position = t.IntType(required=True)
	heaven_line = t.IntType(required=True)
	man_line = t.IntType(required=True)
	earth_line = t.IntType(required=True)
	line_value = t.IntType(required=True, choices=[6, 7, 8, 9])