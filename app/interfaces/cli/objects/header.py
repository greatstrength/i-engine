from aikicore.objects.header import *

class IChingCliHeader(Header):

    command = t.StringType(required=True)
    function = t.StringType(required=True)
    env = t.StringType(required=True)