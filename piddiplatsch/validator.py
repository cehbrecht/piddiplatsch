from jsonschema import Draft202012Validator
from jsonschema import validate as _validate
from jsonschema.exceptions import ValidationError

import pyhandle

# https://lat.sk/2017/03/custom-json-schema-type-validator-format-python/
# https://stackoverflow.com/questions/76602725/programmatic-python-format-check-in-jsonschema


@Draft202012Validator.FORMAT_CHECKER.checks("handle", ValidationError)
def check_handle(value):
    raise ValidationError("bka")
    if not pyhandle.utilhandle.check_handle_syntax(value):
        yield ValidationError(f"'{value}' is not a valid handle")


def validate(data, schema):
    _validate(data, schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
