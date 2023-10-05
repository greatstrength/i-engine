from ..core.domain import *
from .constants import *


class Hexagram(ValueObject):
	name = t.StringType(required=True)
	secondary_names = t.ListType(t.StringType())


class HexagramLine(ValueObject):
	pass


class ResultLine(ValueObject):
	position = t.IntType(required=True)
	heaven_line = t.IntType(required=True)
	man_line = t.IntType(required=True)
	earth_line = t.IntType(required=True)
	line_value = t.IntType(required=True, choices=[6, 7, 8, 9])