import json

import httpx
import loguru
import campaigns.help.json_data as hjd

lg = loguru.logger


def get_amazon_api(url, headers):
    try:
        r = httpx.get(url, headers=headers)
        content = r.text
        lg.info(f'{content}')
        if r.status_code == 200:
            json_body = hjd.is_json(content)
            return json_body
        else:
            return False
    except:
        return False


def get_amazon_next_token_api(url, headers, data):
    try:
        r = httpx.get(url, headers=headers, params=data)
        content = r.text
        lg.info(f'{r.status_code}')
        lg.info(f'{content}')
        if r.status_code == 200:
            json_body = hjd.is_json(content)
            return json_body
        else:
            return False
    except:
        return False


def post_amazon_api(url, post_data, headers):
    api_rep = {}
    lg.info(f'{post_data}')
    lg.info(f'{headers}')
    try:
        # lg.info(f'{headers}')
        r = httpx.post(url, json=post_data, headers=headers)
        lg.info(f'{url},{post_data},{headers}')
        lg.info(f'{r.status_code}')
        content = r.text
        lg.info(f'{content}')
        if 200 <= r.status_code < 400:
            json_body = hjd.is_json(content)
            api_rep['result'] = json_body
            api_rep['message'] = json_body.get('message')
            api_rep['code'] = r.status_code
            return api_rep
    except httpx.ReadTimeout as rto:
        api_rep['message'] = str(rto)
        api_rep['code'] = -1
        return api_rep
    except httpx.ConnectTimeout as cto:
        api_rep['message'] = str(cto)
        api_rep['code'] = -1
        return api_rep


def put_amazon_api(url, post_data, headers):
    api_rep = {}
    lg.info(f'{post_data}')
    lg.info(f'{headers}')
    try:
        # lg.info(f'{headers}')
        r = httpx.put(url, json=post_data, headers=headers)
        lg.info(f'{url},{post_data},{headers}')
        lg.info(f'{r.status_code}')
        content = r.text
        lg.info(f'{content}')
        if 200 <= r.status_code < 400:
            json_body = hjd.is_json(content)
            api_rep['result'] = json_body
            api_rep['message'] = json_body.get('message')
            api_rep['code'] = r.status_code
            return api_rep
    except httpx.ReadTimeout as rto:
        api_rep['message'] = str(rto)
        api_rep['code'] = -1
        return api_rep
    except httpx.ConnectTimeout as cto:
        api_rep['message'] = str(cto)
        api_rep['code'] = -1
        return api_rep
