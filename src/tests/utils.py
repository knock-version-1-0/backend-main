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
        response = consumer.create(request)
    except Exception as exc:
        response = consumer.handle_exception(exc)

    return response
