import help.request_client as hrc
import loguru

lg = loguru.logger


class AmazonAPI:

    def __init__(self, scope, client_id):
        self.amazon_url = 'https://advertising-api.amazon.com'
        self.scope = scope
        self.client_id = client_id

    def __make_headers(self):
        self.headers = {
            "Amazon-Advertising-API-Scope": self.scope,
            "Amazon-Advertising-API-ClientId": self.client_id
        }

    # amazon 获取campaigns 接口调用
    def sp_campaigns_list(self, access_token, next_token):
        url = f'{self.amazon_url}/sp/campaigns/list'
        post_data = {}
        if next_token:
            post_data = {'nextToken': next_token}
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spcampaign.v3+json'
        self.headers["Accept"] = "application/vnd.spcampaign.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    # amazon 获取ad_group接口调用
    def sp_ad_group_list(self, campaign_id, state, ad_group_id):
        url = f'{self.amazon_url}/sp/adGroups/list'
        # post_data = {
        #     "campaignIdFilter": {
        #         "include": [
        #             "string"
        #         ]
        #     }, }
        post_data = {
            'campaignIdFilter': {'include': [campaign_id]}
        }

        if state:
            post_data['stateFilter'] = {'include': [state]}
        if ad_group_id:
            post_data['adGroupIdFilter'] = {'include': [ad_group_id]}
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spadGroup.v3+json'
        self.headers["Accept"] = "application/vnd.spadGroup.v3+json"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    # amazon 创建campaign 接口调用
    def create_sponsored_products_campaigns(self, portfolio_id, end_date, name, targeting_type, state, percent_list,
                                            strategy, start_date, budget_type, budget,
                                            access_token):
        url = f'{self.amazon_url}/sp/campaigns'
        place_ment_list = []
        for percent in percent_list:
            data_dic = {}
            data_dic["percentage"] = int(percent[0])
            data_dic["placement"] = percent[1]
            place_ment_list.append(data_dic)
        post_data = {
            "campaigns": [
                {
                    "portfolioId": portfolio_id,
                    "name": name,
                    "targetingType": targeting_type,
                    "state": state,
                    "dynamicBidding": {
                        "placementBidding": place_ment_list,
                        "strategy": strategy
                    },
                    "startDate": start_date,
                    "budget": {
                        "budgetType": budget_type,
                        "budget": int(budget)
                    }
                }
            ]
        }
        if end_date:
            post_data['campaigns'][0]['endDate'] = end_date
        lg.info(f'{post_data}')
        # return {}
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spcampaign.v3+json'
        self.headers["Accept"] = "application/vnd.spcampaign.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    def create_ad_groups(self, campaign_id, name, state, bid, access_token):
        url = f'{self.amazon_url}/sp/adGroups'
        post_data = {
            "adGroups": [
                {
                    "campaignId": campaign_id,
                    "name": name,
                    "state": state,
                    "defaultBid": float(bid)
                }
            ]
        }
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spadgroup.v3+json'
        self.headers["Accept"] = "application/vnd.spadgroup.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    def create_sp_product_ads(self, campaign_id, asin, state, sku, adgroup_id, access_token):
        url = f'{self.amazon_url}/sp/productAds'
        post_data = {
            "productAds": [
                {
                    "campaignId": campaign_id,
                    "asin": asin,
                    "state": state,
                    "sku": sku,
                    "adGroupId": adgroup_id
                }
            ]
        }
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spproductAd.v3+json'
        self.headers["Accept"] = "application/vnd.spproductAd.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    def create_sp_keyword(self, key_word, campaign_id, match_type, state, bid, ad_group_id, nativeLanguageLocale,
                          keywordText,
                          access_token):
        url = f'{self.amazon_url}/sp/keywords'
        post_data = {
            "keywords": [
                {
                    "nativeLanguageKeyword": key_word,
                    "campaignId": campaign_id,
                    "matchType": match_type,
                    "state": state,
                    "nativeLanguageLocale": nativeLanguageLocale,
                    "bid": float(bid),
                    "adGroupId": ad_group_id,
                    "keywordText": keywordText
                }
            ]
        }
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spkeyword.v3+json'
        self.headers["Accept"] = "application/vnd.spkeyword.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    def delete_sp_campaign_edit(self, campaign_id, access_token):
        url = f'{self.amazon_url}/sp/campaigns/delete'
        post_data = {
            "campaignIdFilter": {
                "include": [
                    campaign_id
                ]
            }
        }
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spcampaign.v3+json'
        self.headers["Accept"] = "application/vnd.spcampaign.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    def delete_sp_adgroup(self, adgroup_id, access_token):
        url = f'{self.amazon_url}/sp/adGroups/delete'
        post_data = {
            "adGroupIdFilter": {
                "include": [
                    adgroup_id
                ]
            }
        }
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spAdGroup.v3+json'
        self.headers["Accept"] = "application/vnd.spAdGroup.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    def get_target_list(self, campaign_id, state, expression, target_id, asin, adgroup_id, access_token):
        url = f'{self.amazon_url}/sp/targets/list'
        post_data = {}
        if campaign_id:
            post_data['campaignIdFilter'] = {"include": [
                campaign_id
            ]}
        if state:
            post_data['stateFilter'] = {"include": [
                state
            ]}
        if expression:
            post_data['expressionTypeFilter'] = {'include': [expression]}
        if target_id:
            post_data['targetIdFilter'] = {'include': [target_id]}
        if asin:
            post_data['asinFilter'] = {'queryTermMatchType': 'BROAD_MATCH', 'include': [asin]}
        if adgroup_id:
            post_data['adGroupIdFilter'] = {'include': [adgroup_id]}
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spTargetingClause.v3+json'
        self.headers["Accept"] = "application/vnd.spTargetingClause.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result

    def update_targeting(self, ex_type, value, target_id, expression_type, state, bid, access_token):
        url = f'{self.amazon_url}/sp/targets'
        post_data = {
            "targetingClauses": [
                {
                    "expression": [
                        {
                            "type": ex_type,
                            "value": value
                        }
                    ],
                    "targetId": target_id,
                    "expressionType": expression_type,
                    "state": state,
                    "bid": float(bid)
                }
            ]
        }
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spTargetingClause.v3+json'
        self.headers["Accept"] = "application/vnd.spTargetingClause.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.put_amazon_api(url, post_data, self.headers)
        return result

    def create_targeting(self, campaignId, ad_groupId, access_token):
        url = f'{self.amazon_url}/sp/targets'
        post_data = {
            "targetingClauses": [
                {
                    "campaignId": campaignId,
                    "expressionType": "AUTO",
                    "adGroupId": ad_groupId
                }
            ]
        }
        self.__make_headers()
        self.headers['Content-Type'] = 'application/vnd.spTargetingClause.v3+json'
        self.headers["Accept"] = "application/vnd.spTargetingClause.v3+json"
        self.headers['Authorization'] = f"Bearer {access_token}"
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result
