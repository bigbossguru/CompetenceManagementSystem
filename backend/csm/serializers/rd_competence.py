from rest_framework.serializers import ModelSerializer, StringRelatedField
from csm.models.rd_competence import (
    EmployeeRDCompetence,
    RDCompetence,
    Platform,
    MetierField
)


class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        read_only = True
        fields = '__all__'


class MetierFieldsSerializer(ModelSerializer):
    class Meta:
        model = MetierField
        read_only = True
        fields = '__all__'


class RDCompetenceSerializer(ModelSerializer):
    class Meta:
        model = RDCompetence
        read_only = True
        fields = '__all__'


class EmployeeRDCompetenceListDetailSerializer(ModelSerializer):
    employee = StringRelatedField()
    platform = PlatformSerializer()
    metier_field = MetierFieldsSerializer()
    competence = RDCompetenceSerializer()

    class Meta:
        model = EmployeeRDCompetence
        read_only = True
        fields = [
            'id', 'employee', 'platform', 'metier_field', 'competence',
            'expected_lvl', 'manager_expected_lvl', 'acquired_lvl',
            'gap', 'coverage', 'create_date'
        ]


class WeightRDCompetenceSerializer(ModelSerializer):
    class Meta:
        model = RDCompetence
        fields = ['competence_id', 'weight']
