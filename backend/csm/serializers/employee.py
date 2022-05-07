from rest_framework.serializers import ModelSerializer, StringRelatedField
from csm.models.employee import Employee
from csm.models.hyperion import Hyperion
from csm.models.job_profile import JobProfile
from csm.models.cost_center import CostCenter


class HyperionSerializer(ModelSerializer):
    class Meta:
        model = Hyperion
        read_only = True
        fields = '__all__'


class JobProfileSerializer(ModelSerializer):
    class Meta:
        model = JobProfile
        read_only = True
        fields = '__all__'


class CostCenterSerializer(ModelSerializer):
    class Meta:
        model = CostCenter
        read_only = True
        fields = '__all__'


class EmployeeListDetailSerializer(ModelSerializer):
    job = JobProfileSerializer()
    hyperion = HyperionSerializer()
    hn1 = StringRelatedField()
    hn2 = StringRelatedField()
    fn1 = StringRelatedField()
    cc = CostCenterSerializer()
    # tpl_owner = StringRelatedField()

    class Meta:
        model = Employee
        read_only = True
        fields = [
            'ps_id', 'person_id', 'first_name', 'last_name', 'email',
            'cadre', 'full_part_time', 'fte', 'type_of_contract', 'location',
            'orgaloc', 'start_date', 'bg', 'pg', 'pl', 'tpl', 'hn1', 'hn2',
            'fn1', 'hyperion', 'job', 'cc', 'status'
        ]


class HistoryEmployeeListDetailSerializer(ModelSerializer):
    class Meta:
        model = Employee
        read_only = True
        fields = [
            'ps_id', 'person_id', 'first_name', 'last_name', 'email',
            'cadre', 'full_part_time', 'fte', 'type_of_contract', 'location',
            'orgaloc', 'start_date', 'bg', 'pg', 'pl', 'tpl', 'hn1', 'hn2',
            'fn1', 'hyperion', 'job', 'cc', 'status'
        ]
