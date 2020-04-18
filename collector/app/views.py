"""This module provides views for collector app."""

from aiohttp.web import RouteTableDef, json_response

from core.utils.file import write_json


routes = RouteTableDef()


# TODO: plan to move server application
@routes.post('/register')
async def register_token(request):
    """Retrieve user's data and set webhook."""
    body = await request.json()
    token = body.get('token', '')
    api = request.app['monobank_api']

    response_body, status = await api.get_user_data(token)
    if status == 200:
        # todo: save user full name from monobank api to DB
        await write_json(response_body, response_body['name'])

        base_url = f'{request.scheme}://{request.host}'
        # todo: fill user_id from users' table
        was_set = await api.set_webhook(token, base_url, 1)
        if was_set is True:
            return json_response(status=200, data={'message': 'Token was registered'})

    return json_response(status=400, data={'message': 'Token was not registered'})


@routes.post('/receiver/{user_id}')
async def receive_transaction(request):
    """Receive transaction from webhook and fill transaction data in DB and spreadsheets."""
    user_id = request.match_info['user_id']
    data = await request.json()
    transaction_id = data['data']['statementItem']['id']
    # todo: use this data to fill in DB and spreadsheets
    await write_json(data, transaction_id)
    return json_response(data={'message': 'success', 'user': user_id, 'data': data})
