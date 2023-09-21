import json
import logging
import time

import requests


def logger_custom_exception(error, name):
    logger = logging.getLogger(name)
    logger_format = logging.Formatter(
        "%(name)s %(asctime)s %(levelname)s %(message)s")
    logger_handler = logging.FileHandler(f'{name}.log', mode='a')
    logger_handler.setFormatter(logger_format)
    logger.addHandler(logger_handler)
    logger.exception(error)


def get_balance(tm_api):
    url = f'https://market.csgo.com/api/v2/get-money?key={tm_api}'

    try:
        response = requests.get(url).json()
        response.pop('success')
    except Exception as error:
        logger_custom_exception(error, __name__)
        time.sleep(30)
        return get_balance(tm_api)
    return response


def get_items_on_sale(tm_api):
    url = (f'https://market.csgo.com/api/v2/items?'
           f'key={tm_api}')
    response = requests.get(url)
    response = response.json()
    if not response['success']:
        return False
    if not response['items']:
        return True, 0, 0
    items_on_sale = 0
    items_sold = 0
    for item in response['items']:
        if item['status'] == '1':
            items_on_sale += 1
        elif item['status'] == '2':
            items_sold += 1
    return True, items_on_sale, items_sold


def get_settings():
    with open('settings.json', 'r') as file:
        data = json.load(file)
        tm_api = data['tm_api']
        interval = data['request_interval']
        tg_api = data['tg_api']
        return {
            'tg_api': tg_api,
            'tm_api': tm_api,
            'interval': interval
        }
