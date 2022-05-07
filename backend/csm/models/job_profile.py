from django.db import models


class JobProfile(models.Model):
    """Job profile Database Model"""

    code = models.CharField(max_length=6)
    jobtitle = models.CharField(max_length=250)
    metier_field = models.CharField(max_length=250, null=True)
    metier = models.ForeignKey('csm.Employee', on_delete=models.SET_NULL, related_name='job_prof_metiers', null=True)

    def __str__(self) -> str:
        return f"{self.code}: {self.jobtitle}"
