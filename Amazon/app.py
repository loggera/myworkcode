from flask import Flask, render_template, request, jsonify
import help.amazon_data as had
import loguru
import help.json_data as hjd
import amazon_api.create_sp_campaigns as api_create_campaigns
import amazon_api.create_sp_ad_group as api_create_ad_group
import amazon_api.create_sp_keyword as api_create_keyword
import amazon_api.create_sp_product_ads as api_create_product_ads
import amazon_api.get_targeting_list as api_get_targeting_list
import amazon_api.update_targeting as api_update_targeting
import amazon_api.create_sp_targeting as api_create_targeting

lg = loguru.logger

app = Flask(__name__)


@app.route('/kr/sp/campaigns', methods=['GET', 'POST'])
def sp_campaigns():
    api_rep = {'status': 'unknown', 'message': '未知错误'}
    status_json, json_body = hjd.is_json_data(str(request.data, encoding="utf-8"), api_rep)
    if not status_json:
        return json_body
    shop = json_body.get('shop')
    data_list = had.get_campaings_data(shop)
    return jsonify(data_list)


@app.route('/bulk/auto/campaign/set', methods=['GET', 'POST'])
def bulk_auto_campaign_set():
    api_rep = {'status': 'unknown', 'message': '未知错误'}
    status_json, json_body = hjd.is_json_data(str(request.data, encoding="utf-8"), api_rep)
    if not status_json:
        return json_body
    # add_value = json_body.get('addValue')
    # count = json_body.get('count')
    #
    bid = json_body.get('defBid')
    lg.info(f'Bid:{bid}')

    asin = json_body.get('asin')
    lg.info(f'{asin}')
    # 根据asin 获取sku
    sku = had.get_asin_info_by_asin(asin)
    if not sku:
        api_rep['status'] = 'failed'
        api_rep['message'] = '未找到对应的sku，请联系工作人员！！！'
        return api_rep
    lg.info(f'{sku}')

    shop_name = json_body.get('shop')
    # portfolio = json_body.get('Portfolio')
    # lg.info(f'ShopName:{shop_name},Portfolio:{portfolio}')
    #
    # # 获取 portfolio_id
    # portfolio_id = had.get_portfolio_id_by_portfolio(portfolio)
    # if not portfolio_id:
    #     api_rep['status'] = 'failed'
    #     api_rep['message'] = '未找到对应的portfolio，请联系工作人员！！！'
    #     return api_rep
    portfolio_id = json_body.get('portfolioId')
    lg.info(f'PortfolioId:{portfolio_id}')

    end_date = json_body.get('endDate')
    lg.info(f'EndTime:{end_date}')
    start_date = json_body.get('startDate')
    lg.info(f'StartDate:{start_date}')

    campaign_name = json_body.get('campaignName')
    lg.info(f'CampaignName:{campaign_name}')

    targeting_type = json_body.get('targetingType')
    if not targeting_type:
        targeting_type = 'AUTO'
    lg.info(f'targetingType:{targeting_type}')

    state = json_body.get('initialState')
    lg.info(f'State:{state}')

    percent_list = []
    top_percent_age = json_body.get('biddingAdjustmentsTopPercentage')
    if top_percent_age:
        percent_list.append((top_percent_age, 'PLACEMENT_TOP'))
    page_percent_age = json_body.get('biddingAdjustmentsPagePercentage')
    if page_percent_age:
        percent_list.append((page_percent_age, 'PLACEMENT_PRODUCT_PAGE'))
    # for i in range(4):
    #     percentage = json_body.get(f'percentage{i}')
    #     placement = json_body.get(f'placement{i}')
    #     if percentage and placement:
    #         percent_list.append((percentage, placement))
    lg.info(f'PercentList:{percent_list}')

    #
    strategy = json_body.get('biddingStrategyKey')
    lg.info(f'strategy:{strategy}')

    #
    budget_type = json_body.get('budgetType')
    if not budget_type:
        budget_type = 'DAILY'
    lg.info(f'budgetType:{budget_type}')

    #
    budget = json_body.get('dailyBudget')
    lg.info(f'budget:{budget}')

    #
    ad_group_name = json_body.get('adGroupName')

    usr_type = json_body.get('useType')

    # # 创建campaign
    campaign_result = api_create_campaigns.campaigns_create(None, portfolio_id, end_date, campaign_name, targeting_type,
                                                            state, percent_list, strategy, start_date, budget_type,
                                                            budget,
                                                            shop_name)
    lg.info(f'创建Campaign:{campaign_result}')
    status = campaign_result.get('status')
    if status != 'success':
        return campaign_result

    # 获取到campaignId
    campaign_id = campaign_result.get('campaignId')
    lg.info(f'{campaign_id}')

    # 创建ad_groups
    ad_group_result = api_create_ad_group.ad_group_create(None, shop_name, campaign_id, ad_group_name, state, bid)
    lg.info(f'{ad_group_result}')
    status = ad_group_result.get('status')
    if status != 'success':
        return ad_group_result
    # 获取到ad_group_id
    ad_group_id = ad_group_result.get('adGroupId')
    lg.info(f'{ad_group_id}')

    # 创建产品广告
    product_ads = api_create_product_ads.product_ads_create(None, shop_name, campaign_id, asin, state, sku,
                                                            ad_group_id)
    lg.info(f'{product_ads}')
    status = product_ads.get('status')
    if status != 'success':
        return product_ads

    ad_id = product_ads.get('adId')
    lg.info(f'{ad_id}')

    # 创建targeting
    targeting_result = api_create_targeting.targeting_create(None, shop_name, campaign_id, ad_group_id)
    lg.info(f'{targeting_result}')
    status = targeting_result.get('status')
    if status != 'success':
        return targeting_result

    target_id = targeting_result.get('TargetId')
    lg.info(f'TargetId:{target_id}')
    # if usr_type and usr_type == 'true':
    #     # 获取targeting 列表
    #     target_result = api_get_targeting_list.targeting_list_get(None, shop_name, campaign_id)
    #     status = target_result.get('status')
    #     if status != 'success':
    #         return target_result
    #     target_list = target_result.get('targetingClauses')
    #     query_high_rel_matches = json_body.get('queryHighRelMatches')
    #     info_type_dic = {}
    #     if query_high_rel_matches:
    #         info_type_dic['QUERY_HIGH_REL_MATCHES'] = query_high_rel_matches
    #     query_broad_rel_matches = json_body.get('queryBroadRelMatches')
    #     if query_broad_rel_matches:
    #         info_type_dic['QUERY_BROAD_REL_MATCHES'] = query_broad_rel_matches
    #
    #     asin_accessory_related = json_body.get('asinAccessoryRelated')
    #     if asin_accessory_related:
    #         info_type_dic['ASIN_ACCESSORY_RELATED'] = asin_accessory_related
    #
    #     asin_substitute_related = json_body.get('asinSubstituteRelated')
    #     if asin_substitute_related:
    #         info_type_dic['ASIN_SUBSTITUTE_RELATED'] = asin_substitute_related
    #     for target in target_list:
    #         expression = target.get('expression')
    #         ex_type = expression[0].get('type')
    #         value = info_type_dic[ex_type]
    #         expression_type = target.get('expressionType')
    #         target_id = target.get('targetId')
    #         bid = value
    #         api_update_targeting.targeting_update(None, shop_name, ex_type, value, target_id, expression_type, state,
    #                                               bid)

    api_rep['status'] = 'success'
    api_rep['message'] = '创建成功'
    return api_rep

    # # 创建keyword
    # keyword_result = api_create_keyword.keyword_create(None, shop_name, key_word, language_locale, campaign_id,
    #                                                    match_type, state, bid, ad_group_id,
    #                                                    keyword_text)
    # status = keyword_result.get('status')
    # if status != 'success':
    #     return keyword_result
    # keyword_id = keyword_result.get('keywordId')
    # lg.info(f'{keyword_id}')
    # api_rep['status'] = 'success'
    # api_rep['message'] = '创建成功'
    # return api_rep


@app.route('/bulk/operate/campaign/set', methods=['GET', 'POST'])
def bulk_operate_campaign_set():
    api_rep = {'status': 'unknown', 'message': '未知错误'}
    status_json, json_body = hjd.is_json_data(str(request.data, encoding="utf-8"), api_rep)
    if not status_json:
        return json_body
    # add_value = json_body.get('addValue')
    # count = json_body.get('count')
    #
    bid = json_body.get('defBid')
    lg.info(f'Bid:{bid}')

    asin = json_body.get('asin')
    lg.info(f'{asin}')
    # 根据asin 获取sku
    sku = had.get_asin_info_by_asin(asin)
    if not sku:
        api_rep['status'] = 'failed'
        api_rep['message'] = '未找到对应的sku，请联系工作人员！！！'
        return api_rep
    lg.info(f'{sku}')

    shop_name = json_body.get('shop')
    # portfolio = json_body.get('Portfolio')
    # lg.info(f'ShopName:{shop_name},Portfolio:{portfolio}')
    #
    # # 获取 portfolio_id
    # portfolio_id = had.get_portfolio_id_by_portfolio(portfolio)
    # if not portfolio_id:
    #     api_rep['status'] = 'failed'
    #     api_rep['message'] = '未找到对应的portfolio，请联系工作人员！！！'
    #     return api_rep
    portfolio_id = json_body.get('portfolioId')
    lg.info(f'PortfolioId:{portfolio_id}')

    end_date = json_body.get('endDate')
    lg.info(f'EndTime:{end_date}')
    start_date = json_body.get('startDate')
    lg.info(f'StartDate:{start_date}')

    campaign_name = json_body.get('campaignName')
    lg.info(f'CampaignName:{campaign_name}')

    targeting_type = json_body.get('targetingType')
    if not targeting_type:
        targeting_type = 'MANUAL'
    lg.info(f'targetingType:{targeting_type}')

    state = json_body.get('initialState')
    lg.info(f'State:{state}')

    percent_list = []
    top_percent_age = json_body.get('biddingAdjustmentsTopPercentage')
    if top_percent_age:
        percent_list.append((top_percent_age, 'PLACEMENT_TOP'))
    page_percent_age = json_body.get('biddingAdjustmentsPagePercentage')
    if page_percent_age:
        percent_list.append((page_percent_age, 'PLACEMENT_PRODUCT_PAGE'))
    lg.info(f'PercentList:{percent_list}')

    #
    strategy = json_body.get('biddingStrategyKey')
    lg.info(f'strategy:{strategy}')

    #
    budget_type = json_body.get('budgetType')
    if not budget_type:
        budget_type = 'DAILY'
    lg.info(f'budgetType:{budget_type}')

    #
    budget = json_body.get('dailyBudget')
    lg.info(f'budget:{budget}')

    #
    ad_group_name = json_body.get('adGroupName')

    # usr_type = json_body.get('useType')

    # # 创建campaign
    campaign_result = api_create_campaigns.campaigns_create(None, portfolio_id, end_date, campaign_name, targeting_type,
                                                            state, percent_list, strategy, start_date, budget_type,
                                                            budget,
                                                            shop_name)
    lg.info(f'创建Campaign:{campaign_result}')
    status = campaign_result.get('status')
    if status != 'success':
        return campaign_result

    # 获取到campaignId
    campaign_id = campaign_result.get('campaignId')
    lg.info(f'campaignId:{campaign_id}')

    # 创建ad_groups
    ad_group_result = api_create_ad_group.ad_group_create(None, shop_name, campaign_id, ad_group_name, state, bid)
    lg.info(f'{ad_group_result}')
    status = ad_group_result.get('status')
    if status != 'success':
        return ad_group_result
    # 获取到ad_group_id
    ad_group_id = ad_group_result.get('adGroupId')
    lg.info(f'获取到ad_group_id:{ad_group_id}')

    key_word = json_body.get('keyword')
    match_type = json_body.get('matchType')
    if not match_type:
        match_type = 'EXACT'
    nativeLanguageLocale = json_body.get('nativeLanguageLocale')
    if not nativeLanguageLocale:
        nativeLanguageLocale = 'zh_CN'
    keywordText = json_body.get('keywordText')
    # 创建keyword
    keyword_result = api_create_keyword.keyword_create(None, shop_name, key_word, campaign_id,
                                                       match_type, state, bid, ad_group_id, nativeLanguageLocale,
                                                       keywordText)
    status = keyword_result.get('status')
    if status != 'success':
        return keyword_result
    keyword_id = keyword_result.get('keywordId')
    lg.info(f'{keyword_id}')
    # 创建产品广告
    product_ads = api_create_product_ads.product_ads_create(None, shop_name, campaign_id, asin, state, sku,
                                                            ad_group_id)
    lg.info(f'{product_ads}')
    status = product_ads.get('status')
    if status != 'success':
        return product_ads

    ad_id = product_ads.get('adId')
    lg.info(f'{ad_id}')

    api_rep['status'] = 'success'
    api_rep['message'] = '创建成功'
    return api_rep


@app.route('/campaign/set', methods=['GET', 'POST'])
def campaign_set():
    api_rep = {'status': 'unknown', 'message': '未知错误'}
    status_json, json_body = hjd.is_json_data(str(request.data, encoding="utf-8"), api_rep)
    if not status_json:
        return json_body

    shop_name = json_body.get('shopname')
    portfolio = json_body.get('Portfolio')
    lg.info(f'ShopName:{shop_name},Portfolio:{portfolio}')

    # 获取 portfolio_id
    portfolio_id = had.get_portfolio_id_by_portfolio(portfolio)
    if not portfolio_id:
        api_rep['status'] = 'failed'
        api_rep['message'] = '未找到对应的portfolio，请联系工作人员！！！'
        return api_rep
    lg.info(f'PortfolioId:{portfolio_id}')

    end_date = json_body.get('endDate')
    lg.info(f'EndTime:{end_date}')
    start_date = json_body.get('startDate')
    lg.info(f'StartDate:{start_date}')

    campaign_name = json_body.get('name')
    lg.info(f'CampaignName:{campaign_name}')
    targeting_type = json_body.get('targetingType')
    lg.info(f'targetingType:{targeting_type}')
    state = json_body.get('State')
    lg.info(f'State:{state}')

    percent_list = []
    for i in range(4):
        percentage = json_body.get(f'percentage{i}')
        placement = json_body.get(f'placement{i}')
        if percentage and placement:
            percent_list.append((percentage, placement))
    lg.info(f'PercentList:{percent_list}')

    strategy = json_body.get('Strategy')
    lg.info(f'strategy:{strategy}')
    budget_type = json_body.get('budgetType')
    lg.info(f'budgetType:{budget_type}')

    budget = json_body.get('budget')
    lg.info(f'budget:{budget}')

    # # 创建campaign
    campaign_result = api_create_campaigns.campaigns_create(None, portfolio_id, end_date, campaign_name, targeting_type,
                                                            state, percent_list, strategy, start_date, budget_type,
                                                            budget,
                                                            shop_name)
    lg.info(f'创建Campaign:{campaign_result}')
    status = campaign_result.get('status')
    if status != 'success':
        return campaign_result

    # 获取到campaignId
    campaign_id = campaign_result.get('campaignId')
    lg.info(f'{campaign_id}')
    api_rep['status'] = 'success'
    api_rep['message'] = '操作成功'
    api_rep['CampaignId'] = campaign_id
    return api_rep


@app.route('/ad/groups/set', methods=['GET', 'POST'])
def ad_groups_set():
    api_rep = {'status': 'unknown', 'message': '未知错误'}
    status_json, json_body = hjd.is_json_data(str(request.data, encoding="utf-8"), api_rep)
    if not status_json:
        return json_body

    shop_name = json_body.get('shopname')
    campaign_name = json_body.get('name')
    lg.info(f'CampaignName:{campaign_name}')
    targeting_type = json_body.get('targetingType')
    lg.info(f'targetingType:{targeting_type}')
    state = json_body.get('State')
    lg.info(f'State:{state}')
    campaign_id = json_body.get('CampaignId')
    bid = json_body.get('Bid')

    # 创建ad_groups
    ad_group_result = api_create_ad_group.ad_group_create(None, shop_name, campaign_id, campaign_name, state, bid)
    lg.info(f'{ad_group_result}')
    status = ad_group_result.get('status')
    if status != 'success':
        return ad_group_result
    # 获取到ad_group_id
    ad_group_id = ad_group_result.get('adGroupId')
    lg.info(f'{ad_group_id}')

    api_rep['status'] = 'success'
    api_rep['message'] = '操作成功'
    api_rep['AdGroupId'] = ad_group_id
    return api_rep


@app.route('/product/ads/set', methods=['GET', "POST"])
def product_adt_set():
    api_rep = {'status': 'unknown', 'message': '未知错误'}
    status_json, json_body = hjd.is_json_data(str(request.data, encoding="utf-8"), api_rep)
    if not status_json:
        return json_body

    asin = json_body.get('ASIN')
    lg.info(f'{asin}')
    # 根据asin 获取sku
    sku = had.get_asin_info_by_asin(asin)
    if not sku:
        api_rep['status'] = 'failed'
        api_rep['message'] = '未找到对应的sku，请联系工作人员！！！'
        return api_rep
    lg.info(f'{sku}')

    shop_name = json_body.get('shopname')
    state = json_body.get('State')
    lg.info(f'State:{state}')
    campaign_id = json_body.get('CampaignId')
    ad_group_id = json_body.get('AdGroupId')
    # 创建产品广告
    product_ads = api_create_product_ads.product_ads_create(None, shop_name, campaign_id, asin, state, sku,
                                                            ad_group_id)
    lg.info(f'{product_ads}')
    status = product_ads.get('status')
    if status != 'success':
        return product_ads

    ad_id = product_ads.get('adId')
    lg.info(f'{ad_id}')

    api_rep['status'] = 'success'
    api_rep['message'] = '操作成功'
    api_rep['AdId'] = ad_id
    return api_rep


@app.route('/keyword/set', methods=['GET', "POST"])
def keyword_set():
    api_rep = {'status': 'unknown', 'message': '未知错误'}
    status_json, json_body = hjd.is_json_data(str(request.data, encoding="utf-8"), api_rep)
    if not status_json:
        return json_body

    asin = json_body.get('ASIN')
    lg.info(f'{asin}')
    # 根据asin 获取sku
    sku = had.get_asin_info_by_asin(asin)
    if not sku:
        api_rep['status'] = 'failed'
        api_rep['message'] = '未找到对应的sku，请联系工作人员！！！'
        return api_rep
    lg.info(f'{sku}')

    shop_name = json_body.get('shopname')
    lg.info(f'ShopName:{shop_name}')
    key_word = json_body.get('KeyWord')
    lg.info(f'KeyWord:{key_word}')
    language_locale = json_body.get('LanguageLocale')
    lg.info(f'LanguageLocale:{language_locale}')
    match_type = json_body.get('MatchType')
    lg.info(f'MatchType:{match_type}')
    bid = json_body.get('Bid')
    lg.info(f'"BID":{bid}')

    state = json_body.get('State')
    lg.info(f'State:{state}')
    campaign_id = json_body.get('CampaignId')
    ad_group_id = json_body.get('AdGroupId')
    nativeLanguageLocale = json_body.get('nativeLanguageLocale')
    if not nativeLanguageLocale:
        nativeLanguageLocale = 'zh_CN'
    keywordText = json_body.get('keywordText')
    # 创建keyword
    keyword_result = api_create_keyword.keyword_create(None, shop_name, key_word, campaign_id,
                                                       match_type, state, bid, ad_group_id, nativeLanguageLocale,
                                                       keywordText)
    status = keyword_result.get('status')
    if status != 'success':
        return keyword_result
    keyword_id = keyword_result.get('keywordId')
    lg.info(f'{keyword_id}')

    api_rep['status'] = 'success'
    api_rep['message'] = '操作成功'
    api_rep['KeywordId'] = keyword_id
    return api_rep


if __name__ == '__main__':
    app.run(app.run(debug=True, port=8000))
