import django_filters
from csm.models.rd_competence import EmployeeRDCompetence
from csm.models.aa_competence import EmployeeAACompetence, FullAACompetence
from csm.models.career_aspiration import CareerAspiration


class EmployeeRDCompetenceFilter(django_filters.FilterSet):
    create_date = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = EmployeeRDCompetence
        fields = ['employee__first_name', 'employee__last_name', 'competence__name',
                  'employee__ps_id', 'competence__type', 'competence__metier_org',
                  'competence__category', 'competence__domain', 'platform__platform_id',
                  'platform__name', 'metier_field__metier_field_id', 'metier_field__name',
                  'metier_field__bg', 'create_date', 'competence__competence_id']


class EmployeeAACompetenceFilter(django_filters.FilterSet):
    interview_date = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = EmployeeAACompetence
        fields = ['employee__first_name', 'employee__last_name', 'competence__name',
                  'competence__code', 'employee__ps_id', 'year', 'interview_date']


class EmployeeFullAACompetenceFilter(django_filters.FilterSet):
    from_date = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = FullAACompetence
        fields = ['employee__first_name', 'employee__last_name', 'employee__ps_id', 'from_date']


class CareerAspirationFilter(django_filters.FilterSet):
    from_date = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CareerAspiration
        fields = ['employee__first_name', 'employee__last_name', 'employee__ps_id', 'from_date']
