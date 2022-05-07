from django.db import models
from simple_history.models import HistoricalRecords


class RDCompetence(models.Model):
    """General R&D Competence Database Model"""

    competence_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    metier_org = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    domain = models.CharField(max_length=250)
    weight = models.PositiveSmallIntegerField(default=5)

    def __str__(self) -> str:
        return f"{self.competence_id}: {self.name}"


class EmployeeRDCompetence(models.Model):
    """Employee with Complete R&D Competence Database Model"""

    employee = models.ForeignKey(
        'csm.Employee',
        on_delete=models.CASCADE,
        related_name='rd_employees'
    )
    platform = models.ForeignKey('Platform', on_delete=models.SET_NULL, null=True)
    metier_field = models.ForeignKey('MetierField', on_delete=models.SET_NULL, null=True)
    competence = models.ForeignKey(
        RDCompetence,
        on_delete=models.CASCADE,
        related_name='rd_competences'
    )
    expected_lvl = models.SmallIntegerField(default=0)
    manager_expected_lvl = models.SmallIntegerField(default=0)
    acquired_lvl = models.SmallIntegerField(default=0)
    gap = models.SmallIntegerField(default=0)
    coverage = models.FloatField(default=0)
    create_date = models.DateField(auto_now_add=True)
    history = HistoricalRecords(related_name='history_rd_competence')

    def __str__(self) -> str:
        return f"{self.competence} - {self.employee}"

    class Meta:
        ordering = ['-create_date']
        unique_together = [['employee', 'competence']]
        constraints = [
            models.UniqueConstraint(fields=['employee', 'competence'], name='employee_rdcompet')
        ]


class MetierField(models.Model):
    """Metier Field Database Model"""

    metier_field_id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    bg = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.metier_field_id}: {self.name}"


class Platform(models.Model):
    """Platform Database Model"""

    platform_id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.platform_id}: {self.name}"
