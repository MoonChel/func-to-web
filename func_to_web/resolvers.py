from __future__ import annotations

import enum
from typing import Type, Any, Dict, List, get_type_hints
from dataclasses import is_dataclass, dataclass, field, asdict

from logging import getLogger

logger = getLogger(__name__)


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
    type: PYTHON_TYPE
    fields: List[ArgSchema] = field(default_factory=list)


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
