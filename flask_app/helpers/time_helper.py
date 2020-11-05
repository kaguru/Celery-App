from datetime import datetime
import pytz
import calendar

nairobi_tz =  pytz.timezone('Africa/Nairobi')


def get_current_kenya_time_utc():
    now_utc = datetime.utcnow()
    now_aware = now_utc.replace(tzinfo=pytz.UTC)
    now_aware_nairobi = now_aware.astimezone(nairobi_tz)
    now_aware_str = now_aware_nairobi.strftime("%d-%m-%Y %H:%M:%S")
    now_datetime_dt = datetime.strptime(now_aware_str, "%d-%m-%Y %H:%M:%S")
    return now_datetime_dt


def combine_mpesa_date_time(__date, __time):
    date_conv = datetime.strptime(__date, '%Y-%m-%d').date()
    time_conv = datetime.strptime(__time, '%H:%M:%S').time()
    datetime_combine = datetime.combine(date_conv, time_conv)
    return datetime_combine


def year_month_splitter(str_year_month):
    spt_str = str_year_month.split('-')
    item_month = int(spt_str[1])
    item_month_str = calendar.month_abbr[item_month]
    return f'{spt_str[0]} {item_month_str}'


def get_date(__input_datetime):
    date_conv = None
    if __input_datetime:
        date_conv = datetime.strptime(__input_datetime, '%Y-%m-%d').date()
    return date_conv


def format_date_string(input_date_string):
    input_date_datetime = datetime.strptime(input_date_string, '%Y-%m-%dT%H:%M:%S')
    return input_date_datetime
