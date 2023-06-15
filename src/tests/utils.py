import json


def ws_response(consumer, method, data=None, token=None, key=None):
    if not data:
        data = {}

    request_data = {
        'data': json.dumps(data),
        'authorization': f'Token {token}' if token else None,
        'key': key,
        'method': method
    }
    message = json.dumps(request_data)
    request = consumer.get_request({'message': message})
    handler = consumer.get_handler()
    if handler:
        try:
            consumer.initial(request)
            response = handler(request)
        except Exception as exc:
            response = consumer.handle_exception(exc)

    return response
