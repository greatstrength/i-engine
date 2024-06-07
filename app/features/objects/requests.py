from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

from .. import *

class AddNewReading(Model):

    name = t.StringType(required=True)
    date = t.StringType(serialized_name='reading_date')
    dimension = t.StringType(choices=READING_RESULT_DIMENSIONS)
    input = t.StringType(required=False, min_length=18, max_length=36)
    no_input = t.BooleanType(default=False)
    input_type = t.StringType(choices=READING_INPUT_TYPES, default=READING_INPUT_TYPE_STANDARD)
    type = t.StringType(default=READING_RESULT_TYPE_DEFAULT, choices=READING_RESULT_TYPES)
    frequency = t.StringType(default=READING_RESULT_FREQUENCY_DEFAULT, choices=READING_RESULT_FREQUENCIES)
    upload_file = t.StringType()
    remove_file = t.BooleanType(default=False)
    cache_only = t.BooleanType(default=False)


class AddReadingResults(Model):
    reading_id = t.StringType(required=True)
    input = t.StringType(required=False, min_length=18, max_length=36)
    input_type = t.StringType(choices=READING_INPUT_TYPES, default=READING_INPUT_TYPE_STANDARD)


class SyncReading(Model):
    reading_id = t.StringType(required=True)
    upload_file = t.StringType()
    remove_from_cache = t.BooleanType(default=False)


class UploadReadingFile(Model):
    reading_id = t.StringType(required=True)
    upload_file = t.StringType(required=True)
    remove_file = t.BooleanType(default=False)


class GetReadingByCategory(Model):
    date = t.StringType()
    type = t.StringType(choices=READING_RESULT_TYPES)
    frequency = t.StringType(choices=READING_RESULT_FREQUENCIES)
    to_json = t.BooleanType(default=False)


class PrintReading(Model):
    reading_id = t.StringType(required=True)
