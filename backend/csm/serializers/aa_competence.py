from rest_framework.serializers import ModelSerializer, StringRelatedField
from csm.models.aa_competence import (
    AACompetence,
    EmployeeAACompetence,
    FullAACompetence
)


class AACompetenceSerializer(ModelSerializer):
    """List of AA Competence Description"""

    class Meta:
        model = AACompetence
        read_only = True
        fields = '__all__'


class EmployeeAACompetenceListDetailSerializer(ModelSerializer):
    """Review for each Employee with AA Competence Level"""
    employee = StringRelatedField()
    competence = AACompetenceSerializer()

    class Meta:
        model = EmployeeAACompetence
        read_only = True
        fields = [
            'id', 'employee', 'competence', 'appraisal_id', 'year',
            'from_date', 'to_date', 'interview_date', 'stage', 'status',
            'rating', 'expected_lvl', 'create_date'
        ]


class EmployeeAAFullDetailSerializer(ModelSerializer):
    """Review, List of Employee with Full AA Report"""
    employee = StringRelatedField()

    class Meta:
        model = FullAACompetence
        read_only = True
        fields = '__all__'


class HistoryEmployeeAACompetenceListDetailSerializer(ModelSerializer):
    """Review for each Employee with AA Competence Level"""

    class Meta:
        model = EmployeeAACompetence
        read_only = True
        fields = [
            'id', 'employee', 'competence', 'appraisal_id', 'year',
            'from_date', 'to_date', 'interview_date', 'stage', 'status',
            'rating', 'expected_lvl', 'create_date'
        ]


class HistoryEmployeeAAFullDetailSerializer(ModelSerializer):
    """Review, List of Employee with Full AA Report"""

    class Meta:
        model = FullAACompetence
        read_only = True
        fields = '__all__'


class WeightAACompetenceSerializer(ModelSerializer):
    class Meta:
        model = AACompetence
        fields = ['code', 'weight']
