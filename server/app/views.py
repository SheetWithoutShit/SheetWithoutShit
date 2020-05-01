"""This module provides views for server app."""

from aiohttp.web import RouteTableDef, json_response


routes = RouteTableDef()


@routes.get('/test')
async def test(request):
    """Test endpoint."""
    print(request)
    return json_response(data={"message": "success"})
