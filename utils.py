import datetime
import json
import aiohttp


def in_bot_channel(channel=None, message=None):
    if message:
        channel = message.channel
    return channel.name == 'bot'


def get_decoded_json(json_body):
    decoder = json.decoder.JSONDecoder()
    decoded_json = decoder.decode(json_body)
    return decoded_json


def get_time_in_country(user, time):
    return time + ' - ' + user


async def get_country_time_from_response(response):
    json_body = await response.text()
    decoded_json = get_decoded_json(json_body)
    country_datetime = decoded_json['datetime']
    country_time = get_time_from_datetime(_datetime=country_datetime, _format='%Y-%m-%dT%H:%M:%S.%f%z')
    return country_time


def get_time_from_datetime(_datetime, _format):
    country_time = datetime.datetime.strptime(_datetime, _format).time().strftime('%H:%M')
    return country_time


async def send_timezones_to_channel(message):
    timezones = {
        "san_jose": '/America/Los_Angeles',
        'moscow': '/Europe/Moscow',
        'ukraine': '/Europe/Riga',
        'australia': '/Australia/Lindeman'
    }
    base_url = "http://worldtimeapi.org/api/timezone"

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + timezones['ukraine']) as response:
            country_time = await get_country_time_from_response(response)
            full_country_time = get_time_in_country('🐇!Турбо_Кролик!🐇', country_time)

            await message.channel.send(full_country_time)

        async with session.get(base_url + timezones['moscow']) as response:
            country_time = await get_country_time_from_response(response)
            full_country_time = get_time_in_country('sanyauni', country_time)

            await message.channel.send(full_country_time)

        async with session.get(base_url + timezones['australia']) as response:
            country_time = await get_country_time_from_response(response)
            full_country_time = get_time_in_country('sliks_', country_time)

            await message.channel.send(full_country_time)

        async with session.get(base_url + timezones['san_jose']) as response:
            country_time = await get_country_time_from_response(response)
            full_country_time = get_time_in_country('LeraST', country_time)

            await message.channel.send(full_country_time)
