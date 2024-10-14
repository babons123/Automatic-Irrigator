import aiocoap.resource as resource
import aiocoap
import aiocoap.numbers as numbers
import time
from model.humidity_sensor import HumiditySensorDescriptor
from kpn_senml import *


class HumiditySensorResource(resource.Resource):

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.humidity_sensor = HumiditySensorDescriptor()
        self.if_ = "core.s"
        self.ct = numbers.media_types_rev['application/senml+json']
        self.rt = "it.unimore.device.sensor.humidity"
        self.title = "Humidity Sensor"

    def build_senml_json_payload(self):
        pack = SenmlPack(self.device_name)
        temp = SenmlRecord("humidity-sensor",
                           unit=SenmlUnits.SENML_UNIT_RELATIVE_HUMIDITY,
                           value=self.humidity_sensor.humidity_value,
                           time=int(time.time()))
        pack.add(temp)
        return pack.to_json()

    async def render_get(self, request):
        print("HumiditySensorResource -> GET Request Received ...")
        print("HumiditySensorResource -> Reading updated humidity value ...")
        self.humidity_sensor.measure_humidity()
        print("HumiditySensorResource -> Updated humidity Value: %f" % self.humidity_sensor.humidity_value)

        payload_string = self.build_senml_json_payload()

        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'],
                               payload=payload_string.encode('utf8'))
