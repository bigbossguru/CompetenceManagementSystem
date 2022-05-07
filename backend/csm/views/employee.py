from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, generics

from csm.models.employee import Employee
from csm.serializers.employee import EmployeeListDetailSerializer


class EmployeeListDetailView(generics.ListAPIView):
    """
    Detail overview for each Employee
    """
    serializer_class = EmployeeListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        'ps_id', 'first_name', 'last_name', 'cadre', 'full_part_time', 'type_of_contract',
        'location', 'orgaloc', 'bg', 'pg', 'pl', 'tpl', 'hn1__ps_id', 'hn1__last_name',
        'hn1__first_name', 'hn2__ps_id', 'hn2__last_name', 'hn2__first_name',
        'fn1__ps_id', 'fn1__last_name', 'fn1__first_name', 'hyperion__code',
        'hyperion__name', 'hyperion__function', 'job__code', 'job__jobtitle', 'job__metier_field',
        'cc__code', 'cc__name', 'aa_employees__competence__name', 'aa_employees__competence__code',
        'rd_employees__competence__competence_id', 'rd_employees__competence__name',
        'rd_employees__competence__type', 'rd_employees__competence__metier_org',
        'rd_employees__competence__category', 'rd_employees__competence__domain',
        'rd_employees__platform__name', 'rd_employees__metier_field__name'
    ]

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return Employee.objects.all()
        if self.request.user.is_manager:
            employees_under_manager = Employee.objects.filter(Q(email=self.request.user.email))
            employees_under_manager |= Employee.objects.filter(Q(hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return Employee.objects.filter(email=self.request.user.email)
