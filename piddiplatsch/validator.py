from jsonschema import Draft202012Validator
from jsonschema import validate as _validate

# from jsonschema.exceptions import ValidationError

import pyhandle
from pyhandle.handleexceptions import HandleSyntaxError

# HINT: See docs how to customize the default validator:
#
# https://lat.sk/2017/03/custom-json-schema-type-validator-format-python/
# https://stackoverflow.com/questions/76602725/programmatic-python-format-check-in-jsonschema


@Draft202012Validator.FORMAT_CHECKER.checks("handle", HandleSyntaxError)
def check_handle(value):
    return pyhandle.utilhandle.check_handle_syntax(value)


def validate(data, schema):
    _validate(data, schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
