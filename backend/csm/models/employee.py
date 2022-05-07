from django.db import models
from simple_history.models import HistoricalRecords

from csm.models.hyperion import Hyperion
from csm.models.job_profile import JobProfile
from csm.models.cost_center import CostCenter


class Employee(models.Model):
    """Employee Database Model"""

    ps_id = models.PositiveIntegerField(primary_key=True)
    person_id = models.PositiveIntegerField(null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    cadre = models.CharField(max_length=50, null=True)
    full_part_time = models.CharField(max_length=50, null=True)
    fte = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    type_of_contract = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    orgaloc = models.CharField(max_length=7, null=True)
    start_date = models.DateField(null=True)
    bg = models.CharField(max_length=50, null=True)
    pg = models.CharField(max_length=50, null=True)
    pl = models.CharField(max_length=50, null=True)
    tpl = models.CharField(max_length=50, null=True)
    hn1 = models.ForeignKey("Employee", on_delete=models.SET_NULL, related_name='hn1s', null=True)
    hn2 = models.ForeignKey("Employee", on_delete=models.SET_NULL, related_name='hn2s', null=True)
    fn1 = models.ForeignKey("Employee", on_delete=models.SET_NULL, related_name='fn1s', null=True)
    hyperion = models.ForeignKey(Hyperion, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(JobProfile, on_delete=models.SET_NULL, null=True)
    cc = models.ForeignKey(CostCenter, on_delete=models.SET_NULL, null=True)
    # tpl_owner = models.ForeignKey("Employee", on_delete=models.SET_NULL, related_name='tpl_owners', null=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(related_name='history_employee')

    def __str__(self) -> str:
        return f"{self.ps_id}: {self.first_name},{self.last_name}"
