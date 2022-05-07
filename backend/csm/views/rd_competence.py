from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, generics, views

from csm.filters import EmployeeRDCompetenceFilter
from csm.models.rd_competence import RDCompetence, EmployeeRDCompetence, MetierField, Platform
from csm.serializers.rd_competence import (
    RDCompetenceSerializer,
    EmployeeRDCompetenceListDetailSerializer,
    MetierFieldsSerializer,
    PlatformSerializer,
    WeightRDCompetenceSerializer
)


class RDCompetenceListView(generics.ListAPIView):
    """
    Detail overview of whole RD competences
    """
    queryset = RDCompetence.objects.all()
    serializer_class = RDCompetenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['name', 'type', 'metier_org', 'category', 'domain']
    search_fields = ['$name', '$type', '$metier_org', '$category', '$domain']


class EmployeeRDCompetenceListDetailView(generics.ListAPIView):
    """
    Detail overview of assignment RD competencies to Employees
    """
    serializer_class = EmployeeRDCompetenceListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmployeeRDCompetenceFilter

    def get_queryset(self):
        if self.request.user.is_local_hr:
            return EmployeeRDCompetence.objects.all()
        if self.request.user.is_manager:
            employees_under_manager = EmployeeRDCompetence.objects.filter(Q(employee__email=self.request.user.email))
            employees_under_manager |= EmployeeRDCompetence.objects.filter(Q(employee__hn1__email=self.request.user.email))
            return employees_under_manager
        if self.request.user.is_regular_employee:
            return EmployeeRDCompetence.objects.filter(employee__hn1__email=self.request.user.email)


class MetierFieldListView(generics.ListAPIView):
    serializer_class = MetierFieldsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MetierField.objects.all()


class PlatformListView(generics.ListAPIView):
    serializer_class = PlatformSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Platform.objects.all()


class WeightRDCompetenceUpdateView(generics.GenericAPIView):
    serializer_class = WeightRDCompetenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RDCompetence.objects.all()

    def get(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return views.Response(serializer.data)

    def get_object(self, pk):
        return RDCompetence.objects.get(competence_id=pk)

    def put(self, request):
        data = request.data
        try:
            if isinstance(data, list):
                for element in data:
                    obj = self.get_object(element.get('competence_id'))
                    obj.weight = element.get('weight')
                    obj.save()
            elif data:
                obj = self.get_object(element.get('competence_id'))
                obj.weight = element.get('weight')
                obj.save()
            else:
                return views.Response(status=views.status.HTTP_400_BAD_REQUEST)
        except RDCompetence.DoesNotExist:
            return views.Response(status=views.status.HTTP_404_NOT_FOUND)
        return views.Response(data)
