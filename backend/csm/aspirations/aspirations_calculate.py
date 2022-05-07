from csm.models.employee import Employee
from csm.models.aa_competence import EmployeeAACompetence
from csm.models.rd_competence import EmployeeRDCompetence


def aspirations_calculate(request_data: dict = None):
    try:
        custom_weight_competences = request_data.get('competence_weight')
        select_employee_id = request_data['subject']['ps_id']
        select_employee = Employee.objects.get(ps_id=select_employee_id)
        all_competences_select_employee = get_dict_competences_of_employee(select_employee)

        list_of_replacement_employee = {'results': []}
        for employee in Employee.objects.all():
            employee_with_competences = potential_employee_with_competences(employee, list(all_competences_select_employee.values()))

            if not employee_with_competences:
                continue

            sum_weight_relative_diff = []
            if isinstance(custom_weight_competences, list):
                for potential_employee_competence in employee_with_competences:

                    for custom_weight_competence in custom_weight_competences:
                        if custom_weight_competence.get('competence_id') == str(potential_employee_competence.competence_id):
                            relative_diff, weight_relative_diff = custom_weight_calculating(
                                potential_employee_competence,
                                all_competences_select_employee.get(potential_employee_competence.competence_id),
                                custom_weight_competence.get('weight')
                            )
                            sum_weight_relative_diff.append(weight_relative_diff)
                    else:
                        relative_diff, weight_relative_diff = default_weight_calculating(
                            potential_employee_competence,
                            all_competences_select_employee.get(potential_employee_competence.competence_id)
                        )
                        sum_weight_relative_diff.append(weight_relative_diff)
            else:
                for potential_employee_competence in employee_with_competences:
                    relative_diff, weight_relative_diff = default_weight_calculating(
                        potential_employee_competence,
                        all_competences_select_employee.get(potential_employee_competence.competence_id)
                    )
                    sum_weight_relative_diff.append(weight_relative_diff)

            list_of_replacement_employee['results'].append({
                'ps_id': employee.ps_id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'approximity_points': sum(sum_weight_relative_diff)
            })

        list_of_replacement_employee['results'] = sorted(list_of_replacement_employee['results'],
                                                         key=lambda d: d['approximity_points'], reverse=True)
        return list_of_replacement_employee
    except Employee.DoesNotExist:
        return {"results": {"message": "not found"}}


def get_competences_of_employee(employee: Employee) -> list:
    list_of_all_competences = [competence for competence in EmployeeAACompetence.objects.filter(employee=employee)]
    list_of_all_competences.extend([competence for competence in EmployeeRDCompetence.objects.filter(employee=employee)])
    return list_of_all_competences


def get_dict_competences_of_employee(employee: Employee) -> dict:
    dict_of_all_competences = {
        competence.competence_id: competence
        for competence in EmployeeAACompetence.objects.filter(employee=employee)
    }
    dict_of_all_competences.update({
        competence.competence_id: competence
        for competence in EmployeeRDCompetence.objects.filter(employee=employee)
    })
    return dict_of_all_competences


def convert_word_levels_to_number(level: str) -> int:
    convert_level = 0

    if level.lower() == 'experienced':
        convert_level = 3
    elif level.lower == 'skilled':
        convert_level = 2
    elif level.lower() == 'learner':
        convert_level = 1
    else:
        convert_level = 0

    return convert_level


def get_only_competence_info(list_or_object):
    if isinstance(list_or_object, list):
        list_of_id_code_competence = []
        for instance in list_or_object:
            if isinstance(instance, EmployeeAACompetence):
                list_of_id_code_competence.append(instance.competence.code)
            elif isinstance(instance, EmployeeRDCompetence):
                list_of_id_code_competence.append(instance.competence.competence_id)
        return list_of_id_code_competence
    else:
        if isinstance(list_or_object, EmployeeAACompetence):
            return list_or_object.competence.code
        elif isinstance(list_or_object, EmployeeRDCompetence):
            return list_or_object.competence.competence_id


def potential_employee_with_competences(employee, select_employee_competences: list) -> list:
    potential_employee = []

    for competence in get_competences_of_employee(employee):
        if get_only_competence_info(competence) in get_only_competence_info(select_employee_competences):
            potential_employee.append(competence)

    if potential_employee:
        return potential_employee


def default_weight_calculating(potential_employee, select_employee_competence) -> tuple:
    relative_diff = 0
    weight_relative_diff = 0
    if isinstance(potential_employee, EmployeeRDCompetence) and isinstance(select_employee_competence, EmployeeRDCompetence):
        relative_diff = potential_employee.acquired_lvl - select_employee_competence.acquired_lvl
        weight_relative_diff = potential_employee.competence.weight * relative_diff
    elif isinstance(potential_employee, EmployeeAACompetence) and isinstance(select_employee_competence, EmployeeAACompetence):
        relative_diff = convert_word_levels_to_number(potential_employee.rating) - convert_word_levels_to_number(select_employee_competence.rating)
        weight_relative_diff = potential_employee.competence.weight * relative_diff
    return relative_diff, weight_relative_diff


def custom_weight_calculating(potential_employee, select_employee_competence, weight) -> tuple:
    relative_diff = 0
    weight_relative_diff = 0
    if isinstance(potential_employee, EmployeeRDCompetence) and isinstance(select_employee_competence, EmployeeRDCompetence):
        relative_diff = potential_employee.acquired_lvl - select_employee_competence.acquired_lvl
        weight_relative_diff = weight * relative_diff
    elif isinstance(potential_employee, EmployeeAACompetence) and isinstance(select_employee_competence, EmployeeAACompetence):
        relative_diff = convert_word_levels_to_number(potential_employee.rating) - convert_word_levels_to_number(select_employee_competence.rating)
        weight_relative_diff = weight * relative_diff
    return relative_diff, weight_relative_diff
