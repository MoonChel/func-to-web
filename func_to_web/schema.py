from typing import Callable, Dict
from dataclasses import asdict

from .resolvers import build_argument_schema


def build_function_schema(function: Callable):
    annotations = []

    for arg_name, arg_type in function.__annotations__.items():
        arg_schema = build_argument_schema(arg_name, arg_type)
        annotations.append(asdict(arg_schema))

    fully_qualified_name = ".".join([function.__module__, function.__name__])

    schema = {
        "name": function.__name__,
        "annotations": annotations,
        "description": function.__doc__,
        "fully_qualified_name": fully_qualified_name,
    }

    return schema


class FunctionRegistry:
    def __init__(self):
        self.schema = {}

    def register(self, function: Callable):
        self.schema[function] = build_function_schema(function)

    def get_function(self, fully_qualified_name):
        for function, schema in self.schema.items():
            if schema["fully_qualified_name"] == fully_qualified_name:
                return function

    def as_dict(self):
        return {
            schema["fully_qualified_name"]: schema for schema in self.schema.values()
        }
