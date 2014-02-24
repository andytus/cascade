from __future__ import absolute_import

from celery import shared_task
from .models import Report

@shared_task
def task_generate_report(report_id, user, site):
    report = Report.objects.get(pk=report_id, site=site)
    report.generate_report(user, site)

@shared_task
def task_generate_all_reports(report, user):
    report.generate_report_sites(user)
