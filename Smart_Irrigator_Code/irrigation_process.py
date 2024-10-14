import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
from resource.temperature_sensor_resource import TemperatureSensorResource
from resource.humidity_sensor_resource import HumiditySensorResource
from resource.rain_sensor_resource import RainSensorResource
from resource.battery_sensor_resource import BatterySensorResource
from resource.irrigation_actuator_resource import IrrigationActuatorResource

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.INFO)


def main():

    device_name = "irrigator-A1"

    root = resource.Site()

    root.add_resource(['.well-known', 'core'], resource.WKCResource(root.get_resources_as_linkheader, impl_info=None))
    root.add_resource(['temperature'], TemperatureSensorResource(device_name))
    root.add_resource(['humidity'], HumiditySensorResource(device_name))
    root.add_resource(['rain'], RainSensorResource(device_name))
    root.add_resource(['battery'], BatterySensorResource(device_name))
    root.add_resource(['irrigation'], IrrigationActuatorResource(device_name))
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683)))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
