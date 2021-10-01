import jdatetime
import datetime
import pytz

tz=pytz.timezone("Asia/Tehran")



def get_now():
    now=datetime.datetime.now()
    return now

def get_j_now():
    j_now=datetime.datetime.now(tz=tz)
    return str(j_now)

def get_g_date():
    now=datetime.datetime.now()
    g_date =str(now.year)+"-"+str(now.month)+"-"+str(now.day) #jdatetime.date(1397,11,2).togregorian()
    return str(g_date)


def get_j_date():
    now=datetime.datetime.now()
    j_date =  jdatetime.date.fromgregorian(day=now.day,month=now.month,year=now.year)
    return str(j_date)


def get_j_year():
    now=datetime.datetime.now()
    j_date =  jdatetime.date.fromgregorian(day=now.day,month=now.month,year=now.year)
    arr_j_date=str(j_date).split("-")
    j_year=arr_j_date[0]
    return str(j_year)

def get_j_month():
    now=datetime.datetime.now()
    j_date =  jdatetime.date.fromgregorian(day=now.day,month=now.month,year=now.year)
    arr_j_date=str(j_date).split("-")
    j_month=arr_j_date[1]
    return str(j_month)

def get_j_day():
    now=datetime.datetime.now()
    j_date =  jdatetime.date.fromgregorian(day=now.day,month=now.month,year=now.year)
    arr_j_date=str(j_date).split("-")
    j_day=arr_j_date[2]
    return str(j_day)

def get_j_hour():
    j_now=datetime.datetime.now(tz=tz)
    hour=str(j_now.hour)
    if len(hour)==1:
        hour="0"+hour
    return hour


def get_j_time():
    now=datetime.datetime.now()
    j_now=datetime.datetime.now(tz=tz)
    second=str(j_now.minute)
    if(len(second)==1):
        second="0"+str(second)
    j_time=str(j_now.hour)+"-"+second+"-"+str(j_now.second)
    return str(j_time)


def get_j_time_micro():
    j_now=datetime.datetime.now(tz=tz)
    second=str(j_now.minute)
    if(len(second)==1):
        second="0"+str(second)
    j_time_micro=str(j_now.hour)+"-"+second+"-"+str(j_now.second)+"-"+str(j_now.microsecond)
    return str(j_time_micro)