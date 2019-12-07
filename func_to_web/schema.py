from __future__ import annotations

from typing import Callable, List, Type
from dataclasses import dataclass, field

from logging import getLogger

from .resolvers import PYTHON_TYPE, resolve_type


logger = getLogger(__name__)


@dataclass
class ArgSchema:
    name: str
    type: PYTHON_TYPE
    fields: List[ArgSchema] = field(default_factory=list)

    def as_dict(self):
        result = {"name": self.name, "type": self.type.name}

        if self.type == PYTHON_TYPE.dataclass:
            result["fields"] = [field.as_dict() for field in self.fields]

        return result


@dataclass
class FunctionSchema:
    name: str
    annotations: List[ArgSchema]
    description: str
    fully_qualified_name: str

    def as_dict(self):
        return {
            "name": self.name,
            "annotations": [arg_schema.as_dict() for arg_schema in self.annotations],
            "description": self.description,
            "fully_qualified_name": self.fully_qualified_name,
        }


def build_function_schema(function: Callable):
    annotations = []

    for arg_name, arg_type in function.__annotations__.items():
        arg_schema = build_argument_schema(arg_name, arg_type)
        annotations.append(arg_schema)

    fully_qualified_name = ".".join([function.__module__, function.__name__])

    schema = FunctionSchema(
        name=function.__name__,
        annotations=annotations,
        description=function.__doc__,
        fully_qualified_name=fully_qualified_name,
    )

    return schema


def build_argument_schema(arg_name: str, arg_type: Type) -> ArgSchema:
    python_type = resolve_type(arg_type)
    schema = ArgSchema(name=arg_name, type=python_type)

    # recursivly resolve dataclass types
    if python_type == PYTHON_TYPE.dataclass:
        try:
            hints = get_type_hints(arg_type)
        except NameError:
            logger.warning("Please check if 'type' is available globally")
            raise

        for class_field_name, class_field_type in hints.items():
            schema.fields.append(
                build_argument_schema(class_field_name, class_field_type)
            )

    return schema
