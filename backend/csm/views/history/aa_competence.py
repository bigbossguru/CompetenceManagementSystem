from django.db.models import Q
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics

from csm.models.aa_competence import FullAACompetence, EmployeeAACompetence
from csm.serializers.aa_competence import (
    HistoryEmployeeAACompetenceListDetailSerializer,
    HistoryEmployeeAAFullDetailSerializer
)


class HistoryEmployeeAACompetenceFilter(FilterSet):
    interview_date = CharFilter(lookup_expr='icontains')
    history_date = CharFilter(lookup_expr='icontains')
    employee__first_name = CharFilter()
    employee__last_name = CharFilter()
    competence__id = CharFilter()
    competence__name = CharFilter()
    competence__code = CharFilter()
    employee__ps_id = CharFilter()
    year = CharFilter()


class HistoryEmployeeFullAACompetenceFilter(FilterSet):
    pass


class HistoryEmployeeAACompetenceListDetailView(generics.ListAPIView):
    """
    Detail overview of assignment AA competencies to Employees
    """
    serializer_class = HistoryEmployeeAACompetenceListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoryEmployeeAACompetenceFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return EmployeeAACompetence.history.all()
        if self.request.user.is_manager:
            employees_under_manager = EmployeeAACompetence.history.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= EmployeeAACompetence.history.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return EmployeeAACompetence.history.filter(employee__hn1__email=self.request.user.email)


class HistoryEmployeeAAFullListView(generics.ListAPIView):
    """
    Detail overview of AA Full Report for each Employees
    """
    serializer_class = HistoryEmployeeAAFullDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoryEmployeeFullAACompetenceFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return FullAACompetence.history.all()
        if self.request.user.is_manager:
            employees_under_manager = FullAACompetence.history.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= FullAACompetence.history.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return FullAACompetence.history.filter(employee__hn1__email=self.request.user.email)
