SomeError = Exception


def get_error_name(err: SomeError):
    return err.__name__
