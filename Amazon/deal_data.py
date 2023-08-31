import help.mysql_helper as hmh
import loguru

lg = loguru.logger

local_db = hmh.DataContext('localhost', 3306, 'root', 'root', 'amazon_work')


def create_data(rows):
    query = (
        f"INSERT INTO amzasin_searchterm (Campaign_Name,Advertised_ASIN,Impressions,Clicks,Spend,Day7_Total_Sales,Day7_TotalUnits,campaign_id,ad_group_id,Date) "
        f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    local_db.exec_many_non_query(query, rows)


def create_data_asin(rows):
    query = (
        f"INSERT INTO searchamzasin (ASIN,Date,Customer_Search_Term"
        f",campaign_id,Targeting,ad_group_id,Total_Impressions,Total_Clicks,TotalOrders,TotalUnits,TotalSales,Spend) "
        f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    local_db.exec_many_non_query(query, rows)

    # query = (
    #     f"INSERT INTO searchamzasin ('ASIN','Year_Month','Customer_Search_Term','campaign_id','Targeting','ad_group_id','Total_Impressions','Total_Clicks','TotalOrders','TotalUnits','TotalSales','Spend') "
    #     f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    # local_db.exec_many_non_query(query, rows)


world_db = hmh.DataContext('192.168.1.28', 3306, 'root', 'root@123', 'world')

sql = """	SELECT            `amzasin`.`Advertised_ASIN` AS `ASIN`,
            CONCAT(
                YEAR(`searchterm`.`Date`), '-', LPAD(MONTH(`searchterm`.`Date`), 2, '0')
            ) AS `Year_Month`,
            `searchterm`.`Customer_Search_Term` AS `Customer_Search_Term`,
            amzasin.campaign_id as campaign_id,
            searchterm.Targeting as Targeting,
            amzasin.ad_group_id as ad_group_id,
            SUM(`searchterm`.`Impressions`) AS `Total_Impressions`,
            SUM(`searchterm`.`Clicks`) AS `Total_Clicks`,
            SUM(`searchterm`.`Day7_TotalOrders`) AS `TotalOrders`,
            SUM(`searchterm`.`Day7_TotalUnits`) AS `TotalUnits`,
            SUM(`searchterm`.`Day7_TotalSales`) AS `TotalSales`,
            SUM(`searchterm`.`Spend`) AS `Spend`
        FROM
            `amzasin`
        JOIN
            `searchterm` ON `amzasin`.`campaign_id` = `searchterm`.`campaign_id`
        WHERE
            YEAR(`searchterm`.`Date`) = 2023
            AND MONTH(`searchterm`.`Date`) = 8
        GROUP BY
            `amzasin`.`Advertised_ASIN`,
            YEAR(`searchterm`.`Date`),
            MONTH(`searchterm`.`Date`)"""
rows = world_db.exec_query(sql)
create_data_asin(rows)
# for i in rows:
#     print(i)
# world_db = hmh.DataContext('192.168.1.28', 3306, 'root', 'root@123', 'world')
# page_size = 1000
# page_number = 1
# while True:
#     sql = f"""SELECT amzasin.Campaign_Name,amzasin.Advertised_ASIN,
#         amzasin.Impressions,amzasin.Clicks,amzasin.Spend,
#         amzasin.Day7_Total_Sales,amzasin.Day7_TotalUnits,
#         amzasin.campaign_id,amzasin.ad_group_id , searchterm.Date
#     FROM amzasin
#     JOIN searchterm ON amzasin.campaign_id = searchterm.campaign_id
#         AND amzasin.ad_group_id = searchterm.ad_group_id
#     LIMIT {(page_number - 1) * page_size} ,{page_size} """
#     lg.info(f'{sql}')
#     rows = world_db.exec_query(sql)
#     create_data(rows)
#     # for row in rows:
#     #     print(row)
#     if len(rows) < page_size:
#         break
#     page_number += 1
