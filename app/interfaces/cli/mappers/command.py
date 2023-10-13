from ...commands import *

def add_new_reading(context, request, app_context, **kwargs):
    return AddNewReading(dict(
        name = request.get('name', None),
        date = request.get('date', None),
        input = request.get('input', None),
        type = request.get('type', None),
        frequency = request.get('frequency', None),
        dimension = request.get('dimension', None)
    ))