import aiocoap.resource as resource
import aiocoap
import aiocoap.numbers as numbers
import time
import json
from aiocoap.numbers.codes import Code
from model.irrigation_history import IrrigationHistoryDescriptor
from request.irrigation_request import IrrigationRequestDescriptor
from kpn_senml import *


class IrrigationActuatorResource(resource.ObservableResource):

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.irrigation_history = IrrigationHistoryDescriptor()
        self.if_ = "core.a"
        self.ct = numbers.media_types_rev['application/senml+json']
        self.rt = "it.unimore.device.actuator.irrigation"
        self.title = "Irrigation Actuator"

    def build_senml_json_payload(self):
        pack = SenmlPack(self.device_name)
        pack.base_time = int(time.time())
        pack.base_unit = SenmlUnits.SENML_UNIT_COUNTER

        low = SenmlRecord("low_irrigation", value=self.irrigation_history.lowCount)
        medium = SenmlRecord("medium_irrigation", value=self.irrigation_history.mediumCount)
        high = SenmlRecord("high_irrigation", value=self.irrigation_history.highCount)
        total = SenmlRecord("total_irrigation", value=self.irrigation_history.totalCount)

        pack.add(low)
        pack.add(medium)
        pack.add(high)
        pack.add(total)

        return pack.to_json()

    async def render_get(self, request):
        print("IrrigationActuatorResource -> GET Request Received ...")
        payload_string = self.build_senml_json_payload()
        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'], payload=payload_string.encode('utf8'))

    async def render_post(self, request):
        print("IrrigationActuatorResource -> POST Request Received ...")
        self.irrigation_history.increase_low_watering()
        self.updated_state()
        print("IrrigationActuatorResource -> Starting Basic Irrigation ...")
        return aiocoap.Message(code=Code.CHANGED)

    async def render_put(self, request):
        print('IrrigationActuatorResource -> PUT Byte payload: %s' % request.payload)
        json_payload_string = request.payload.decode('UTF-8')
        print('IrrigationActuatorResource -> PUT String Payload: %s' % json_payload_string)
        irrigation_request = IrrigationRequestDescriptor(**json.loads(json_payload_string))
        print('Irrigation Type Request Received: %s' % irrigation_request.type)
        if irrigation_request.type == IrrigationRequestDescriptor.IRRIGATION_TYPE_LOW:
            self.irrigation_history.increase_low_watering()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        elif irrigation_request.type == IrrigationRequestDescriptor.IRRIGATION_TYPE_MEDIUM:
            self.irrigation_history.increase_medium_watering()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        elif irrigation_request.type == IrrigationRequestDescriptor.IRRIGATION_TYPE_HIGH:
            self.irrigation_history.increase_high_watering()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        else:
            return aiocoap.Message(code=Code.BAD_REQUEST)
