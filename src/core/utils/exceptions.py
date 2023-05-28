SomeError = Exception


def get_error_name(err: SomeError):
    """
    Error의 status를 class name str로 나타내기 위함.
    ApiPayload.status로 접근 가능한 문자열
    """
    return err.__class__.__name__
