from django.db import models
from solo.models import SingletonModel


class SystemConfiguration(SingletonModel):
    start_update_datetime = models.DateTimeField()
    end_update_datetime = models.DateTimeField()
    files_detail = models.ManyToManyField('FilesDetail')
    service_emails = models.ManyToManyField('ServiceEmail')

    def __str__(self):
        return "System Configuration"


class ServiceEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class FilesDetail(models.Model):
    file_name = models.CharField(max_length=250)
    start_header = models.PositiveSmallIntegerField()
    required = models.BooleanField(default=True)
    file_upload = models.FileField(null=True)

    def __str__(self):
        return self.file_name
