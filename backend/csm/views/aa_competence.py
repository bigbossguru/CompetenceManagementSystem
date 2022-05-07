from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, generics, views

from csm.filters import EmployeeAACompetenceFilter, EmployeeFullAACompetenceFilter
from csm.models.aa_competence import AACompetence, FullAACompetence, EmployeeAACompetence
from csm.serializers.aa_competence import (
    AACompetenceSerializer,
    EmployeeAACompetenceListDetailSerializer,
    EmployeeAAFullDetailSerializer,
    WeightAACompetenceSerializer
)


class AACompetenceListView(generics.ListAPIView):
    """
    Detail overview of whole AA competences
    """
    queryset = AACompetence.objects.all()
    serializer_class = AACompetenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['name', 'code']


class EmployeeAACompetenceListDetailView(generics.ListAPIView):
    """
    Detail overview of assignment AA competencies to Employees
    """
    serializer_class = EmployeeAACompetenceListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeAACompetenceFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return EmployeeAACompetence.objects.all()
        if self.request.user.is_manager:
            employees_under_manager = EmployeeAACompetence.objects.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= EmployeeAACompetence.objects.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return EmployeeAACompetence.objects.filter(employee__hn1__email=self.request.user.email)


class EmployeeAAFullListView(generics.ListAPIView):
    """
    Detail overview of AA Full Report for each Employees
    """
    serializer_class = EmployeeAAFullDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeFullAACompetenceFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return FullAACompetence.objects.all()
        if self.request.user.is_manager:
            employees_under_manager = FullAACompetence.objects.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= FullAACompetence.objects.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return FullAACompetence.objects.filter(employee__hn1__email=self.request.user.email)


class WeightAACompetenceUpdateView(generics.GenericAPIView):
    serializer_class = WeightAACompetenceSerializer

    def get_queryset(self):
        return AACompetence.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return views.Response(serializer.data)

    def get_object(self, pk):
        return AACompetence.objects.get(code=pk)

    def put(self, request):
        data = request.data
        try:
            if isinstance(data, list):
                for element in data:
                    obj = self.get_object(element.get('code'))
                    obj.weight = element.get('weight')
                    obj.save()
            elif data:
                obj = self.get_object(element.get('code'))
                obj.weight = element.get('weight')
                obj.save()
            else:
                return views.Response(status=views.status.HTTP_400_BAD_REQUEST)
        except AACompetence.DoesNotExist:
            return views.Response(status=views.status.HTTP_404_NOT_FOUND)
        return views.Response(data)
