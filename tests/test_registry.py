import pytest
from func_to_web.schema import FunctionRegistry


@pytest.fixture(scope="function")
def registry():
    return FunctionRegistry()


def hello(name: str) -> str:
    """
    hello
    test
    """
    return "Hello " + name


def test_registry(registry: FunctionRegistry):
    registry.register(hello)

    assert hello in registry.schema


def test_registry_as_dict(registry: FunctionRegistry):
    registry.register(hello)

    expected_dict = {
        "tests.test_registry.hello": {
            "name": "hello",
            "description": hello.__doc__,
            "fully_qualified_name": "tests.test_registry.hello",
            "annotations": [
                {"name": "name", "type": "string"},
                {"name": "return", "type": "string"},
            ],
        }
    }

    assert expected_dict == registry.as_dict()
