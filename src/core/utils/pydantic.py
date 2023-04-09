from typing import (
    Any,
)

from pydantic import validate_model
from pydantic.error_wrappers import ValidationError


object_setattr = object.__setattr__
MISSING = 'value_error.missing'


class RequestBody:
    """
    If you wish to exclude validation for missing fields of the BaseModel,
    you can inherit from the RequestBody class.\n
    It is crucial to align the order of inheritance correctly
    to ensure that the validation is not applied to the fields of the BaseModel.\n
    To do this, you can follow the example shown below:

    For example:
    class Model(RequestBody, BaseModel): ...

    Please make sure that the RequestBody class is inherited before the BaseModel class.
    """

    def __init__(__pydantic_self__, **data: Any) -> None:
        """
        Create a new model by parsing and validating input data from keyword arguments.

        Raises ValidationError if the input data cannot be parsed to form a valid model.
        """
        # Uses something other than `self` the first arg to allow "self" as a settable attribute
        values, fields_set, validation_error = validate_model(__pydantic_self__.__class__, data)

        if validation_error:
            _errors = []
            for e in validation_error.errors():
                if e['type'] == MISSING:
                    continue
                _errors.append(e)
            if len(_errors) > 0:
                raise ValidationError(_errors, validation_error.model)
        try:
            object_setattr(__pydantic_self__, '__dict__', values)
        except TypeError as e:
            raise TypeError(
                'Model values must be a dict; you may not have returned a dictionary from a root validator'
            ) from e
        object_setattr(__pydantic_self__, '__fields_set__', fields_set)
        __pydantic_self__._init_private_attributes()