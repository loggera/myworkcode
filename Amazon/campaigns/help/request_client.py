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
    try:
        lg.info(f'{headers}')
        r = httpx.post(url, json=post_data, headers=headers)
        # lg.info(f'{r.status_code}')
        content = r.text
        # lg.info(f'{content}')
        if r.status_code == 200:
            json_body = hjd.is_json(content)
            return json_body
        else:
            return False
    except:
        return False
