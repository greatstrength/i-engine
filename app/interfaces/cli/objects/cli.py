from schematics import types as t, Model

class CliCommandExecution(Model):
    command = t.StringType(required=True)
    function = t.StringType(required=True)
    env = t.StringType()
    args = t.StringType()
    args_type = t.StringType(choices=['json'], default='json')
    debug = t.BooleanType(default=False, deserialize_from=['verbose'])