from django.db import models
from simple_history.models import HistoricalRecords


class AACompetence(models.Model):
    """General Annual Appraisal Competence Database Model"""

    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=250)
    weight = models.PositiveSmallIntegerField(default=5)

    def __str__(self) -> str:
        return f"{self.code}: {self.name}"


class EmployeeAACompetence(models.Model):
    """Employee with Complete Annual Appraisal Competence Database Model"""

    appraisal_id = models.CharField(max_length=50, null=True)
    year = models.IntegerField(null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    employee = models.ForeignKey('csm.Employee', on_delete=models.CASCADE, related_name='aa_employees')
    interview_date = models.DateField(null=True)
    stage = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    competence = models.ForeignKey(AACompetence, on_delete=models.CASCADE, related_name='aa_competences')
    rating = models.CharField(max_length=50, null=True)
    expected_lvl = models.CharField(max_length=50, null=True)
    create_date = models.DateField(auto_now_add=True)
    history = HistoricalRecords(related_name='history_aa_competence')

    def __str__(self) -> str:
        return f"{self.competence} - {self.employee}"

    class Meta:
        ordering = ['-create_date']
        unique_together = [['employee', 'competence']]
        constraints = [
            models.UniqueConstraint(fields=['employee', 'competence'], name='employee_aacompet')
        ]


class FullAACompetence(models.Model):
    """Full Annual Appraisal Report for each Employee"""

    appraisal_id = models.CharField(max_length=50, null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    employee = models.OneToOneField(
        'csm.Employee',
        on_delete=models.CASCADE,
        related_name='fullaa_employees',
        unique=True
    )
    interview_date = models.DateField(null=True)
    stage = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    date_completed_on = models.DateField(null=True)
    next_date_career_discus = models.DateField(null=True)
    performance = models.CharField(max_length=50, null=True)
    trend = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True)
    level = models.CharField(max_length=50, null=True)
    key_specific_obj = models.CharField(max_length=50, null=True)
    general_mission = models.CharField(max_length=50, null=True)
    demonstrated_behavior = models.CharField(max_length=50, null=True)
    leadership = models.CharField(max_length=50, null=True)
    comments = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(related_name='history_fullaa_competence')

    def __str__(self) -> str:
        return f"FullAA {self.employee}"

    class Meta:
        ordering = ['-create_date']
