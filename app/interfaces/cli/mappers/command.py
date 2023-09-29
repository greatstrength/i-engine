from ...commands import *

def add_new_reading(context, request, app_context, **kwargs):
    return AddNewReading(dict(
        input = request.input,
        dimension = request.dimension
    ))