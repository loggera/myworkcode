import API.amazon_api as amazon_api
import service.amazon_token as sv_ama_token
import help.redis_helper as hrh
import loguru

lg = loguru.logger


def ad_group_create(token_status, shop_name, campaign_id, name, state, bid):
    api_rep = {'status': 'failed', 'message': '未知错误'}
    # 先取redis(待优化)
    cache_key = f'Amazon1:access:token:{shop_name}'
    access_token = hrh.next_get_value(cache_key)
    lg.info(f'{cache_key},{access_token}')

    config_pro = sv_ama_token.make_token_post_data(shop_name)
    if not config_pro:
        api_rep['status'] = 'failed'
        api_rep['message'] = '未获取到该店铺的client_id相关信息,请联系亚马逊运营商,请联系工作人员！！'
        return api_rep
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
    ad_group_create_api = ama_api.create_ad_groups(campaign_id, name, state, bid, access_token)
    lg.info(f'{ad_group_create_api}')

    response_code = ad_group_create_api.get('code')
    response_result = ad_group_create_api.get('result')
    if response_code == 207:
        ad_group_id = ad_groups_create_result(response_result)
        lg.info(f'{ad_group_id}')
        if not ad_group_id:
            api_rep['message'] = '创建失败'
            api_rep['status'] = 'failed'
            return api_rep
        else:
            api_rep['message'] = '创建成功'
            api_rep['status'] = 'success'
            api_rep['adGroupId'] = ad_group_id
            return api_rep
    if response_code == 403:
        if not token_status:
            ad_group_create(True, shop_name, campaign_id, name, state, bid)


def ad_groups_create_result(result):
    ad_group_ids = result.get('adGroups')
    lg.info(f'{ad_group_ids}')
    if not ad_group_ids:
        return False
    success = ad_group_ids.get('success')
    if success and len(success) != 0:
        # ad_group = success[0].get('adGroup')
        ad_group_id = success[0].get('adGroupId')
        return ad_group_id
    else:
        return False


