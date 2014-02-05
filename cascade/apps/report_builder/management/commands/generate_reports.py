__author__ = 'jbennett'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from cascade.apps.report_builder.models import Report
from optparse import make_option

class Command(BaseCommand):
    args = '<site1, site2 ...>'
    help = 'generates a fill for reports on all sites'
    option_list = BaseCommand.option_list + (
        make_option('--username',
                    action='store',
                    type='string',
                    dest='username',
                    default=None,
                    help='enter username',
                    ),

    )

    def handle(self, *args, **options):
        if options['username']:
            user = User.objects.get(username=options['username'])
            if not args:
                if user:
                    reports = Report.objects.all()
                    for report in reports:
                        report.generate_report_sites(user)
            else:
                for site_name in args:
                    site = Site.objects.get(name=site_name)
                    reports = Report.objects.filter(site=site)
                    for report in reports:
                        report.generate_report(user, site)



