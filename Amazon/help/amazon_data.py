import loguru
import help.mysql_helper as mysql

lg = loguru.logger

# amazon_db = mysql.DataContext('localhost', 3306, 'root', 'root', 'amazon_work')
world_db = mysql.DataContext('192.168.1.28', 3306, 'root', 'root@123', 'world')


def get_campaings_data(shop):
    sql = f'select campaign_id,name,campaign_type,targeting_type,premium_bid_adjustment,daily_budget,state,portfolioId from campaign where shop ="{shop}"'
    date_list = world_db.exec_query_as_dict(sql)
    if date_list is not None and len(date_list) > 0:
        return date_list
    else:
        return None


def get_asin_list_by_asin(asin):
    sql = f'select sku from captainbi_sku where asin ="{asin}" and sku NOT LIKE "amzn.gr%" '
    data_list = world_db.exec_query_as_dict(sql)
    sku_list = []
    if data_list:
        for data in data_list:
            sku = data.get('sku')
            sku_list.append(sku)
    return list(set(sku_list))


def get_asin_info_by_asin(asin):
    sql = f'select sku from captainbi_sku where asin ="{asin}" and sku NOT LIKE "amzn.gr%" and sku not like "%=%"'
    data = world_db.exec_query_one_as_dict(sql)
    if data:
        sku = data.get('sku')
        return sku
    return False


print(get_asin_info_by_asin('B09TZXZDYX'))

# def create_table(table_name, columns):
#     lg.info(f'{table_name},{columns}')
#     amazon_db.exec_create_table(table_name=table_name, columns=columns)


def set_sp_campaigns_date():
    pass


# def insert_batch_data(data_list, table_name):
#     # 获取字典中的所有键
#     keys = data_list[0].keys()
#     lg.info(f'{keys}')
#     # 构建插入语句的参数部分
#     placeholders = ', '.join(['%s'] * len(keys))
#
#     # 构建插入语句
#     query = f"INSERT INTO {table_name} ({', '.join(keys)}) VALUES ({placeholders})"
#     lg.info(f'{query}')
#     # 构建参数列表
#     values = [tuple(d.values()) for d in data_list]
#     lg.info(f'{values}')
#     # 执行批量插入
#     amazon_db.exec_many_non_query(query, values)


def get_client_id_by_ad_name(ad_name):
    sql = f'select * from ad_api_message  where ad_name ="{ad_name}"'
    data = world_db.exec_query_one_as_dict(sql)
    return data


# print(get_client_id_by_ad_name('TooCust-mx'))

def get_portfolio_id_by_portfolio(portfolio):
    sql = f'select Portfolio_id from portfolios where Portfolio_name="{portfolio}"'
    data = world_db.exec_query_one_as_dict(sql)
    if data:
        portfolio_id = data.get('Portfolio_id')
        return portfolio_id
    return None

# # 示例数据
# data_list = [
#     {'name': 'John', 'age': 25, 'city': 'New York'},
#     {'name': 'Jane', 'age': 30, 'city': 'Los Angeles'},
#     {'name': 'Mike', 'age': 35, 'city': 'Chicago'}
# ]

# # 调用方法将数据批量写入数据库
# insert_batch_data(data_list, 'your_table_name')  # 替换成你的表名

#
# def get_campaigns_data():
#     sql = 'select * from campaign'
#     result = cur.execute_query(sql)
#     return result
#
#
# def get_table_head():
#     # 获取表头
#     sql = "SHOW FIELDS FROM campaign"
#     labels = cur.execute_query(sql)
#     lg.info(f'{labels}')
#     labels = [l[0] for l in labels]
#     return labels


# results = get_campaings_data()
# for item in results:
#     print(item)
