import json


def ws_response(consumer, data, token=None, key=None):
    request_data = {
        'data': json.dumps(data),
        'authorization': f'Token {token}' if token else None,
        'key': key
    }
    message = json.dumps(request_data)
    request = consumer.get_request({'message': message})

    try:
        consumer.initial(request)
        for method_name in consumer.get_crud_method_names():
            handler = getattr(consumer, method_name, None)
            if handler:
                break
        response = handler(request)
    except Exception as exc:
        response = consumer.handle_exception(exc)

    return response
