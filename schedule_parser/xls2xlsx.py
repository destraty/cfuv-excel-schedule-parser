import jpype
import os
import asposecells


def xls2xlsx(folder: str) -> None:
    """
    Преобразовывает .xls документы в .xlsx без потери структуры
    :param folder:
    :return: None
    """
    jpype.startJVM()
    from asposecells.api import Workbook
    folder_path = folder
    file_list = os.listdir(folder_path)

    for file_name in file_list:
        if file_name.endswith(".xls"):
            print(f'{file_name} преобразован в .xlsx ')
            workbook = Workbook(f"{folder_path}{file_name}")
            workbook.save(f"{folder_path}{file_name.replace('.xls', '')}.xlsx")
            os.remove(f'{folder_path}{file_name}')
    jpype.shutdownJVM()
