import logging
import asyncio
import link_header
from aiocoap import *
import json

logging.basicConfig(level=logging.INFO)

RT_TEMPERATURE_SENSOR = "it.unimore.device.sensor.temperature"
RT_HUMIDITY_SENSOR = "it.unimore.device.sensor.humidity"
RT_RAIN_SENSOR = "it.unimore.device.sensor.rain"
RT_BATTERY_SENSOR = "it.unimore.device.sensor.battery"
RT_IRRIGATION_ACTUATOR = "it.unimore.device.actuator.irrigation"
TARGET_ENDPOINT = 'coap://127.0.0.1:5683'
WELL_KNOWN_CORE_URI = "/.well-known/core"

target_temperature_sensor_uri = None
target_humidity_sensor_uri = None
target_rain_sensor_uri = None
target_battery_sensor_uri = None
target_irrigation_actuator_uri = None


def is_device_valid(core_link_format_response):
    global target_temperature_sensor_uri, target_humidity_sensor_uri, target_rain_sensor_uri, target_battery_sensor_uri, target_irrigation_actuator_uri
    links_headers = link_header.parse(core_link_format_response)
    for link in links_headers.links:
        if link.href != WELL_KNOWN_CORE_URI:
            for pair in link.attr_pairs:
                key = pair[0]
                value = pair[1]
                if key == "rt" and value == RT_TEMPERATURE_SENSOR:
                    target_temperature_sensor_uri = link.href
                elif key == "rt" and value == RT_HUMIDITY_SENSOR:
                    target_humidity_sensor_uri = link.href
                elif key == "rt" and value == RT_RAIN_SENSOR:
                    target_rain_sensor_uri = link.href
                elif key == "rt" and value == RT_BATTERY_SENSOR:
                    target_battery_sensor_uri = link.href
                elif key == "rt" and value == RT_IRRIGATION_ACTUATOR:
                    target_irrigation_actuator_uri = link.href

    print('Temperature Sensor Uri: ' + target_temperature_sensor_uri)
    print('Humidity Sensor Uri: ' + target_humidity_sensor_uri)
    print('Rain Sensor Uri: ' + target_rain_sensor_uri)
    print('Battery Sensor Uri: ' + target_battery_sensor_uri)
    print('Irrigation Actuator Uri: ' + target_irrigation_actuator_uri)

    if target_temperature_sensor_uri is not None \
            and target_humidity_sensor_uri is not None \
            and target_rain_sensor_uri is not None \
            and target_battery_sensor_uri is not None \
            and target_irrigation_actuator_uri is not None:
        return True
    else:
        return False


async def temperature_high(coap_client):
    request = Message(code=Code.GET, uri=TARGET_ENDPOINT + target_temperature_sensor_uri)
    try:
        response = await coap_client.request(request).response
    except Exception as e:
        return False
    else:
        response_string = response.payload.decode("utf-8")
        json_senml = json.loads(response_string)
        if 35 > json_senml[0]['v'] > 30:
            main.temperature = json_senml[0]['v']
            main.irrigation_level = "Low"
            return True
        elif 40 > json_senml[0]['v'] > 35:
            main.temperature = json_senml[0]['v']
            main.irrigation_level = "Medium"
            return True
        elif json_senml[0]['v'] > 40:
            main.temperature = json_senml[0]['v']
            main.irrigation_level = "High"
            return True
        else:
            main.temperature = json_senml[0]['v']
            return False


async def humidity_low(coap_client):
    request = Message(code=Code.GET, uri=TARGET_ENDPOINT + target_humidity_sensor_uri)
    try:
        response = await coap_client.request(request).response
    except Exception as e:
        return False
    else:
        response_string = response.payload.decode("utf-8")
        json_senml = json.loads(response_string)
        if 30 < json_senml[0]['v'] < 40:
            main.humidity = json_senml[0]['v']
            main.irrigation_level = "Low"
            return True
        elif 20 < json_senml[0]['v'] < 30:
            main.humidity = json_senml[0]['v']
            main.irrigation_level = "Medium"
            return True
        elif json_senml[0]['v'] < 20:
            main.humidity = json_senml[0]['v']
            main.irrigation_level = "High"
            return True
        else:
            main.humidity = json_senml[0]['v']
            return False


async def rain_low(coap_client):
    request = Message(code=Code.GET, uri=TARGET_ENDPOINT + target_rain_sensor_uri)
    try:
        response = await coap_client.request(request).response
    except Exception as e:
        return False
    else:
        response_string = response.payload.decode("utf-8")
        json_senml = json.loads(response_string)
        if 20 < json_senml[0]['v'] < 30:
            main.rain = json_senml[0]['v']
            main.irrigation_level = "Low"
            return True
        elif 10 < json_senml[0]['v'] < 20:
            main.rain = json_senml[0]['v']
            main.irrigation_level = "Medium"
            return True
        elif json_senml[0]['v'] < 10:
            main.rain = json_senml[0]['v']
            main.irrigation_level = "High"
            return True
        else:
            main.rain = json_senml[0]['v']
            return False


async def battery_low(coap_client):
    request = Message(code=Code.GET, uri=TARGET_ENDPOINT + target_battery_sensor_uri)
    try:
        response = await coap_client.request(request).response
    except Exception as e:
        return False
    else:
        response_string = response.payload.decode("utf-8")
        json_senml = json.loads(response_string)
        if json_senml[0]['v'] < 30:
            main.battery = json_senml[0]['v']
            return True
        else:
            main.battery = json_senml[0]['v']
            return False


async def trigger_irrigation(coap_client):
    request = Message(code=Code.POST, uri=TARGET_ENDPOINT + target_irrigation_actuator_uri)
    try:
        response = await coap_client.request(request).response
    except Exception as e:
        print('Failed to fetch resources:')
        print(e)
    else:
        if response.code.is_successful():
            return True
        else:
            return False


async def main():

    main.temperature = None
    main.humidity = None
    main.rain = None
    main.battery = None
    main.irrigation_level = None

    coap_client = await Context.create_client_context()

    request = Message(code=Code.GET, uri=TARGET_ENDPOINT + WELL_KNOWN_CORE_URI)

    try:
        response = await coap_client.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        response_string = response.payload.decode("utf-8")
        print(response_string)
        if is_device_valid(response_string):
            print("Valid Target Device Detected !")
            if await battery_low(coap_client):
                print("Batteria Scarica! Ricaricare!")
                print("Valore Batteria = {:.2f} %".format(main.battery))
            elif await temperature_high(coap_client):
                print("Temperatura Elevata !")
                print("Valore Temperatura = {:.2f} °C".format(main.temperature))
                irrigation_result = await trigger_irrigation(coap_client)
                if irrigation_result == True:
                    print("Acqua Somministrata ")
                    print("Quantità Somministrata :  ", main.irrigation_level)
                else:
                    print("Error irrigating ! Please try later ...")
            elif await humidity_low(coap_client):
                print("Umidità Bassa !")
                print("Valore Umidità = {:.2f} % ".format(main.humidity))
                irrigation_result = await trigger_irrigation(coap_client)
                if irrigation_result == True:
                    print("Acqua Somministrata ")
                    print("Quantità Somministrata : ", main.irrigation_level)
                else:
                    print("Error irrigating ! Please try later ...")
            elif await rain_low(coap_client):
                print("Pioggia Scarsa ! ")
                print("Valore Pioggia = {:.2f} m^3".format(main.rain))
                irrigation_result = await trigger_irrigation(coap_client)
                if irrigation_result == True:
                    print("Acqua Somministrata ")
                    print("Quantità Somministrata :  ", main.irrigation_level)
                else:
                    print("Error irrigating ! Please try later ...")
            else:
                print("Valore Batteria = {:.2f} %".format(main.battery))
                print("Valore Temperatura = {:.2f} °C".format(main.temperature))
                print("Valore Umidità = {:.2f} %".format(main.humidity))
                print("Valore Pioggia = {:.2f} m^3".format(main.rain))
                print("Non è Necessario Fornire Acqua ")
        else:
            print("Error: Invalid Device Detected !")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
