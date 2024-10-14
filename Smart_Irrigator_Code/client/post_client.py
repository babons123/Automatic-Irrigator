import logging
import asyncio
import aiocoap
from aiocoap import *

logging.basicConfig(level=logging.INFO)


async def main():

    protocol = await Context.create_client_context()

    request = Message(code=aiocoap.POST, uri='coap://127.0.0.1:5683/irrigation')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print(response)
        response_string = response.payload.decode("utf-8")
        print('Result: %s\nPayload: %r\nPayload String: %s' % (response.code, response.payload, response_string))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
