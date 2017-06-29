# -*- coding: utf-8 -*-
from django.db.models import Sum
from .models import WorkDate
from .settings import wd_settings
from .exceptions import WorkDateException
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _

def working_time(datetime_start, datetime_end):
    if isinstance(datetime_start, str):
        datetime_start = datetime.strptime(datetime_start, wd_settings.DATETIME_FORMAT)
    if isinstance(datetime_end, str):
        datetime_end = datetime.strptime(datetime_end, wd_settings.DATETIME_FORMAT)
    if datetime_start > datetime_end:
        raise WorkDateException(_('Start date/time must be lesser or equal than end.'))
    try:
        start_date = WorkDate.objects.get(date=datetime_start.date())
        end_date = WorkDate.objects.get(date=datetime_end.date())
    except WorkDate.DoesNotExist:
        raise WorkDateException(_('Selected dates not found in shedule.'))
    
    if start_date.date == end_date.date:
        start_time = max(datetime_start.time, start_date.get_start_time)
        end_time = min(datetime_end.time, start_date.get_end_time)
        return (end_time - start_time).total_seconds()
    
    summary_time = (start_date.get_end_time - datetime_start.time()).total_seconds()\
        if start_date.get_end_time > datetime_start.time() else 0
    summary_time += (end_date.get_start_time - datetime_end.time()).total_seconds()\
        if end_date.get_start_time > datetime_end.time() else 0
    total_time = WorkDate.objects.filter(is_weekend=False,\
                        date__gt=datetime_start.date(), date__lt=datetime_end.date(),\
                        start_time__isnull=False, end_time__isnull=False).aggregate(time_sum=Sum('seconds'))
    summary_time += total_time['time_sum']
    return summary_time

def from_this_time(hours):
    if hours <= 0:
        raise WorkDateException(_('Wrong hours count'))
    datetime_start = datetime.now()
    try:
        current_date = WorkDate.objects.get(date=datetime_start.date())
    except WorkDate.DoesNotExist:
        raise WorkDateException(_('Selected date not found in shedule.'))
    if current_date.get_end_datetime > datetime_start:
        delta = current_date.get_end_datetime - datetime_start
        current_hours = delta.total_seconds() // 3600
    else:
        current_hours = 0
    while current_hours < hours:
        try:
            current_date = WorkDate.objects.get(date=current_date.date+timedelta(days=1), is_weekend=False)
        except WorkDate.DoesNotExist:
            raise WorkDateException(_('Selected dates not found in shedule.'))
        current_hours += current_date.get_hours
    if current_hours > hours:
        diff = current_date.get_hours - (current_hours - hours)
        end_time = current_date.get_start_datetime + timedelta(hours=diff)
    else:
        end_time = current_date.get_end_datetime
    return end_time
