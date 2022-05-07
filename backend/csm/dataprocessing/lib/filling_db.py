from pathlib import Path
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .settings import (
    FILES_NAME, COLUMNS_NAME_MASTER, COLUMNS_NAME_RD,
    COLUMNS_AA_COMP, COLUMNS_AA_FULL, COLUMNS_NAME_CA, to_list
)
import pandas as pd
from .manipulation import extract_data, comments_to_multiline_string
from csm.models.employee import Employee
from csm.models.job_profile import JobProfile
from csm.models.cost_center import CostCenter
from csm.models.hyperion import Hyperion
from csm.models.aa_competence import (
    AACompetence, FullAACompetence, EmployeeAACompetence
)
from csm.models.career_aspiration import CareerAspiration
from csm.models.rd_competence import (
    RDCompetence, MetierField, Platform, EmployeeRDCompetence
)

BLANK_EMPTY_LIST = ('nan', '-', 'not-found')


def master_data_to_db(path: Path) -> None:
    database_with_hyperion(path)
    database_with_cc(path)
    fields = to_list(COLUMNS_NAME_MASTER)

    for _, row in extract_data(path, fields, FILES_NAME['master']).iterrows():
        try:
            last, first = str(row[COLUMNS_NAME_MASTER['employee']['fullname']]).split(',')
        except ValueError:
            last, first = str(row[COLUMNS_NAME_MASTER['employee']['fullname']]).rsplit(' ', 1)

        hyperion = Hyperion.objects.get(code=row[COLUMNS_NAME_MASTER['hyperion']['code']])
        cc = CostCenter.objects.get(code=row[COLUMNS_NAME_MASTER['cc']['code']])
        job_profile, _ = JobProfile.objects.update_or_create(
            code=row[COLUMNS_NAME_MASTER['job_profile']['code']],
            jobtitle=row[COLUMNS_NAME_MASTER['job_profile']['jobtitle']],
            metier_field=row[COLUMNS_NAME_MASTER['job_profile']['metier_field']]
        )

        _start_date = row[COLUMNS_NAME_MASTER['employee']['start_date']]

        employee, _ = Employee.objects.get_or_create(ps_id=row[COLUMNS_NAME_MASTER['employee']['ps_id']])
        employee.person_id = row[COLUMNS_NAME_MASTER['employee']['person_id']]
        employee.first_name = first
        employee.last_name = last
        employee.email = row[COLUMNS_NAME_MASTER['employee']['email']]
        employee.hyperion = hyperion
        employee.cadre = row[COLUMNS_NAME_MASTER['employee']['cadre']]
        employee.full_part_time = row[COLUMNS_NAME_MASTER['employee']['full_part_time']]
        employee.fte = row[COLUMNS_NAME_MASTER['employee']['fte']]
        employee.type_of_contract = row[COLUMNS_NAME_MASTER['employee']['type_of_contract']]
        employee.location = row[COLUMNS_NAME_MASTER['employee']['location']]
        employee.orgaloc = row[COLUMNS_NAME_MASTER['employee']['orgaloc']]
        employee.start_date = _start_date if _start_date is not pd.NaT else None
        employee.cc = cc
        employee.job = job_profile
        employee.pl = row[COLUMNS_NAME_MASTER['employee']['pl']]
        employee.bg = row[COLUMNS_NAME_MASTER['employee']['bg']]
        employee.save()

    # Filled hierarchical superior n+1
    for _, row in extract_data(path, fields, FILES_NAME['master']).iterrows():
        try:
            hn1 = Employee.objects.get(ps_id=row[COLUMNS_NAME_MASTER['employee']['hn1_id']])
            Employee.objects.filter(ps_id=row[COLUMNS_NAME_MASTER['employee']['ps_id']]).update(hn1=hn1)
        except ObjectDoesNotExist:
            continue

    # Filled hierarchical superior n+2
    for _, row in extract_data(path, fields, FILES_NAME['master']).iterrows():
        try:
            empl = Employee.objects.get(ps_id=row[COLUMNS_NAME_MASTER['employee']['ps_id']])
            if empl.hn1 is not None:
                hn1 = Employee.objects.get(ps_id=empl.hn1.ps_id)
                Employee.objects.filter(ps_id=row[COLUMNS_NAME_MASTER['employee']['ps_id']]).update(hn2=hn1.hn1)
        except ObjectDoesNotExist:
            continue

    # Filled cost centre owner
    for _, row in extract_data(path, fields, FILES_NAME['master']).iterrows():
        try:
            owner = Employee.objects.get(email=row[COLUMNS_NAME_MASTER['cc']['owner']])
            CostCenter.objects.filter(code=row[COLUMNS_NAME_MASTER['cc']['code']]).update(owner=owner)
        except ObjectDoesNotExist:
            continue

    # Create users for employees
    create_user_by_employee()

    # For each employee who is manager
    set_manager_permission()


def rd_competence_to_db(path: Path) -> None:
    database_with_rdcompetence(path)
    database_with_metier_field(path)
    database_with_platform(path)

    fields = to_list(COLUMNS_NAME_RD)

    for _, row in extract_data(path, fields, FILES_NAME['rd_competence']).iterrows():
        try:
            metier_field = MetierField.objects.get(metier_field_id=row[COLUMNS_NAME_RD['metier_field']['metier_field_id']])
            platform = Platform.objects.get(platform_id=row[COLUMNS_NAME_RD['platform']['platform_id']])
            rd_competence = RDCompetence.objects.get(competence_id=row[COLUMNS_NAME_RD['competence']['competence_id']])
            employee = Employee.objects.get(ps_id=row[COLUMNS_NAME_RD['level']['employee']])
            employee_competence, _ = EmployeeRDCompetence.objects.get_or_create(
                employee=employee,
                competence=rd_competence
            )
            employee_competence.platform = platform
            employee_competence.metier_field = metier_field
            employee_competence.expected_lvl = row[COLUMNS_NAME_RD['level']['expected_lvl']]
            employee_competence.manager_expected_lvl = row[COLUMNS_NAME_RD['level']['manager_expected_lvl']]
            employee_competence.acquired_lvl = row[COLUMNS_NAME_RD['level']['acquired_lvl']]
            employee_competence.gap = row[COLUMNS_NAME_RD['level']['gap']]
            employee_competence.coverage = row[COLUMNS_NAME_RD['level']['coverage']]
            employee_competence.save()
        except ObjectDoesNotExist:
            continue


def aa_competence_to_db(path: Path) -> None:
    database_with_aacompetence(path)
    fields = to_list(COLUMNS_AA_COMP)

    for _, row in extract_data(path, fields, FILES_NAME['aa_competence']).iterrows():
        try:
            # Checkout date is correct
            _from_date = row[COLUMNS_AA_COMP['level']['from_date']]
            _to_date = row[COLUMNS_AA_COMP['level']['to_date']]
            _interview_date = row[COLUMNS_AA_COMP['level']['interview_date']]

            competence = AACompetence.objects.get(name=row[COLUMNS_AA_COMP['competence']['name']])
            employee = Employee.objects.get(ps_id=row[COLUMNS_AA_COMP['level']['employee']])
            employee_competence, _ = EmployeeAACompetence.objects.get_or_create(
                employee=employee,
                competence=competence
            )
            employee_competence.appraisal_id = row[COLUMNS_AA_COMP['level']['appraisal_id']]
            employee_competence.year = row[COLUMNS_AA_COMP['level']['year']]
            employee_competence.from_date = _from_date if _from_date is not pd.NaT else None
            employee_competence.to_date = _to_date if _to_date is not pd.NaT else None
            employee_competence.interview_date = _interview_date if _interview_date is not pd.NaT else None
            employee_competence.stage = row[COLUMNS_AA_COMP['level']['stage']]
            employee_competence.status = row[COLUMNS_AA_COMP['level']['status']]
            employee_competence.rating = row[COLUMNS_AA_COMP['level']['rating']]
            employee_competence.expected_lvl = row[COLUMNS_AA_COMP['level']['expected_lvl']]
            employee_competence.save()
        except ObjectDoesNotExist:
            continue


def full_aa_report_to_db(path: Path) -> None:
    fields = to_list(COLUMNS_AA_FULL)

    for _, row in extract_data(path, fields, FILES_NAME['aa_full']).iterrows():
        try:
            _from_date = row[COLUMNS_AA_FULL['aa_full']['from_date']]
            _to_date = row[COLUMNS_AA_FULL['aa_full']['to_date']]
            _interview_date = row[COLUMNS_AA_FULL['aa_full']['interview_date']]
            _date_completed_on = row[COLUMNS_AA_FULL['aa_full']['date_completed_on']]
            _next_date_career_discus = row[COLUMNS_AA_FULL['aa_full']['next_date_career_discus']]

            comment = comments_to_multiline_string(COLUMNS_AA_FULL['comments'], row)
            employee = Employee.objects.get(ps_id=row[COLUMNS_AA_FULL['aa_full']['employee']])
            fullaacompet, _ = FullAACompetence.objects.get_or_create(employee=employee)
            fullaacompet.appraisal_id = row[COLUMNS_AA_FULL['aa_full']['appraisal_id']]
            fullaacompet.from_date = _from_date if _from_date is not pd.NaT else None
            fullaacompet.to_date = _to_date if _to_date is not pd.NaT else None
            fullaacompet.interview_date = _interview_date if _interview_date is not pd.NaT else None
            fullaacompet.stage = row[COLUMNS_AA_FULL['aa_full']['stage']]
            fullaacompet.status = row[COLUMNS_AA_FULL['aa_full']['status']]
            fullaacompet.date_completed_on = _date_completed_on if _date_completed_on is not pd.NaT else None
            fullaacompet.next_date_career_discus = _next_date_career_discus if _next_date_career_discus is not pd.NaT else None
            fullaacompet.performance = row[COLUMNS_AA_FULL['aa_full']['performance']]
            fullaacompet.trend = row[COLUMNS_AA_FULL['aa_full']['trend']]
            fullaacompet.category = row[COLUMNS_AA_FULL['aa_full']['category']]
            fullaacompet.level = row[COLUMNS_AA_FULL['aa_full']['level']]
            fullaacompet.key_specific_obj = row[COLUMNS_AA_FULL['aa_full']['key_specific_obj']]
            fullaacompet.general_mission = row[COLUMNS_AA_FULL['aa_full']['general_mission']]
            fullaacompet.demonstrated_behavior = row[COLUMNS_AA_FULL['aa_full']['demonstrated_behavior']]
            fullaacompet.leadership = row[COLUMNS_AA_FULL['aa_full']['leadership']]
            fullaacompet.comments = comment
            fullaacompet.save()
        except ObjectDoesNotExist:
            continue


def career_aspiration_to_db(path: Path) -> None:
    fields = to_list(COLUMNS_NAME_CA)

    for _, row in extract_data(path, fields, FILES_NAME['career']).iterrows():
        try:
            _from_date = row[COLUMNS_NAME_CA['ca']['from_date']]
            _to_date = row[COLUMNS_NAME_CA['ca']['to_date']]

            employee = Employee.objects.get(ps_id=row[COLUMNS_NAME_CA['ca']['employee']])
            successor1 = Employee.objects.get(ps_id=row[COLUMNS_NAME_CA['ca']['successor1']])
            successor2 = Employee.objects.get(ps_id=row[COLUMNS_NAME_CA['ca']['successor2']])
            successor3 = Employee.objects.get(ps_id=row[COLUMNS_NAME_CA['ca']['successor3']])
            career_aspirat, _ = CareerAspiration.objects.get_or_create(employee=employee)
            career_aspirat.from_date = _from_date if _from_date is not pd.NaT else None
            career_aspirat.to_date = _to_date if _to_date is not pd.NaT else None
            career_aspirat.current_stage = row[COLUMNS_NAME_CA['ca']['current_stage']]
            career_aspirat.stay_current_position = row[COLUMNS_NAME_CA['ca']['stay_current_position']]
            career_aspirat.expertise = row[COLUMNS_NAME_CA['ca']['expertise']]
            career_aspirat.eligibility = row[COLUMNS_NAME_CA['ca']['eligibility']]
            career_aspirat.current_salary = row[COLUMNS_NAME_CA['ca']['current_salary']]
            career_aspirat.new_salary = row[COLUMNS_NAME_CA['ca']['new_salary']]
            career_aspirat.increase_proposal = row[COLUMNS_NAME_CA['ca']['increase_proposal']]
            career_aspirat.budget = row[COLUMNS_NAME_CA['ca']['budget']]
            career_aspirat.risk_resignation = row[COLUMNS_NAME_CA['ca']['risk_resignation']]
            career_aspirat.successor1 = successor1
            career_aspirat.successor2 = successor2
            career_aspirat.successor3 = successor3
            career_aspirat.save()
        except ObjectDoesNotExist:
            continue


def create_user_by_employee(key: str = 'HR'):
    for instance in Employee.objects.all():
        try:
            if key in instance.job.jobtitle:
                user = get_user_model().objects.create_user(
                    email=instance.email, password='',
                    username=str(instance.email).split('@')[0],
                    is_local_hr=True)
            else:
                user = get_user_model().objects.create_user(
                    email=instance.email, password='',
                    username=str(instance.email).split('@')[0])

            password = get_user_model().objects.make_random_password()
            user.set_password(password)
            user.save()
        except IntegrityError:
            continue


def set_manager_permission():
    list_of_managers = [obj.hn1 for obj in Employee.objects.all() if obj.hn1 is not None]
    list_of_managers = set(list_of_managers)
    users = get_user_model()
    for manager in list_of_managers:
        m = users.objects.get(email=manager.email)
        m.is_manager = True
        m.save()


def database_with_rdcompetence(path):
    fields = to_list(COLUMNS_NAME_RD)

    for _, row in extract_data(path, fields, FILES_NAME['rd_competence']).iterrows():
        rd_competence, _ = RDCompetence.objects.get_or_create(
            competence_id=row[COLUMNS_NAME_RD['competence']['competence_id']]
        )
        rd_competence.name = row[COLUMNS_NAME_RD['competence']['name']]
        rd_competence.type = row[COLUMNS_NAME_RD['competence']['type']]
        rd_competence.metier_org = row[COLUMNS_NAME_RD['competence']['metier_org']]
        rd_competence.category = row[COLUMNS_NAME_RD['competence']['category']]
        rd_competence.domain = row[COLUMNS_NAME_RD['competence']['domain']]
        rd_competence.save()


def database_with_metier_field(path):
    fields = to_list(COLUMNS_NAME_RD)

    for _, row in extract_data(path, fields, FILES_NAME['rd_competence']).iterrows():
        metierfield, _ = MetierField.objects.get_or_create(
            metier_field_id=row[COLUMNS_NAME_RD['metier_field']['metier_field_id']]
        )
        metierfield.bg = row[COLUMNS_NAME_RD['metier_field']['bg']]
        metierfield.name = row[COLUMNS_NAME_RD['metier_field']['name']]
        metierfield.save()


def database_with_platform(path):
    fields = to_list(COLUMNS_NAME_RD)

    for _, row in extract_data(path, fields, FILES_NAME['rd_competence']).iterrows():
        platform, _ = Platform.objects.get_or_create(platform_id=row[COLUMNS_NAME_RD['platform']['platform_id']])
        platform.name = row[COLUMNS_NAME_RD['platform']['name']]
        platform.save()


def database_with_hyperion(path):
    fields = to_list(COLUMNS_NAME_MASTER)

    for _, row in extract_data(path, fields, FILES_NAME['master']).iterrows():
        hyperion, _ = Hyperion.objects.get_or_create(code=row[COLUMNS_NAME_MASTER['hyperion']['code']])
        hyperion.name = row[COLUMNS_NAME_MASTER['hyperion']['name']]
        hyperion.function = row[COLUMNS_NAME_MASTER['hyperion']['function']]
        hyperion.save()


def database_with_cc(path):
    fields = to_list(COLUMNS_NAME_MASTER)

    for _, row in extract_data(path, fields, FILES_NAME['master']).iterrows():
        cc, _ = CostCenter.objects.get_or_create(code=row[COLUMNS_NAME_MASTER['cc']['code']])
        cc.name = row[COLUMNS_NAME_MASTER['cc']['name']]
        cc.save()


def database_with_aacompetence(path):
    fields = to_list(COLUMNS_AA_COMP)

    for _, row in extract_data(path, fields, FILES_NAME['aa_competence']).iterrows():
        AACompetence.objects.update_or_create(
            code=row[COLUMNS_AA_COMP['competence']['code']],
            name=row[COLUMNS_AA_COMP['competence']['name']]
        )
