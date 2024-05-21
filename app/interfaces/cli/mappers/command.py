from ...commands import *

def add_new_reading(context, request, app_context, **kwargs):
    data = AddNewReading(dict(
        name = request.get('name', None),
        date = request.get('date', None),
        type = request.get('type', None),
        frequency = request.get('frequency', None),
        dimension = request.get('dimension', None)
    ))

    input = request.get('input', None)
    if not input:
        return data
    
    for i in range(0, 18, 3):
        row = [int(input[i]), int(input[i + 1]), int(input[i + 2])]
        data.input.append(row)
    
    return data