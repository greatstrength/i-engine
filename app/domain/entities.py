from .value_objects import *

class Trigram(Model):
    id = t.StringType()
    name = t.StringType()
    element = t.StringType()
    yarrow_value = t.StringType()
    position = t.IntType()

class Hexagram(Model):

    class Line(Model):
        text = t.ListType(t.StringType())
        type = t.StringType(choices=['reminder', 'warning'])
        yarrow_value = t.IntType(choices=[6, 9])

    name = t.StringType(required=True)
    secondary_names = t.ListType(t.StringType())
    wilhelm_index = t.IntType(required=True)
    yarrow_value = t.StringType(required=True)
    judgement = t.ListType(t.StringType())
    image = t.ListType(t.StringType())
    changing_lines = t.DictType(t.ModelType(Line))