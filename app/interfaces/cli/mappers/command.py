from ....features.objects import *

def map_request_input(request):
    request_input = request.get('input', None)
    if request_input:
        input = []
        for i in range(0, 18, 3):
            row = [int(request_input[i]), int(request_input[i + 1]), int(request_input[i + 2])]
            input.append(row)
        return input

def add_new_reading(context, request, app_context, **kwargs):
    request['input'] = map_request_input(request)
    
    return AddNewReading(dict(
        **request
    ), strict=False)

def add_reading_results(context, request, app_context, **kwargs):
    request['input'] = map_request_input(request)
    return AddReadingResults(dict(
        **request
    ), strict=False)

def print_new_reading_result(context, request, app_context, **kwargs):
    return PrintReading(dict(
        reading_id=context.result.id,
        **kwargs
    ), strict=False)