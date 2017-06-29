# -*- coding: utf-8 -*-

from django.conf import settings


class Settings(object):
    def __init__(self, **kwargs):
        self.defaults = kwargs

    def __getattr__(self, key):
        return getattr(settings, 'WORKDATES_%s' % key, self.defaults[key])


wd_settings = Settings(
    DATE_FORMAT='%d.%m.%Y',
    DATETIME_FORMAT='%d.%m.%Y %H:%M',
    SHEDULE_FILL_DAYS=30,
    DEFAULT_SHEDULE={
                'all':'08:00-18:00', # required
                '6':'08:00-16:00',
                'weekend':[6],
                }
)
