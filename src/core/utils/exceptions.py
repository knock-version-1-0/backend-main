SomeError = Exception


def get_error_name(err: SomeError):
    return err.__class__.__name__
