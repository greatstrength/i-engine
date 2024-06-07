from ....features.objects import *


def default(context, request, app_context, **kwargs):
    from importlib import import_module
    request_type = kwargs.get('request_type', None)
    if not request_type:
        return None
    
    if len(request_type.split('.')) <= 1:
        module_path = 'app.features.objects.requests'
    else: 
        module_path = '.'.join(request_type.split('.')[:-1])
        request_type = request_type.split('.')[-1]
    
    request_obj = getattr(import_module(module_path), request_type)

    return request_obj(dict(
        **request
    ), strict=False)


def print_new_reading_result(context, request, app_context, **kwargs):
    return PrintReading(dict(
        reading_id=context.result.id,
        **kwargs
    ), strict=False)
