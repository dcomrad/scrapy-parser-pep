from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATETIME_FORMAT = '%d.%m.%Y_%H-%M-%S'

DB_NAME = 'sqlite_pep_parse.db'
DB_URL = 'sqlite:///{}'.format(DB_NAME)
