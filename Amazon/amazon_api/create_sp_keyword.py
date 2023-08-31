import API.amazon_api as amazon_api
import service.amazon_token as sv_ama_token
import help.redis_helper as hrh
import loguru

lg = loguru.logger


# def keyword_create():
#     pass


def keyword_create(token_status, shop_name, key_word, campaign_id, match_type, state, bid, ad_group_id,
                   nativeLanguageLocale, keywordText):
    api_rep = {'status': 'failed', 'message': '未知错误'}

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
        access_token = sv_ama_token.get_amazon_token_by_ad_name(shop_name, grant_type, client_id, refresh_token,
                                                                client_secret)
        if not access_token:
            api_rep['status'] = 'failed'
            api_rep['message'] = '为获取到access_token,请联系工作人员！！'
            return api_rep

    ama_api = amazon_api.AmazonAPI(scope=amazon_advertising_api_scope, client_id=amazon_advertising_api_clientId)
    keyword_api = ama_api.create_sp_keyword(key_word, campaign_id, match_type, state, bid,
                                            ad_group_id, nativeLanguageLocale, keywordText,access_token)
    response_code = keyword_api.get('code')
    response_result = keyword_api.get('result')
    if response_code == 207:
        keyword_id = keyword_result(response_result)
        if not keyword_id:
            api_rep['message'] = '创建失败'
            api_rep['status'] = 'failed'
            return api_rep
        else:
            api_rep['message'] = '创建成功'
            api_rep['status'] = 'success'
            api_rep['keywordId'] = keyword_id
            return api_rep
    if response_code == 403:
        if not token_status:
            keyword_create(True, shop_name, key_word, campaign_id, match_type, state, bid,
                           ad_group_id,nativeLanguageLocale, keywordText)


def keyword_result(result):
    ad_group_ids = result.get('keywords')
    if not ad_group_ids:
        return False
    success = ad_group_ids.get('success')
    if success and len(success) != 0:
        keyword_id = success[0].get('keywordId')
        return keyword_id
    else:
        return False


if __name__ == '__main__':
    keyword_create(None, 'TooCust', 'test', '541742939232080', 'EXACT', 'PAUSED', '0.75', '557494513833088')
