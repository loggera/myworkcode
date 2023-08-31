import campaigns.service.amazon_token as sv_amazon_token
import campaigns.help.request_client as hrc
import loguru
import campaigns.help.amazon_data as amazon_data

lg = loguru.logger
access_token = sv_amazon_token.get_amazon_token()
headers = {
    "Authorization": f"Bearer {access_token}",
    "Amazon-Advertising-API-Scope": "2355346886591079",
    "Amazon-Advertising-API-ClientId": "amzn1.application-oa2-client.652f99ef3ff840a5bef05e5eb3a2e308"
}


class Campaign:
    def __init__(self):
        self.sp_url = 'https://advertising-api.amazon.com'
        # self.amazon_token = sv_amazon_token.get_amazon_token()
        self.headers = headers

    def sp_campaigns(self):
        url = f'{self.sp_url}/sp/campaigns/list'
        post_data = {
            # "campaignIdFilter": {
            #     "include": [
            #         "231526480252427"
            #     ]
            # },
            # "portfolioIdFilter": {
            #     "include": [
            #         "35339171199537"
            #     ]
            # },
            "stateFilter": {
                "include": [
                    "ENABLED"
                ]
            }}
        #     "maxResults": 0,
        #     "nextToken": f'Bearer {access_token}',
        #     "includeExtendedDataFields": True,
        #     "nameFilter": {
        #         "queryTermMatchType": "BROAD_MATCH",
        #         "include": [
        #             "8.9--liu--A--Head Guard"
        #         ]
        #     }
        # }
        # self.headers["Content-Type"] = "application/vnd.spcampaign.v3+json"
        self.headers["Accept"] = "application/vnd.spcampaign.v3+json"
        lg.info(f'{self.headers}')
        result = hrc.post_amazon_api(url, post_data, self.headers)
        return result


campaign = Campaign()
result_list = campaign.sp_campaigns().get('campaigns')
campaign_data_list = []
for result in result_list:
    budget = result.get('budget').get('budget')
    budget_type = result.get('budget').get('budgetType')
    campaign_id = result.get('campaignId')
    name = result.get('name')
    portfolio_id = result.get('portfolioId')
    start_date = result.get('startDate')
    state = result.get('state')
    targeting_type = result.get('targetingType')
    data = (budget, budget_type, campaign_id, name, portfolio_id, start_date, state, targeting_type)
    campaign_data_list.append(data)
print(campaign_data_list)

amazon_data.create_campaigns_data_to_mylocal_db(campaign_data_list)
