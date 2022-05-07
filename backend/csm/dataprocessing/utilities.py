import os
import json
import datetime
from pathlib import Path
from dataclasses import dataclass
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from django.core.management import call_command
from celery import shared_task
from .lib.config import Configuration
from .lib.manipulation import (
    MissingOrDistortedColumnsInTable,
    MissingSpreadsheetsExport,
    uniform_format,
    check_complete_files,
    check_exist_dir
)
from .lib.filling_db import (
    master_data_to_db,
    rd_competence_to_db,
    aa_competence_to_db,
    full_aa_report_to_db,
    career_aspiration_to_db
)


# Working with config spreadsheet file
cfg = Configuration()
LOGGER_FILE = Path().absolute() / "logs/status.json"


@dataclass
class StateProcessing:
    """Save all states for during processing files"""
    file_name: str

    def save(self, data: dict):
        self.data = data
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def email(self):
        head = self.data.get('message').split(',')[0]
        send_mail(subject=f'[SERVER] {head}',
                  message=self.data.get('message'),
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[cfg.get_email()],
                  fail_silently=False)


# Recursively remove all files in tempfiles directory
def remove_tmpfiles() -> None:
    for file in os.listdir(settings.TEMPFILES_ROOT):
        os.remove(settings.TEMPFILES_ROOT.joinpath(file))


# Recursively remove all file in mediafiles direstory
def remove_mediafiles() -> None:
    for file in os.listdir(settings.MEDIA_ROOT):
        os.remove(settings.MEDIA_ROOT.joinpath(file))


# Processing spreadsheets: uniform format each spreadsheet, extract info from table, filling database
@shared_task
def processing_spreadsheet() -> str:
    try:
        state = StateProcessing(file_name=LOGGER_FILE)
        state.save(
            {
                'status': 'IN PROGRESS',
                'message': 'Processing spreadsheets...........................................',
                'created': str(datetime.datetime.now())
            }
        )

        if not check_exist_dir(settings.TEMPFILES_ROOT):
            os.mkdir(settings.TEMPFILES_ROOT)
        check_complete_files(settings.MEDIA_ROOT, cfg)
        uniform_format(settings.MEDIA_ROOT, cfg, settings.TEMPFILES_ROOT)

        # Filling database
        master_data_to_db(settings.TEMPFILES_ROOT)
        rd_competence_to_db(settings.TEMPFILES_ROOT)
        aa_competence_to_db(settings.TEMPFILES_ROOT)
        full_aa_report_to_db(settings.TEMPFILES_ROOT)
        career_aspiration_to_db(settings.TEMPFILES_ROOT)

        # Removes duplicate on history database
        # call_command('clean_duplicate_history', '--auto')

        # Recursively remove all files in tempfiles directory
        remove_tmpfiles()
        remove_mediafiles()
        state.save(
            {
                'status': 'OK',
                'message': 'Processing spreadsheets: extract data from table and filling database success',
                'created': str(datetime.datetime.now())
            }
        )
        return 'Processing spreadsheets: uniform format, extract from table and filling database success'
    except (MissingSpreadsheetsExport, MissingOrDistortedColumnsInTable) as e:
        remove_tmpfiles()
        state.save(
            {
                'status': 'BAD',
                'message': f'Missing files or invalid contents, error message: {e}',
                'created': str(datetime.datetime.now())
            }
        )
        # state.email()
        return f'Missing files or invalid contents, error message: {e}! Sending email to HR Valeo'

    except PermissionError as e:
        remove_tmpfiles()
        state.save(
            {
                'status': 'BAD',
                'message': f'Permission error, error message: {e}',
                'created': str(datetime.datetime.now())
            }
        )
        # state.email()
        return f'Permission error, error message: {e}'

    except (KeyError, AttributeError) as e:
        remove_tmpfiles()
        state.save(
            {
                'status': 'BAD',
                'message': f'Invalid data, error message: {e}',
                'created': str(datetime.datetime.now())
            }
        )
        # state.email()
        return f'Invalid data {e}! Sending email to HR Valeo'
