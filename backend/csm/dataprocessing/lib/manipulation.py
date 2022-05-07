import os
from typing import Iterable, List, Optional
from pathlib import Path
import pandas as pd
import numpy as np
from .config import Configuration


class MissingOrDistortedColumnsInTable(Exception):
    """
    Missing or distorted columns in the table
    """


class MissingSpreadsheetsExport(Exception):
    """Raised when missing spreadsheets export"""


def uniform_format(resources_path: Path, cfg: Configuration, tempfile_path: Path, extension: str = 'xlsx') -> bool:
    paths_of_files = list(resources_path.glob(f"*.{extension}"))
    for file_path in paths_of_files:
        skip_rows: int = cfg.get_start_header(file_path.name)
        df = pd.read_excel(file_path, skiprows=skip_rows)
        df.columns = [str(name).lower().strip().replace(' ', '_') for name in df.columns]
        file_name = file_path.name.replace(' ', '_')
        df.to_excel(tempfile_path.joinpath(f'uniform_{file_name}'), index=False)
    return True


def extract_data(path: Path, fields: List[str], key: str, nan_to_blank=False, extension: str = 'xlsx') -> pd.DataFrame:
    for file in path.glob(f'*.{extension}'):
        if key.lower() in file.name.lower():
            file_name = file.name
            df = pd.read_excel(file)
            if all(field in df.columns for field in fields):
                df = df[fields]
                if nan_to_blank:
                    for column in df.columns:
                        if 'date' in column:
                            df[column] = pd.to_datetime(df[column]).dt.date
                            df[column] = df[column].astype(object).where(df[column].notnull(), np.nan)
                    df.fillna('', inplace=True)
                for column in df.columns:
                    if 'date' in column:
                        df[column] = pd.to_datetime(df[column]).dt.date
                return df
            else:
                raise MissingOrDistortedColumnsInTable(f'File: {file_name}, Missing these columns: {fields}')


def separate_column(df: pd.DataFrame, orig_name: str, new_names: list, **kwargs) -> pd.DataFrame:
    df_columns = df.columns

    if orig_name in df_columns:
        df_extract = pd.DataFrame(df[orig_name].str.split(' ', 1).tolist(), columns=new_names)

        if kwargs.get('inplace', False):
            df = pd.concat([df_extract, df], axis=1)
        else:
            return pd.concat([df_extract, df], axis=1)


def save_to_file(dfs: list[pd.DataFrame]) -> None:
    for idx, df in enumerate(dfs):
        df.to_excel(f"file_{idx}.xlsx", index=False)


def check_complete_files(path: Path, cfg: Configuration, file_extension: str = 'xlsx') -> MissingSpreadsheetsExport:
    paths_of_files = list(path.glob(f"*.{file_extension}"))
    if paths_of_files:
        control_flags = {}
        for file_expected in cfg.get_list_of_filesname():
            for file_actually in paths_of_files:
                if file_expected.lower() in file_actually.name.lower():
                    control_flags[file_expected] = True
                    break
                control_flags[file_expected] = False

        if not all(control_flags.values()):
            error_string = ' '.join([name for name, val in control_flags.items() if not val])
            raise MissingSpreadsheetsExport(f'export files missing ({error_string})')
    else:
        raise MissingSpreadsheetsExport('empty directory')


def check_exist_dir(path: Path, dir_name: str = "") -> bool:
    if dir_name:
        return path.joinpath(dir_name).exists()
    return path.exists()


def comments_to_multiline_string(fields: list, row: Iterable) -> str:
    comments = ''''''
    for idx, field in enumerate(fields):
        comments += str(field).replace('_', ' ').title() + ': {' + str(idx) + '}\n\n'

    values = list(map(str, row[fields]))
    comments = comments.format(*values)
    return comments


def replace_key_with_value(src: dict, dest: dict) -> None:
    for key, value in src.items():
        if value in dest:
            dest[key] = dest.pop(value)


def _validate_data(model, serializer, data_dest, data_src):
    queryset = model.objects.get(ps_id__ps_id=data_dest.get('ps_id'))
    database_record = serializer(queryset).data
    print(database_record)

    replace_key_with_value(data_src, data_dest)
    export_record = serializer(data_dest).data
    print(export_record)
