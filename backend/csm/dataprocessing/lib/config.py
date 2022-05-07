import json
from pathlib import Path

CONFIG_FILE = Path().absolute() / 'config.json'


class Configuration:
    def __init__(self):
        if not CONFIG_FILE.exists():
            self._create()
        self._read()

    def _create(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as config_file:
            json.dump(CONFIG_SAMPLE, config_file, indent=4)

    def _read(self):
        with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
            data = json.load(config_file)
            return data

    def get_number_of_files(self) -> int:
        return self._read()["spreadsheet"]["count"]

    def get_list_of_filesname(self) -> list:
        return self._read()["spreadsheet"]["filename"]

    def get_start_header(self, name: str) -> int:
        for key, value in self._read()["spreadsheet"]["startheader"].items():
            if key in name.lower():
                return value

    def get_list_of_emails(self) -> list:
        return self._read()["email"]

    def get_remote_path(self) -> list:
        return self._read()['path']

    def get_time(self, start: bool = False, end: bool = False) -> list:
        if start:
            return self._read()['data_time']['start_month']['time'].split(':')
        if end:
            return self._read()['data_time']['end_month']['time'].split(':')
        return [8, 30]

    def get_day_of_month(self, start: bool = False, end: bool = False) -> str:
        if start and end:
            return f"{self._read()['data_time']['start_month']['day']},{self._read()['data_time']['end_month']['day']}"
        if start:
            return self._read()['data_time']['start_month']['day']
        if end:
            return self._read()['data_time']['end_month']['day']
        return "1"


CONFIG_SAMPLE = {
                    "spreadsheet": {
                        "count": 6,
                        "filename": ["ca", "aa_full", "master", "aa_competence", "ps", "cda"],
                        "startheader": {
                            "aa_competence": 1,
                            "aa_full": 2,
                            "ca": 1,
                            "master": 0,
                            "ps": 1,
                            "cda": 0
                        }
                    },
                    "email": ["admin@admin.com"],
                    "path": "",
                    "data_time": {
                        "start_month": {
                            "time": "8:30",
                            "day": "1-5"
                        },
                        "end_month": {
                            "time": "8:30",
                            "day": "15-17"
                        }
                    },
                }


def logger_read(path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data
