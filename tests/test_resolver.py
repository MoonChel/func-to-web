from __future__ import annotations
from dataclasses import dataclass

from func_to_web.function_to_web import build_function_schema
from func_to_web.resolvers import ArgSchema, build_argument_schema, PYTHON_TYPE


def test_build_argument_schema_simple():
    @dataclass
    class DummyObject:
        param_1: str
        param_2: int

    expected_schema = ArgSchema(name="a", type=PYTHON_TYPE.string.value)

    assert expected_schema == build_argument_schema(arg_name="a", arg_type=str)
