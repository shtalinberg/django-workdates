# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from .models import WorkDate


@admin.register(WorkDate)
class WorkDateAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'start_time', 'end_time', 'is_weekend', 'get_week_day')
    list_filter = ('is_weekend',)
    list_editable = ('start_time', 'end_time', 'is_weekend')
    search_fields = ['date', 'start_time', 'end_time']
    date_hierarchy = 'date'
    actions = ['mark_as_weekend', 'unmark_as_weekend']
    
    def mark_as_weekend(self, request, queryset):
        if queryset:
            queryset.update(is_weekend=True)
            messages.success(request, _('%d dates marked as weekend' % queryset.count()))
    
    def unmark_as_weekend(self, request, queryset):
        if queryset:
            queryset.update(is_weekend=False)
            messages.success(request, _('%d dates unmarked as weekend' % queryset.count()))
    
    mark_as_weekend.short_description = _('Mark as weekend')
    unmark_as_weekend.short_description = _('Unmark as weekend')
