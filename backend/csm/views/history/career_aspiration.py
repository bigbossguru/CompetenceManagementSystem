from django.db.models import Q
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics

from csm.models.career_aspiration import CareerAspiration
from csm.serializers.career_aspiration import (
    EmployeeCareerAspirationListSerializer,
)


class HistoryCareerAspirationFilter(FilterSet):
    history_date = CharFilter(lookup_expr='icontains')
    employee__first_name = CharFilter()
    employee__last_name = CharFilter()
    employee__ps_id = CharFilter()


class HistoryEmployeeCareerAspirationListView(generics.ListAPIView):
    """
    History last of change detail overview of assignment Career Aspiration for each Employees
    """
    serializer_class = EmployeeCareerAspirationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoryCareerAspirationFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return CareerAspiration.history.all()
        if self.request.user.is_manager:
            employees_under_manager = CareerAspiration.history.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= CareerAspiration.history.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return CareerAspiration.history.filter(employee__hn1__email=self.request.user.email)
