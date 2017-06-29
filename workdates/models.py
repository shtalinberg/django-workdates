# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import date, datetime
from .settings import wd_settings


class WorkDate(models.Model):
    date = models.DateField(_('Date'), unique=True, db_index=True, default=date.today)
    start_time = models.TimeField(_('Start time'), blank=True, null=True)
    end_time = models.TimeField(_('End time'), blank=True, null=True)
    seconds = models.BigIntegerField(_('Seconds'), editable=False, default=0)
    is_weekend = models.BooleanField(_('Is weekend'), default=False)
    
    class Meta:
        verbose_name = _('Work date')
        verbose_name_plural = _('Work dates')

    def __unicode__(self):
        return '%s' % self.date.strftime(wd_settings.DATE_FORMAT)
    
    @property
    def get_start_time(self):
        if self.end_time is None:
            return None
        return self.start_time if self.start_time is not None\
            else datetime.strptime('00:00', '%H:%M')
    
    @property
    def get_end_time(self):
        if self.start_time is None:
            return None
        return self.end_time if self.end_time is not None\
            else datetime.strptime('23:59', '%H:%M')
    
    @property
    def get_seconds(self):
        return self.seconds if not self.is_weekend else 0
    
    @property
    def get_week_day(self):
        return u'%s' % _(self.date.strftime('%A'))
    
    @property
    def get_start_datetime(self):
        return datetime.combine(self.date, self.get_start_time)
    
    @property
    def get_end_datetime(self):
        return datetime.combine(self.date, self.get_end_time)
    
    @property
    def get_hours(self):
        return self.get_end_time.hour - self.get_start_time.hour
    
    def save(self, *args, **kwargs):
        if self.get_end_time is None:
            self.seconds = 0
        else:
            self.seconds = (self.get_end_time - self.get_start_time).total_seconds()
        super(WorkDate, self).save(*args, **kwargs)
    
    def clean(self):
        if self.start_time is None and self.end_time is None:
            return
        if self.start_time >= self.end_time:
            raise ValidationError(_('Start time must be lesser than end time'))
