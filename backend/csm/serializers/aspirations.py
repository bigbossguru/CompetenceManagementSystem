from rest_framework.serializers import Serializer, Serializer, CharField, ListSerializer, IntegerField


class SubjectSerializer(Serializer):
    ps_id = IntegerField()


class BaseCompetenceWeightInfoSerializer(Serializer):
    competence_id = CharField()
    weight = IntegerField()


class AspirationsDataSerializer(Serializer):
    subject = SubjectSerializer()
    competence_weight = ListSerializer(child=BaseCompetenceWeightInfoSerializer(), required=False)
