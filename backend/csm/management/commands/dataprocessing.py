from django.core.management.base import BaseCommand
from csm.dataprocessing.utilities import processing_spreadsheet


class Command(BaseCommand):
    help = 'Export and Process spreadsheets'

    def handle(self, *args, **options):
        self.stdout.write(processing_spreadsheet())
