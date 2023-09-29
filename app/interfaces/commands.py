from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

from ..constants import *

class AddNewReading(Model):

    name = t.StringType(required=True)
    dimension = t.StringType(default=DIMENSION_8, choices=DIMENSIONS)
    input = t.ListType(t.IntType(), required=True, min_size=6, max_size=18)
