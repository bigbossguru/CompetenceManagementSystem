from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics
from rest_framework.filters import SearchFilter

from csm.filters import CareerAspirationFilter
from csm.models.career_aspiration import CareerAspiration
from csm.serializers.career_aspiration import (
    EmployeeCareerAspirationListSerializer,
)


class EmployeeCareerAspirationListView(generics.ListAPIView):
    """
    Detail overview of assignment Career Aspiration for each Employees
    """
    serializer_class = EmployeeCareerAspirationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CareerAspirationFilter

    search_fields = ['$employee__first_name', '$employee__last_name']

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return CareerAspiration.objects.all()
        if self.request.user.is_manager:
            employees_under_manager = CareerAspiration.objects.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= CareerAspiration.objects.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return CareerAspiration.objects.filter(employee__hn1__email=self.request.user.email)
