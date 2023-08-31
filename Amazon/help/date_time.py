# -*- coding:utf-8 -*-
import datetime
from dateutil import tz
from dateutil.relativedelta import relativedelta
from dateutil import rrule
import time

cn_zone = tz.gettz('Asia/Shanghai')


def get_now():
    return datetime.datetime.now(tz=cn_zone)


def make_stamp_by_time(time_yyr):
    nyr_time = time.strptime(time_yyr, "%Y-%m-%d %H:%M:%S")
    nyr_time_stamp = int(time.mktime(nyr_time))
    return nyr_time_stamp


def get_now_time():
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(get_now_timestamp()))
    return now_time


def get_now_timestamp():
    return int(get_now().timestamp())


def get_now_time_data():
    now_time = time.strftime('%Y-%m-%d', time.localtime(get_now_timestamp()))
    return now_time


def get_today_min_time():
    now_time = time.strftime('%Y-%m-%d', time.localtime(get_now_timestamp()))
    now_time = f'{now_time} 00:00:00'
    return now_time


def get_next_day_stamp():
    month_date = datetime.datetime.now().date() + relativedelta(days=1)
    month_date = str(month_date) + ' ' + '00:00:00'
    time_stamp = time.mktime(time.strptime(month_date, '%Y-%m-%d %H:%M:%S'))
    return int(time_stamp)


def get_long_now_timestamp():
    return int(get_now().timestamp() * 1000)


def get_now_date_start_time():
    return get_date_start_time(get_now())


def get_format_year_month(date):
    return date.strftime('%Y-%m')


def get_format_date(date):
    return date.strftime('%Y-%m-%d')


def get_format_time(date):
    return date.strftime('%H:%M:%S')


def get_format_data_by_number(date):
    return date.strftime('%Y%m%d')


def get_format_data_by_ymdhms(date):
    return date.strftime('%Y%m%d%H%M%S')


def get_format_data_by_ymdh(date):
    return date.strftime('%Y%m%d%H')


def get_format_date_time(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def get_date_start_time(date_time):
    return datetime.datetime.combine(date_time.date(), datetime.time.min)


def get_date_end_time(date_time):
    return get_format_date_time(datetime.datetime.combine(date_time.date(), datetime.time.max))


def add_day(date, day):
    return date + datetime.timedelta(days=day)


def get_today_time():
    today = datetime.datetime.today()
    return today


def get_today_zero_time():
    today = get_today_time()
    today_zero = today.replace(hour=0, minute=0, second=0, microsecond=0)
    return today_zero


def get_yestarday_time():
    return get_today_zero_time() - datetime.timedelta(days=1)


def get_tomorrow_time():
    return get_today_zero_time() + datetime.timedelta(days=1)


def add_month(date, month):
    return date + relativedelta(months=month)


def add_hour(date, hour):
    return date + datetime.timedelta(hours=hour)


def add_minute(date, minute):
    return date + datetime.timedelta(minutes=minute)


def parse_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d')


def parse_date_number(str_date):
    return datetime.datetime.strptime(str_date, '%Y%m%d')


def parse_date_time(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')


def diff_hour_now(start_time):
    left = get_format_date_time(start_time)
    right = get_format_date_time(get_now())
    return rrule.rrule(rrule.HOURLY, dtstart=parse_date_time(left), until=parse_date_time(right)).count()


def get_rucker_finance_month(date):
    finance_month = get_format_year_month(date)
    if date.day > 25:
        finance_month = get_format_year_month(add_day(date, 10))
        pass
    return finance_month


def get_info_sign_timestamp(now_time):
    hour_time_list = [i for i in range(0, 25, 3)]
    now_hour = int(str(now_time).split(' ')[1].split(':')[0])
    hour_index = int(now_hour / 3)
    hour = hour_time_list[hour_index]
    now_time_year_mon_day = str(now_time).split(' ')[0].replace('-', '')
    return f'{now_time_year_mon_day}{hour}'


def get_info_entry_timestamp(now_time):
    hour_time_list = [i for i in range(0, 25, 3)]
    now_hour = int(str(now_time).split(' ')[1].split(':')[0])
    now_minute = int(str(now_time).split(' ')[1].split(':')[1])
    hour_index = int(now_hour / 3)
    hour = hour_time_list[hour_index]
    now_time_year_mon_day = str(now_time).split(' ')[0].replace('-', '')
    return f'{now_time_year_mon_day}{hour}{now_minute}'


def compare_time(compare_first_time, compare_second_time, compare):
    compare_first_time = time.mktime(time.strptime(compare_first_time, '%Y-%m-%d %H:%M:%S'))
    compare_second_time = time.mktime(time.strptime(compare_second_time, '%Y-%m-%d %H:%M:%S'))
    if compare == '大于':
        return compare_first_time > compare_second_time
    if compare == '小于':
        return compare_first_time < compare_second_time
    if compare == '大于等于':
        return compare_first_time >= compare_second_time
    if compare == '小于等于':
        return compare_first_time <= compare_second_time
    else:
        return False


def add_one_hours(str_time):
    time_aq = parse_date_time(str_time)
    hour_date = time_aq + relativedelta(hours=1)
    return hour_date


def jian_one_s(str_time):
    time_aq = parse_date_time(get_format_date_time(str_time))

    hour_date = time_aq - relativedelta(seconds=2)
    return hour_date


def get_now_time_all():
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(get_now_timestamp()))
    return now_time


def get_format_day_by_timestamp(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-09 18:59:20)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

