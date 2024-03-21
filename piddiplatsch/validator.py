from jsonschema import FormatChecker
from jsonschema import validate as _validate

import pyhandle
from pyhandle.handleexceptions import HandleSyntaxError

# HINT: See docs how to customize the default validator:
#
# https://lat.sk/2017/03/custom-json-schema-type-validator-format-python/
# https://stackoverflow.com/questions/76602725/programmatic-python-format-check-in-jsonschema

format_checker = FormatChecker()


@format_checker.checks("handle", HandleSyntaxError)
def check_handle(value):
    return pyhandle.utilhandle.check_handle_syntax(value)


def validate(data, schema):
    _validate(data, schema, format_checker=format_checker)
