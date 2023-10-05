from ..core.domain import *
from .constants import *


class Hexagram(ValueObject):
	pass


class HexagramLine(ValueObject):
	pass


class ResultLine(ValueObject):
	position = t.IntType(required=True)
	heaven_line = t.IntType(required=True)
	man_line = t.IntType(required=True)
	earth_line = t.IntType(required=True)
	line_value = t.IntType(required=True, choices=[6, 7, 8, 9])