# func to web

small library, that can create web api from your python function.

Example:

```python
def hello(name: str) -> str:
    """
    hello
    test
    """
    return "Hello " + name
```

will generate this json description:

```python
{
    "module_name.hello": {
        "name": "hello",
        "description": '\n    hello\n    test\n    ',
        "fully_qualified_name": "module_name.hello",
        "annotations": [
            {"name": "name", "type": "string"},
            {"name": "return", "type": "string"},
        ],
    }
}
```

which can be easily dumped into json object

## Supported types

https://github.com/MoonChel/func-to-web/blob/aef19dd9952687f2f4a9f088ceea42c47a2ebe05/func_to_web/resolvers.py#L12
