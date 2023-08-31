import API.amazon_api as amazon_api
import service.amazon_token as sv_ama_token
import help.redis_helper as hrh
import loguru

lg = loguru.logger


def campaigns_create(token_status, portfolio_id, end_date, name, targeting_type, state, percent_list
                     , strategy, start_date, budget_type, budget, shop_name):
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
    campaigns_create_api = ama_api.create_sponsored_products_campaigns(portfolio_id, end_date, name, targeting_type,
                                                                       state, percent_list, strategy, start_date,
                                                                       budget_type,
                                                                       budget,
                                                                       access_token)
    lg.info(f'CampaignsApi:{campaigns_create_api}')
    response_code = campaigns_create_api.get('code')
    response_result = campaigns_create_api.get('result')
    if response_code == 207:
        campaign_id = campaigns_create_result(response_result)
        lg.info(f'{campaign_id}')
        if not campaign_id:
            api_rep['message'] = '创建失败'
            api_rep['status'] = 'failed'
            return api_rep
        else:
            api_rep['message'] = '创建成功'
            api_rep['status'] = 'success'
            api_rep['campaignId'] = campaign_id
            return api_rep
    if response_code == 403:
        if not token_status:
            campaigns_create(True, portfolio_id, end_date, name, targeting_type, state, percent_list, strategy,
                             start_date, budget_type, budget,
                             shop_name)


def campaigns_create_result(result):
    campaigns = result.get('campaigns')
    lg.info(f'{campaigns}')
    if not campaigns:
        return False
    success = campaigns.get('success')
    lg.info(f'{success}')
    if success and len(success) != 0:
        campaign_id = success[0].get('campaignId')
        return campaign_id
    else:
        return False
