import datetime
from datetime import date
from Cian.config import DATES


# this function accept int: year, int: month, int: day and return datetime object
def convert_to_datetime(year, month, day, time):
    date_string = f"{year}-{month}-{day} {int(time)}:{int((time - int(time)) * 60)}"
    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M")
    return date_object


# this function return datetime object from date string:
def current_date(date_string):
    # cut unusefull information:
    date_list = date_string[11:].split(',')
    # check date:
    if date_list[0] == "сегодня":
        # today date/time:
        today_date = date.today()
        year, month, day = today_date.year, today_date.month, today_date.day
        # srt --> time object:
        time_string = date_list[1].replace(' ', '')
        time_datetime = datetime.datetime.strptime(time_string, "%H:%M").time()
        time = float(time_datetime.hour) + float(time_datetime.minute) / 60

        return convert_to_datetime(year, month, day, time)

    elif date_list[0] == "вчера":
        today_date = date.today()
        yesterday_date = today_date - datetime.timedelta(days=1)
        yesterday_date.strftime('%Y-%m-%d')
        year, month, day = yesterday_date.year, yesterday_date.month, yesterday_date.day
        # srt --> time object:
        time_string = date_list[1].replace(' ', '')
        time_datetime = datetime.datetime.strptime(time_string, "%H:%M").time()
        time = float(time_datetime.hour) + float(time_datetime.minute) / 60

        return convert_to_datetime(year, month, day, time)

    else:
        # get today year:
        current_year = datetime.datetime.now().year
        # day + month list:
        day_month_list = date_list[0].split(' ')
        # current day:
        day = int(day_month_list[0])
        # current month
        month = DATES[day_month_list[1]]
        # current time:
        time = float(date_list[1].replace(':', '.'))

        return convert_to_datetime(current_year, month, day, time)