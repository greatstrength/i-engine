from ....features.objects import *

def map_request_input(request):
    import json

    request_input = request.get('input', None)
    input_type = request.get('input_type', None)
    if not request_input:
        return None
    if input_type == READING_INPUT_TYPE_STANDARD:
        input = []
        for i in range(0, 18, 3):
            row = [int(request_input[i]), int(request_input[i + 1]), int(request_input[i + 2])]
            input.append(row)
        return input
    if input_type == READING_INPUT_TYPE_JSON:
        return json.loads(request_input[0])

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