from dataclasses import dataclass

from func_to_web.resolvers import PYTHON_TYPE
from func_to_web.schema import ArgSchema, FunctionSchema, build_function_schema


def hello(name: str) -> str:
    """
    hello
    test
    """
    return "Hello " + name


@dataclass
class ReservationNumber:
    text: str


@dataclass
class ReservationStatus:
    text: str


@dataclass
class Reservation:
    reservation_number: ReservationNumber


def hello_reservation(reservation: Reservation) -> ReservationStatus:
    """
    get reservation status
    """
    return ReservationStatus("pending")


class TestBuildSchema:
    def test_build_function_schema_simple(self):
        expected_schema = FunctionSchema(
            name="hello",
            description=hello.__doc__,
            annotations=[
                ArgSchema(name="name", type=PYTHON_TYPE.string),
                ArgSchema(name="return", type=PYTHON_TYPE.string),
            ],
            fully_qualified_name="tests.test_schema.hello",
        )

        assert expected_schema == build_function_schema(function=hello)

    def test_build_function_schema_recursive_arguments(self):
        expected_schema = FunctionSchema(
            name="hello_reservation",
            description=hello_reservation.__doc__,
            fully_qualified_name="tests.test_schema.hello_reservation",
            annotations=[
                ArgSchema(
                    name="reservation",
                    type=PYTHON_TYPE.dataclass,
                    fields=[
                        ArgSchema(
                            name="reservation_number",
                            type=PYTHON_TYPE.dataclass,
                            fields=[ArgSchema(name="text", type=PYTHON_TYPE.string)],
                        )
                    ],
                ),
                ArgSchema(
                    name="return",
                    type=PYTHON_TYPE.dataclass,
                    fields=[ArgSchema(name="text", type=PYTHON_TYPE.string)],
                ),
            ],
        )

        assert expected_schema == build_function_schema(function=hello_reservation)
