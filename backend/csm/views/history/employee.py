from django.db.models import Q
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics

from csm.models.employee import Employee
from csm.serializers.employee import HistoryEmployeeListDetailSerializer


class HistoryEmployeeFilter(FilterSet):
    create_date = CharFilter(lookup_expr='icontains')
    start_date = CharFilter(lookup_expr='icontains')
    ps_id = CharFilter(lookup_expr='icontains')
    # start_date = CharFilter(lookup_expr='icontains')


class HistoryEmployeeListView(generics.ListAPIView):
    """
    History overview of last changes Employees
    """

    serializer_class = HistoryEmployeeListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoryEmployeeFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return Employee.history.all()
        if self.request.user.is_manager:
            employees_under_manager = Employee.history.filter(Q(email=self.request.user.email))
            employees_under_manager |= Employee.history.filter(Q(hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return Employee.history.filter(email=self.request.user.email)
