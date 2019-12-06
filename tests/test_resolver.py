from __future__ import annotations
from dataclasses import dataclass

from func_to_web.schema import build_function_schema
from func_to_web.resolvers import ArgSchema, build_argument_schema, PYTHON_TYPE

import pytest


@dataclass
class FirstLevelGlobal:
    param_1: str
    param_2: int


@dataclass
class SecondLevelGlobal:
    param_1: str
    first: FirstLevelGlobal


class TestBuildArgumentSchema:
    def test_dataclass_field_type(self):
        @dataclass
        class Dummy:
            param_1: str

        assert Dummy.__annotations__["param_1"] == "str"

    def test_build_argument_schema_simple(self):
        expected_schema = ArgSchema(name="a", type=PYTHON_TYPE.string)

        assert expected_schema == build_argument_schema(arg_name="a", arg_type=str)

    def test_build_argument_schema_dataclass(self):
        @dataclass
        class Dummy:
            param_1: str
            param_2: int

        expected_schema = ArgSchema(
            name="dummy",
            type=PYTHON_TYPE.dataclass,
            fields=[
                ArgSchema(name="param_1", type=PYTHON_TYPE.string),
                ArgSchema(name="param_2", type=PYTHON_TYPE.integer),
            ],
        )

        assert expected_schema == build_argument_schema(
            arg_name="dummy", arg_type=Dummy
        )

    def test_build_argument_schema_recursive(self):
        expected_schema = ArgSchema(
            name="second",
            type=PYTHON_TYPE.dataclass,
            fields=[
                ArgSchema(name="param_1", type=PYTHON_TYPE.string),
                ArgSchema(
                    name="first",
                    type=PYTHON_TYPE.dataclass,
                    fields=[
                        ArgSchema(name="param_1", type=PYTHON_TYPE.string),
                        ArgSchema(name="param_2", type=PYTHON_TYPE.integer),
                    ],
                ),
            ],
        )

        assert expected_schema == build_argument_schema(
            arg_name="second", arg_type=SecondLevelGlobal
        )

    def test_build_argument_schema_raise_name_error(self):
        @dataclass
        class FirstLevel:
            param_1: str
            param_2: int

        @dataclass
        class SecondLevel:
            param_1: str
            first: FirstLevel

        with pytest.raises(NameError):
            build_argument_schema(arg_name="second", arg_type=SecondLevel)
