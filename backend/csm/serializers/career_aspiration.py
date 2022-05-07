from rest_framework.serializers import ModelSerializer, StringRelatedField
from csm.models.career_aspiration import CareerAspiration


class EmployeeCareerAspirationListSerializer(ModelSerializer):
    employee = StringRelatedField()

    class Meta:
        model = CareerAspiration
        read_only = True
        fields = '__all__'
