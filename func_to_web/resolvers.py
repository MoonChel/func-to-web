from __future__ import annotations

import enum
from typing import Type, Any, Dict, List
from dataclasses import is_dataclass, dataclass, field


class PYTHON_TYPE(enum.Enum):
    string = str
    integer = int
    double = float
    boolean = bool
    dataclass = enum.auto()


STANDARD_TYPES = {
    PYTHON_TYPE.string.value: PYTHON_TYPE.string,
    PYTHON_TYPE.integer.value: PYTHON_TYPE.integer,
    PYTHON_TYPE.double.value: PYTHON_TYPE.double,
    PYTHON_TYPE.boolean.value: PYTHON_TYPE.boolean,
}


def is_standard_type(t: Type) -> bool:
    return t in STANDARD_TYPES


def resolve_type(t: Type) -> PYTHON_TYPE:
    if is_dataclass(t):
        return PYTHON_TYPE.dataclass
    elif is_standard_type(t):
        return STANDARD_TYPES[t]

    raise Exception(f"Type: '{t}' is not supported")


@dataclass
class ArgSchema:
    name: str
    type: str
    fields: List[ArgSchema] = field(default_factory=list)

    def as_dict(self):
        schema = {"name": self.name, "type": self.type}

        if self.fields:
            schema["fields"] = [arg_field.as_dict() for arg_field in self.fields]

        return schema


def build_argument_schema(arg_name: str, arg_type: Type) -> ArgSchema:
    python_type = resolve_type(arg_type)
    schema = ArgSchema(name=arg_name, type=python_type.name)

    # recursivly resolve dataclass types
    if python_type == PYTHON_TYPE.dataclass:
        for (
            dataclass_field_name,
            dataclass_field,
        ) in arg_type.__dataclass_fields__.items():
            schema.fields.append(
                build_argument_schema(dataclass_field_name, dataclass_field.type)
            )

    return schema
