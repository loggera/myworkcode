import API.amazon_api as ama_api
import service.amazon_token as sat
import loguru
import help.amazon_data as had

lg = loguru.logger
sp_api = ama_api.AmazonAPI('2355346886591079', 'amzn1.application-oa2-client.652f99ef3ff840a5bef05e5eb3a2e308')


# 调用获取campaigns列表接口
def get_sp_campaigns(next_token):
    access_token = sat.get_amazon_token(None)
    result = sp_api.sp_campaigns_list(access_token, next_token)
    if result.get('code') == 200:
        api_req = sp_campaigns_data(result)
        # data_list = api_req['result']
        # lg.info(f'{data_list}')
        # lg.info(f'{len(data_list)}')
        next_token = api_req['nextToken']
        lg.info(f'{next_token}')
        if next_token:
            get_sp_campaigns(next_token)
        return
        #     # lg.info(f'{data_dic}')
        # result = sp_api.sp_campaigns_list(access_token, next_token)
    elif result.get('code') == 403:
        access_token = sat.get_amazon_token(True)
        result = sp_api.sp_campaigns_list(access_token, None)


# 处理获取到的campaigns 的数据
def sp_campaigns_data(result):
    api_req = {}
    data = result.get('result')
    # lg.info(f'{data}')
    next_token = data.get('nextToken')
    # lg.info(f'{next_token}')
    data_list = data.get('campaigns')
    # 即将写入数据库的数据
    result_list = []
    for data_dic in data_list:
        result_dic = {}
        budget = data_dic.get('budget').get('budget')
        if not budget:
            budget = 'Null'
        result_dic['budget'] = budget
        budget_type = data_dic.get('budget').get('budgetType')
        result_dic['budgetType'] = budget_type
        check_list = ['campaignId', 'name', 'state']
        data_dic = check_value(data_dic, check_list)
        result_dic['campaignId'] = data_dic.get('campaignId')
        result_dic['name'] = data_dic.get('name')
        result_dic['state'] = data_dic.get('state')
        result_list.append(result_dic)

    if result_list:
        set_campaigns_to_mysql(result_list)
        api_req['nextToken'] = next_token
        return api_req
    else:
        return {}


# 检查字段的值是否存在
def check_value(data_dic, check_list):
    for i in check_list:
        if not data_dic.get(i):
            data_dic[i] = 'Null'
    return data_dic


# 批量写入mysql方法
def set_campaigns_to_mysql(result):
    had.insert_batch_data(result, 'campaign')

# if __name__ == '__main__':
#     get_sp_campaigns(None)
