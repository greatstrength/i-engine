from .. import *

cache = {}

def list():
    return cache.get('cli')
    