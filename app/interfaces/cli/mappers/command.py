from .. import *

def add_new_reading(context, request, app_context, **kwargs):
    request_input = request.get('input', None)
    if request_input:
        input = []
        for i in range(0, 18, 3):
            row = [int(request_input[i]), int(request_input[i + 1]), int(request_input[i + 2])]
            input.append(row)
        request['input'] = input
    
    return AddNewReading(dict(
        **request
    ), strict=False)