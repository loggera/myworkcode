import loguru
import campaigns.help.request_client as hrc
import help.redis_helper as hrh
import help.amazon_data as had

lg = loguru.logger


def make_token_post_data(ad_name):
    return had.get_client_id_by_ad_name(ad_name)


# status 记录是否超时
def get_amazon_token(status):
    cache_key = 'Amazon1:access:token'
    if not status:
        # 暂用待修改
        cache_value = hrh.next_get_value(cache_key)
        if cache_value:
            return cache_value
    url = 'https://api.amazon.com/auth/o2/token'
    lg.info(f'{url}')
    post_data = {
        "grant_type": "refresh_token",
        "client_id": "amzn1.application-oa2-client.652f99ef3ff840a5bef05e5eb3a2e308",
        "refresh_token": "Atzr|IwEBIARrce9b1Bm-C-fK75_rxDCkYZzEXQ6O3_NscQh4z5bu594gK0gaXy53TPGIZ44qqlj6ksW0joKe0HIfEl1qG_eBlb1cyl0K2XdZgaUSE8aM8KxWyarFNibyqe6aHl7JBHgXwVplQQhBJfPhoMk9uBS3aFIIN3KL2TXdFIBQy_aN2WMvnGt4kMhWxxwrh1tsjxrmdPA73oZ_yXCapR3br3b5osZcUerdB5cX2OdCPzRPYawT9rdQz-i_EvpmbtDv9XFgj3r47YJeluGVVhAZe8qKEx3uL3JiqVwGHzUO1njLv0DA3cIX25BuzDiRgTKaihd3HnVqKAhHnWsz4a7ESuuHqlIeSUo5FL0-cbrVnKuZNCEvNYOtTA26oQ_F1Wbt1fqr1eVaEyRPGLwtn-9N0DUzByj9CPoAfxf4PwByrW5T8h-xnxqgHn5SrvVM9kNlFltHzUJpk35BHflS07Q8iV0m6TyM0XYUpXpg8UKLmA2NDw",
        "client_secret": "93bacf67676f0f19d23097d03ad838a90d6177739efab3bcff8a8ebdbdff87cb"
    }
    result = hrc.post_amazon_api(url, post_data, {})
    expires_in = result.get('expires_in')
    if expires_in == 3600:
        access_token = result.get('access_token')
        hrh.next_set_value(cache_key, access_token, 60 * 30)
        return access_token
    else:
        return False


def get_amazon_token_by_ad_name(ad_name, grant_type, client_id, refresh_token, client_secret):
    cache_key = f'Amazon1:access:token:{ad_name}'
    url = 'https://api.amazon.com/auth/o2/token'
    lg.info(f'{url}')
    post_data = {
        "grant_type": grant_type,
        "client_id": client_id,
        "refresh_token": refresh_token,
        "client_secret": client_secret
    }
    result = hrc.post_amazon_api(url, post_data, {})
    expires_in = result.get('expires_in')
    if expires_in == 3600:
        access_token = result.get('access_token')
        hrh.next_set_value(cache_key, access_token, 60 * 30)
        return access_token
    else:
        return False


# if __name__ == '__main__':
#     get_amazon_token()
# r = httpx.post(url, data=post_data)
# if r.status_code == 200:
#     content = r.json()
#     lg.info(f'{content}')
#     access_token = content.get('access_token')
#     lg.info(f'{access_token}')
#     return access_token
if __name__ == '__main__':
    count = '5'
    add_value = '0.1'
    bid = '0.75'
    for i in range(int(count)):

        b_id = float(bid) + i * float(add_value)
        print(b_id)
