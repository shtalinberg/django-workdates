# -*- coding: utf-8 -*-
import traceback
from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext_lazy as _
from workdates.models import WorkDate
from workdates.settings import wd_settings
from workdates.exceptions import WorkDateException
from datetime import date, timedelta, datetime


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            shedule = wd_settings.DEFAULT_SHEDULE
            
            if not 'all' in shedule:
                raise WorkDateException(_('Default shedule for all days not found'))
            if not 'weekend' in shedule:
                raise WorkDateException(_('Default weekend not found'))
            
            qs = WorkDate.objects.all()
            if qs.count() > 0:
                start_date = qs.latest().date+timedelta(days=1)
            else:
                start_date = date.today()
            for i in range(1, wd_settings.SHEDULE_FILL_DAYS):
                wday = start_date.weekday()
                wdate = WorkDate(date=start_date)
                if wday in shedule['weekend']:
                    wdate.is_weekend = True
                if str(wday) in shedule:
                    work_time = shedule[str(wday)]
                else:
                    work_time = shedule['all']
                work_times = work_time.split('-')
                wdate.start_time = datetime.strptime(work_times[0], '%H:%M')
                wdate.end_time = datetime.strptime(work_times[1], '%H:%M')
                wdate.save()
                start_date += timedelta(days=1)
            print(_('Shedule for %d days created' % wd_settings.SHEDULE_FILL_DAYS))
        except Exception, WorkDateException:
            traceback.print_exc()
