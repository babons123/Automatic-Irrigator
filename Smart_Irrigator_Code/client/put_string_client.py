import logging
import asyncio
import aiocoap
from aiocoap import *
from request.irrigation_request import IrrigationRequestDescriptor

logging.basicConfig(level=logging.INFO)


async def main():

    protocol = await Context.create_client_context()

    request = Message(code=aiocoap.PUT, uri='coap://127.0.0.1:5683/irrigation')
    irrigation_request = IrrigationRequestDescriptor(IrrigationRequestDescriptor.IRRIGATION_TYPE_LOW)
    #irrigation_request = IrrigationRequestDescriptor(IrrigationRequestDescriptor.IRRIGATION_TYPE_MEDIUM)
    #irrigation_request = IrrigationRequestDescriptor(IrrigationRequestDescriptor.IRRIGATION_TYPE_HIGH)
    payload_json_string = irrigation_request.to_json()
    request.payload = payload_json_string.encode("utf-8")

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resources:')
        print(e)
    else:
        print(response)
        response_string = response.payload.decode("utf-8")
        print('Result: %s\nPayload: %r\nPayload String: %s' % (response.code, response.payload, response_string))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
