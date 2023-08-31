import loguru
import campaigns.help.request_client as hrc
lg = loguru.logger


def get_amazon_token():
    url = 'https://api.amazon.com/auth/o2/token'
    lg.info(f'{url}')
    post_data = {
        "grant_type": "refresh_token",
        "client_id": "amzn1.application-oa2-client.652f99ef3ff840a5bef05e5eb3a2e308",
        "refresh_token": "Atzr|IwEBIARrce9b1Bm-C-fK75_rxDCkYZzEXQ6O3_NscQh4z5bu594gK0gaXy53TPGIZ44qqlj6ksW0joKe0HIfEl1qG_eBlb1cyl0K2XdZgaUSE8aM8KxWyarFNibyqe6aHl7JBHgXwVplQQhBJfPhoMk9uBS3aFIIN3KL2TXdFIBQy_aN2WMvnGt4kMhWxxwrh1tsjxrmdPA73oZ_yXCapR3br3b5osZcUerdB5cX2OdCPzRPYawT9rdQz-i_EvpmbtDv9XFgj3r47YJeluGVVhAZe8qKEx3uL3JiqVwGHzUO1njLv0DA3cIX25BuzDiRgTKaihd3HnVqKAhHnWsz4a7ESuuHqlIeSUo5FL0-cbrVnKuZNCEvNYOtTA26oQ_F1Wbt1fqr1eVaEyRPGLwtn-9N0DUzByj9CPoAfxf4PwByrW5T8h-xnxqgHn5SrvVM9kNlFltHzUJpk35BHflS07Q8iV0m6TyM0XYUpXpg8UKLmA2NDw",
        "client_secret": "93bacf67676f0f19d23097d03ad838a90d6177739efab3bcff8a8ebdbdff87cb"
    }
    result = hrc.post_amazon_api(url, post_data, {})
    lg.info(f'{result}')
    expires_in = result.get('expires_in')
    if expires_in == 3600:
        access_token = result.get('access_token')
        return access_token
    else:
        return False


if __name__ == '__main__':
    get_amazon_token()
    # r = httpx.post(url, data=post_data)
    # if r.status_code == 200:
    #     content = r.json()
    #     lg.info(f'{content}')
    #     access_token = content.get('access_token')
    #     lg.info(f'{access_token}')
    #     return access_token
