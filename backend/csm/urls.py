from django.urls import path
from dj_rest_auth import views

from csm.views import history
from csm.views.career_aspiration import EmployeeCareerAspirationListView
from csm.views.employee import EmployeeListDetailView
from csm.views.rd_competence import (
    RDCompetenceListView,
    EmployeeRDCompetenceListDetailView,
    MetierFieldListView,
    PlatformListView,
    WeightRDCompetenceUpdateView
)
from csm.views.aa_competence import (
    AACompetenceListView,
    EmployeeAACompetenceListDetailView,
    EmployeeAAFullListView,
    WeightAACompetenceUpdateView
)
from csm.views.system_config import (
    SystemConfigView,
    FilesDetailViewSet,
    ServiceEmailsViewSet,
    UserAccessReportListView,
    FileUploadView,
    RunUpdateDatabaseFromExportView,
    StatusUpdateDatabaseFromExportView
)
from csm.views.aspirations import AspirationsDataCalculateView


urlpatterns = [
    # Endpoints for competence managment system
    path('employee/', EmployeeListDetailView.as_view(), name='employees_all'),
    path('rdcompetence/', RDCompetenceListView.as_view(), name='rdcompetence_list'),
    path('rdcompetence/weight/', WeightRDCompetenceUpdateView.as_view(), name='rdcompetence_weight_list'),
    path('rdcompetence/metierfield/', MetierFieldListView.as_view(), name='metierfield_list'),
    path('rdcompetence/platform/', PlatformListView.as_view(), name='platform_list'),
    path('aacompetence/', AACompetenceListView.as_view(), name='aacompetence_list'),
    path('aacompetence/weight/', WeightAACompetenceUpdateView.as_view(), name='aacompetence_weight_list'),
    path('employee/rdcompetence/', EmployeeRDCompetenceListDetailView.as_view(), name='rdcompetences_employees'),
    path('employee/aacompetence/', EmployeeAACompetenceListDetailView.as_view(), name='aacompetences_employees'),
    path('employee/fullaacompetence/', EmployeeAAFullListView.as_view(), name='fullaacompetences_employees'),
    path('employee/careeraspiration/', EmployeeCareerAspirationListView.as_view(), name='careeraspirations_employees'),
    path('aspirations/', AspirationsDataCalculateView.as_view(), name='aspirations'),

    # History data
    path('history/employee/', history.employee.HistoryEmployeeListView.as_view(), name='history_employee_all'),
    path('history/employee/careeraspiration/', history.career_aspiration.HistoryEmployeeCareerAspirationListView.as_view(),
         name='history_careeraspiration'),
    path('history/employee/aacompetence/', history.aa_competence.HistoryEmployeeAACompetenceListDetailView.as_view(),
         name='history_aacompetence'),
    path('history/employee/rdcompetence/', history.rd_competence.HistoryEmployeeRDCompetenceListDetailView.as_view(),
         name='history_rdcompetence'),

    # Authentication and reset (change) password by email
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('auth/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Endpoints for data processing
    path('system/config/', SystemConfigView.as_view()),
    path('system/config/files/', FilesDetailViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('system/config/files/<int:pk>/', FilesDetailViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}), name='file_detail'
    ),
    path('system/config/emails/', ServiceEmailsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('system/config/emails/<int:pk>/', ServiceEmailsViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}), name='email_detail'
    ),
    path('system/user/accessreport', UserAccessReportListView.as_view(), name='user_access_report'),

    path('upload/', FileUploadView.as_view(), name='upload'),
    path('update/', RunUpdateDatabaseFromExportView.as_view(), name='run_update'),
    path('update/status/', StatusUpdateDatabaseFromExportView.as_view(), name='run_update_status'),
]
