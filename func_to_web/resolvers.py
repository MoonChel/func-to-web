import enum
from typing import List, Type
from dataclasses import is_dataclass


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
