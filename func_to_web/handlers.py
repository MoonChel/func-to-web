from aiohttp import web


async def handler(request: web.Request):
    json = await request.json()
    fully_qualified_name = json["fully_qualified_name"]

    registry = request.app["function_registry"]
    function = registry.get_function(fully_qualified_name)

    if not function:
        return web.Response("Function not found", status=404)

    result = function(**json["arguments"])

    return web.json_response({"result": result})


async def get_schema_for_web(request):
    registry = request.app["function_registry"]
    return web.json_response(registry.as_dict())
