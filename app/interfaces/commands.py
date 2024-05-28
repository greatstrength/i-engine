from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

from ..constants import *
from ..domain import *

class AddNewReading(Model):

    name = t.StringType(required=True)
    date = t.StringType()
    dimension = t.StringType(required=True, choices=READING_RESULT_DIMENSIONS)
    input = t.ListType(t.ListType(t.IntType(), min_size=3, max_size=3), min_size=6, max_size=6, default=[])
    type = t.StringType(default=READING_RESULT_TYPE_DEFAULT, choices=READING_RESULT_TYPES)
    frequency = t.StringType(default=READING_RESULT_FREQUENCY_DEFAULT, choices=READING_RESULT_FREQUENCIES)
    upload_file = t.StringType()
    remove_file = t.BooleanType(default=False)
    cache_only = t.BooleanType(default=False)


class SyncReading(Model):
    reading_id = t.StringType(required=True)
    upload_file = t.StringType()
    remove_from_cache = t.BooleanType(default=False)
