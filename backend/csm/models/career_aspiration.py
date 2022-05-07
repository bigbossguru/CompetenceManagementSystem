from django.db import models
from simple_history.models import HistoricalRecords


class CareerAspiration(models.Model):
    """Career Aspirations for each Employee Database Model"""

    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    employee = models.OneToOneField(
        'csm.Employee',
        on_delete=models.CASCADE,
        related_name='ca_employees',
        unique=True
    )
    current_stage = models.CharField(max_length=250, null=True)
    stay_current_position = models.CharField(max_length=50, null=True)
    expertise = models.CharField(max_length=50, null=True)
    eligibility = models.CharField(max_length=50, null=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    new_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    increase_proposal = models.CharField(max_length=50, null=True)
    budget = models.CharField(max_length=50, null=True)
    risk_resignation = models.CharField(max_length=50, null=True)
    successor1 = models.ForeignKey('csm.Employee', on_delete=models.SET_NULL, related_name='successors1', null=True)
    successor2 = models.ForeignKey('csm.Employee', on_delete=models.SET_NULL, related_name='successors2', null=True)
    successor3 = models.ForeignKey('csm.Employee', on_delete=models.SET_NULL, related_name='successors3', null=True)
    comments = models.TextField(blank=True, null=True)
    create_date = models.DateField(auto_now=True)
    history = HistoricalRecords(related_name='history_ca')

    def __str__(self) -> str:
        return f"CareerAspiration {self.employee}"
