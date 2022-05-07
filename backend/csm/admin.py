from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from csm.models.user import User, UserAccessReport
from csm.models.employee import Employee
from csm.models.job_profile import JobProfile
from csm.models.cost_center import CostCenter
from csm.models.hyperion import Hyperion
from csm.models.career_aspiration import CareerAspiration
from csm.models.aa_competence import (
    AACompetence,
    EmployeeAACompetence,
    FullAACompetence
)
from csm.models.rd_competence import (
    EmployeeRDCompetence,
    RDCompetence,
    Platform,
    MetierField
)
from csm.models.system_config import (
    SystemConfiguration,
    FilesDetail,
    ServiceEmail
)

admin.site.site_header = "Competence Managment System"
admin.site.site_title = "CSM Admin System"
admin.site.index_title = "Welcome to CSM System"


class UserAdmin(UserAdmin):
    model = User
    list_display = (
        'email', 'is_regular_employee',
        'is_manager', 'is_local_hr', 'is_regional_hr'
    )
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': (
                'is_regular_employee', 'is_manager', 'is_local_hr',
                'is_regional_hr', 'is_active', 'is_staff'
            )
            }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_manager',
                'is_regular_employee',  'is_local_hr', 'is_regional_hr'
            )
            }),
    )
    search_fields = ('email',)
    ordering = ('email',)


class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('ps_id', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
admin.site.register(UserAccessReport)
admin.site.register(JobProfile)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Hyperion)
admin.site.register(CostCenter)
admin.site.register(AACompetence)
admin.site.register(RDCompetence)
admin.site.register(EmployeeRDCompetence)
admin.site.register(MetierField)
admin.site.register(Platform)
admin.site.register(FullAACompetence)
admin.site.register(CareerAspiration)
admin.site.register(SystemConfiguration)
admin.site.register(EmployeeAACompetence)
admin.site.register(FilesDetail)
admin.site.register(ServiceEmail)
admin.site.unregister(Group)
