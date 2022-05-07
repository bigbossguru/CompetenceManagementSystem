from django.db import models


class CostCenter(models.Model):
    """Cost Center Database Model"""

    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey('csm.Employee', on_delete=models.SET_NULL, related_name='cc_employees', null=True)

    def __str__(self) -> str:
        return f"{self.code}: {self.name}"
