import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from csm.models.user import UserAccessReport


class Command(BaseCommand):
    def handle(self, *args, **options):
        Users = get_user_model()
        name_reports = [f'RA{i}' for i in range(1, 10)]
        name_reports += [f'RB{i}' for i in range(1, 7)]
        name_reports += [f'RC{i}' for i in range(1, 6)]

        for user in Users.objects.all():
            for name_report in name_reports:
                UserAccessReport.objects.create(
                    user=user,
                    name=name_report,
                    is_access=True,
                )
