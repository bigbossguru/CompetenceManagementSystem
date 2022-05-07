import os
from django.conf import settings
from rest_framework import permissions, generics, viewsets
from rest_framework.views import Response, status, APIView
from csm.dataprocessing.lib.config import logger_read
from csm.dataprocessing.utilities import LOGGER_FILE, processing_spreadsheet

from csm.models.user import UserAccessReport
from csm.models.system_config import SystemConfiguration, FilesDetail, ServiceEmail
from csm.serializers.system_config import (
    SystemConfigurationSerializer,
    FilesDetailSerializer,
    ServiceEmailSerializer,
    UserAccessReportSerializer,
    FileUploadSerializer
)


class SystemConfigView(generics.RetrieveUpdateAPIView):
    """
    Main system configuration view
    """
    serializer_class = SystemConfigurationSerializer

    def get_object(self):
        return SystemConfiguration.objects.get(id=SystemConfiguration.singleton_instance_id)


class FilesDetailViewSet(viewsets.ModelViewSet):
    """
    List of export files description
    """
    queryset = FilesDetail.objects.all()
    serializer_class = FilesDetailSerializer

    def create(self, request, *args, **kwargs):
        if not settings.MEDIA_ROOT.exists():
            os.mkdir(settings.MEDIA_ROOT)
        if not settings.TEMPFILES_ROOT.exists():
            os.mkdir(settings.TEMPFILES_ROOT)
        file_upload = request.FILES.get('file_upload')

        file_to_bytes = file_upload.read()
        file_path = os.path.join(settings.MEDIA_ROOT, file_upload.name)

        with open(file_path, "wb") as binary_file:
            binary_file.write(file_to_bytes)

        serializer = FilesDetailSerializer(data=request.data)
        if serializer.is_valid():
            config = SystemConfiguration.objects.get(id=SystemConfiguration.singleton_instance_id)
            file = FilesDetail.objects.create(**serializer.data)
            config.files_detail.add(file)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ServiceEmailsViewSet(viewsets.ModelViewSet):
    """
    List of service email, send warning etc
    """
    queryset = ServiceEmail.objects.all()
    serializer_class = ServiceEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = ServiceEmailSerializer(data=request.data)
        if serializer.is_valid():
            config = SystemConfiguration.objects.get(id=SystemConfiguration.singleton_instance_id)
            file = ServiceEmail.objects.create(**serializer.data)
            config.service_emails.add(file)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAccessReportListView(generics.ListAPIView):
    """Short Review, List of User Access Report"""
    queryset = UserAccessReport.objects.all()
    serializer_class = UserAccessReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class FileUploadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileUploadSerializer

    def post(self, request):
        if not settings.MEDIA_ROOT.exists():
            os.mkdir(settings.MEDIA_ROOT)
        if not settings.TEMPFILES_ROOT.exists():
            os.mkdir(settings.TEMPFILES_ROOT)
        files_upload = request.FILES.getlist('files_upload')

        if 'files_upload' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for file in files_upload:
            file_to_bytes = file.read()
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)

            with open(file_path, "wb") as binary_file:
                binary_file.write(file_to_bytes)

        return Response({'file_upload': file.name}, status=status.HTTP_201_CREATED)


class RunUpdateDatabaseFromExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            'info': "This is endpoint serves for launch data processing and update database from export files",
            "command": "For activate this script send command:run"
        }
        if logger_read(LOGGER_FILE)['status'] == "IN PROGRESS":
            data = logger_read(LOGGER_FILE)
        return Response(data)

    def post(self, request):
        if (request.data.get("command") == "run") and (logger_read(LOGGER_FILE)['status'] != "IN PROGRESS"):
            processing_spreadsheet.delay()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StatusUpdateDatabaseFromExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(data=logger_read(LOGGER_FILE), status=status.HTTP_200_OK)
