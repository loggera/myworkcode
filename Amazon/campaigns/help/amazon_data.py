import campaigns.help.mysql as chm
import loguru
import campaigns.help.mysql_helper as mysql

lg = loguru.logger

amazon_db = mysql.DataContext('localhost', 3306, 'root', 'root', 'amazon_work')

cur = chm.MySQLHelper()
cur.connect()


def get_campaings_data():
    sql = f'select budget,budgetType,campaignId,name,portfolioId,state from campaign'
    date_list = amazon_db.exec_query_as_dict(sql)
    if date_list is not None and len(date_list) > 0:
        return date_list
    else:
        return None


def create_campaigns_data_to_mylocal_db(value):
    # sql = "insert into campaign ('budget','budgetType','campaignId','name','portfoliold','startDate','state','targetingType') values (%s,%s,%s,%s,%s,%s,%s,%s)"
    sql = 'insert into campaign (`budget`,`budgetType`,`campaignId`,`name`,`portfolioId`,`startDate`,`state`,`targetingType`) values (%s,%s,%s,%s,%s,%s,%s,%s)'

    cur.execute_batch_create(sql, value)

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
