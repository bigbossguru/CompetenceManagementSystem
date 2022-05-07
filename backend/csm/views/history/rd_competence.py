from django.db.models import Q
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics

from csm.models.rd_competence import EmployeeRDCompetence
from csm.serializers.rd_competence import (
    EmployeeRDCompetenceListDetailSerializer
)


class HistoryEmployeeRDCompetenceFilter(FilterSet):
    history_date = CharFilter(lookup_expr='icontains')
    employee__first_name = CharFilter()
    employee__last_name = CharFilter()
    competence__name = CharFilter()
    employee__ps_id = CharFilter()
    competence__type = CharFilter()
    competence__metier_org = CharFilter()
    competence__category = CharFilter()
    competence__domain = CharFilter()
    platform__platform_id = CharFilter()
    platform__name = CharFilter()
    metier_field__metier_field_id = CharFilter()
    metier_field__name = CharFilter()
    metier_field__bg = CharFilter()
    create_date = CharFilter()
    competence__competence_id = CharFilter()


class HistoryEmployeeRDCompetenceListDetailView(generics.ListAPIView):
    """
    Detail overview of assignment RD competencies to Employees
    """
    serializer_class = EmployeeRDCompetenceListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoryEmployeeRDCompetenceFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return EmployeeRDCompetence.history.all()
        if self.request.user.is_manager:
            employees_under_manager = EmployeeRDCompetence.history.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= EmployeeRDCompetence.history.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return EmployeeRDCompetence.history.filter(employee__hn1__email=self.request.user.email)
