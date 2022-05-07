import datetime
from django.core.management.base import BaseCommand
from csm.models.system_config import SystemConfiguration, ServiceEmail, FilesDetail


class Command(BaseCommand):
    def handle(self, *args, **options):
        list_of_filename = [
            'template CDA', 'template MASTER DATA', 'template AA Competence',
            'template AA Full', 'template CA', 'template PS'
        ]
        service_email = ServiceEmail.objects.create(
            email='changeme@email.com'
        )
        system_config = SystemConfiguration.objects.create(
            start_update_datetime=datetime.datetime.now(),
            end_update_datetime=datetime.datetime.now()
        )
        for file_name in list_of_filename:
            file_detail = FilesDetail.objects.create(
                file_name=file_name,
                start_header=0,
                required=True
            )
            system_config.files_detail.add(file_detail)
        system_config.service_emails.add(service_email)
