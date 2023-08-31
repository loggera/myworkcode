import API.amazon_api as amazon_api
import service.amazon_token as sv_ama_token
import help.redis_helper as hrh
import loguru

lg = loguru.logger


def adgroup_sp_delete(token_status, shop_name, adgroup_id):
    api_rep = {'status': 'failed', 'message': '未知错误'}

    cache_key = f'Amazon1:access:token:{shop_name}'
    lg.info(f'{cache_key}')
    access_token = hrh.next_get_value(cache_key)
    lg.info(f'{cache_key},{access_token}')

    config_pro = sv_ama_token.make_token_post_data(shop_name)
    if not config_pro:
        api_rep['status'] = 'failed'
        api_rep['message'] = '未获取到该店铺的client_id相关信息,请联系亚马逊运营商,请联系工作人员！！'
        return api_rep
    lg.info(f'ConfigPro:{config_pro}')
    amazon_advertising_api_scope = config_pro.get('amazon_advertising_api_scope')
    amazon_advertising_api_clientId = config_pro.get('amazon_advertising_api_clientId')

    if token_status:
        access_token = None
    lg.info(f'{access_token}')
    if not access_token:
        grant_type = config_pro.get('grant_type')
        client_id = config_pro.get('client_id')
        refresh_token = config_pro.get('refresh_token')
        client_secret = config_pro.get('client_secret')
        access_token = sv_ama_token.get_amazon_token_by_ad_name(shop_name, grant_type, client_id,
                                                                refresh_token,
                                                                client_secret)
        if not access_token:
            api_rep['status'] = 'failed'
            api_rep['message'] = '为获取到access_token,请联系工作人员！！'
            return api_rep

    ama_api = amazon_api.AmazonAPI(scope=amazon_advertising_api_scope, client_id=amazon_advertising_api_clientId)
    adgroup_delete_api = ama_api.delete_sp_adgroup(adgroup_id, access_token)
    code = adgroup_delete_api.get('code')
    lg.info(f'adGroupDeleteApi:{adgroup_delete_api}')

    if code == 207:
        campaigns_del_result = adgroup_delete_api.get('result')
        delete_result = adgroup_delete_result(campaigns_del_result)
        if delete_result:
            api_rep['message'] = '删除成功'
            api_rep['status'] = 'success'
            return api_rep
        else:
            api_rep['status'] = 'failed'
            api_rep['message'] = '删除失败'
            return api_rep
    elif code == 403:
        if not token_status:
            adgroup_sp_delete(True, shop_name, adgroup_id)


def adgroup_delete_result(result):
    adgroup = result.get('adGroup')
    if adgroup:
        success = adgroup.get('success')
        if success:
            return True
    return False


if __name__ == '__main__':
    adgroup_sp_delete(None,'TooCust','388615969431363')