from typing import Callable, Dict, Optional, NoReturn
from .schema import FunctionSchema, build_function_schema


class FunctionRegistry:
    def __init__(self):
        self.schema: Dict[str, FunctionSchema] = {}

    def register(self, function: Callable) -> NoReturn:
        self.schema[function] = build_function_schema(function)

    def get_function(self, fully_qualified_name: str) -> Optional[Callable]:
        for function, schema in self.schema.items():
            if schema["fully_qualified_name"] == fully_qualified_name:
                return function

        return None

    def as_dict(self) -> Dict:
        return {
            schema.fully_qualified_name: schema.as_dict()
            for schema in self.schema.values()
        }
