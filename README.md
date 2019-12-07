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
