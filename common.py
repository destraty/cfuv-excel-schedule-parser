from pathlib import Path
import tempfile

import re


ROOT_DIR = Path(__file__).resolve().parents[0].as_posix()
SQL_PATH = f"{ROOT_DIR}/storage/teacher_rating.db"
TEMP_DIR = Path(tempfile.gettempdir()).as_posix()


def is_url(string):
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return bool(url_pattern.search(string))

if __name__ == "__main__":
    print(ROOT_DIR)
    print(TEMP_DIR)
    print(SQL_PATH)

