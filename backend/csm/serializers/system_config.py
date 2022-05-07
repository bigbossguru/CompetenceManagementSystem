from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    HyperlinkedIdentityField,
    EmailField,
    Serializer,
    FileField
)
from dj_rest_auth.serializers import LoginSerializer as RestLoginSerializer

from csm.models.user import UserAccessReport
from csm.models.system_config import (
    SystemConfiguration,
    ServiceEmail,
    FilesDetail
)


class UserAccessReportSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = UserAccessReport
        fields = '__all__'


class ServiceEmailSerializer(ModelSerializer):
    class Meta:
        model = ServiceEmail
        fields = '__all__'


class FilesDetailSerializer(ModelSerializer):
    class Meta:
        model = FilesDetail
        fields = '__all__'


class SystemConfigurationSerializer(ModelSerializer):
    service_emails = HyperlinkedIdentityField('email_detail', many=True)
    files_detail = HyperlinkedIdentityField('file_detail', many=True)

    class Meta:
        model = SystemConfiguration
        fields = ['start_update_datetime', 'end_update_datetime', 'files_detail', 'service_emails']


class FileUploadSerializer(Serializer):
    files_upload = FileField(allow_empty_file=False, use_url=True)

    class Meta:
        fields = '__all__'


class LoginSerializer(RestLoginSerializer):
    username = None
    email = EmailField(required=True, allow_blank=False)
