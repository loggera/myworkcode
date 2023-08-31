import API.amazon_api as amazon_api
import service.amazon_token as sv_ama_token
import help.redis_helper as hrh
import loguru

lg = loguru.logger


def targeting_list_get(token_status, shop_name, campaign_id):
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
    target_list_api = ama_api.get_target_list(campaign_id, None, None, None, None, None, access_token)
    code = target_list_api.get('code')
    lg.info(f'targetListApi:{target_list_api}')

    if code == 200:
        target_list_result = target_list_api.get('result')
        targeting_clauses = targeting_list_result(target_list_result)
        if targeting_clauses:
            api_rep['message'] = '获取成功'
            api_rep['targetingClauses'] = targeting_clauses
            api_rep['status'] = 'success'
            return api_rep
        else:
            api_rep['status'] = 'failed'
            api_rep['message'] = '获取失败'
            return api_rep
    elif code == 403:
        if not token_status:
            targeting_list_get(True, shop_name, campaign_id)


#
def targeting_list_result(result):
    targeting_clauses = result.get('targetingClauses')
    if targeting_clauses:
        return targeting_clauses
    else:
        return False
if __name__ == '__main__':
    print(targeting_list_get(None, 'TooCust', '476675318154924'))

#         target_id = targeting_clauses[0].get('targetId')
#         if target_id:
#             return target_id
#     return False
