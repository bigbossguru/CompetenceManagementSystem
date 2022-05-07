FILES_NAME = {
    'master': 'master',
    'rd_competence': 'cda',
    'aa_competence': 'aa_competence',
    'aa_full': 'aa_full',
    'career': 'ca',
}


"""
Here we are defining columns name as in a spreadsheet table
"""
COLUMNS_NAME_MASTER = {
    # Original fields from spreadsheet Master Data after uniform process

    # Hyperion
    'hyperion': {
        'code': 'hyperion_kod',
        'name': 'hyperion',
        'function': 'hyperion_function',
    },

    # JobProfile
    'job_profile': {
        'code': 'job_code',
        'jobtitle': 'jobtitle',
        'metier_field': 'metier',
    },

    # Cost Centre
    'cc': {
        'code': 'cc',
        'code_': 'cc_2',
        'name': 'cc_name',
        'owner': 'ccowneremail',
    },

    # Employee
    'employee': {
        'ps_id': 'people_soft_id',
        'person_id': 'osobní_číslo_(čtyřmístné)',
        'fullname': 'příjmení,_jméno_(bez_diakritiky)',
        'email': 'email',
        'cadre': 'cadre',
        'full_part_time': 'doba_určitá/neurčitá',
        'fte': 'fte',
        'type_of_contract': 'druh_kontraktu_(hpp)',
        'location': 'lokace',
        'orgaloc': 'orgalog',
        'start_date': 'group_seniority_date',
        'hn1_id': 'n+1_id',
        'pl': 'pl_(oddělení)',
        'bg': 'bg_by_orgaloc',
    }
}

COLUMNS_NAME_RD = {
    # Original fields from spreadsheet CDA after uniform process

    'metier_field': {
        'metier_field_id': 'metier_field_id',
        'bg': 'metier_field_bg',
        'name': 'metier_field'
    },

    'platform': {
        'platform_id': 'platform_id',
        'name': 'platform'
    },

    'competence': {
        'competence_id': 'competence_id',
        'name': 'competencename',
        'type': 'competencetype',
        'metier_org': 'competence_metier_/_organization',
        'category': 'competence_category',
        'domain': 'competence_domain',
    },

    'level': {
        'employee': 'ps_code',
        'expected_lvl': 'expected_level',
        'manager_expected_lvl': 'manager_expected_level',
        'acquired_lvl': 'acquiredlevel',
        'gap': 'gap',
        'coverage': 'competence_coverage',
    }
}

COLUMNS_AA_COMP = {
    # Original fields from spreadsheet AA competence after uniform process

    'competence': {
        'code': 'competence_code',
        'name': 'competence_description',
    },

    'level': {
        'appraisal_id': 'appraisal_id',
        'year': 'year',
        'from_date': 'from_date',
        'to_date': 'to_date',
        'employee': 'ps_id',
        'interview_date': 'date_of_interview',
        'stage': 'stage',
        'status': 'status',
        'rating': 'rating',
        'expected_lvl': 'expected_level',
    }
}

COLUMNS_AA_FULL = {
    # Original fields from spreadsheet AA Full report after uniform process

    'aa_full': {
        'appraisal_id': 'appraisal_id',
        'from_date': 'from_date',
        'to_date': 'to_date',
        'employee': 'employee_id',
        'interview_date': 'date_of_interview',
        'stage': 'stage',
        'status': 'status',
        'date_completed_on': 'completed_on',
        'next_date_career_discus': 'date_of_next_detailed_career_discussion',
        'performance': 'performance',
        'trend': 'trend',
        'category': 'category',
        'level': 'level',
        'key_specific_obj': 'key_specific_objectives',
        'general_mission': 'general_mission',
        'demonstrated_behavior': 'demonstrated_behavior',
        'leadership': 'leadership',
    },
    'comments': ['employees_self_assessment', 'engagement_survey_key_objectives_description',
                 'competences_and_personal_characteristics_(most_help)',
                 'competences_and_personal_characteristics_(acquired_or_improved)',
                 'well_being_at_work', 'performance_comments', 'general_comments_(n+1)',
                 'general_comments_(employee)', 'general_comments_(n+2)']
}


COLUMNS_NAME_CA = {
    # Original fields from spreadsheet CA after uniform process

    'ca': {
        'from_date': 'from_date',
        'to_date': 'to_date',
        'employee': 'ps_id',
        'current_stage': 'current_stage',
        'stay_current_position': 'stay_in_current_position',
        'expertise': 'expertise',
        'eligibility': 'eligibility',
        'current_salary': 'current_salary',
        'new_salary': 'new_salary_proposed',
        'increase_proposal': 'new_increase_proposal',
        'budget': 'budget(%)',
        'risk_resignation': 'risk_resignation',
        'successor1': 'successor_1_ps_id',
        'successor2': 'successor_2_ps_id',
        'successor3': 'successor_3_ps_id',
    }
}


def to_list(data: dict) -> list:
    """
    This function convert nested dict all values to one list
    all fields which need for pandas dataframe
    """
    result = []

    for sub in data.values():
        if isinstance(sub, dict):
            result += sub.values()
        elif isinstance(sub, list):
            result += sub
        else:
            result.append(sub)
    return result
