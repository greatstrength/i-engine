from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

from ..constants import *
from ..domain import *

class AddNewReading(Model):

    name = t.StringType(required=True)
    date = t.StringType()
    dimension = t.StringType(required=True, choices=READING_RESULT_DIMENSIONS)
    input = t.ListType(t.IntType(), required=True, min_size=6, max_size=18)
    type = t.StringType(default=READING_RESULT_TYPE_DEFAULT, choices=READING_RESULT_TYPES)
    frequency = t.StringType(default=READING_RESULT_FREQUENCY_DEFAULT, choices=READING_RESULT_FREQUENCIES)
