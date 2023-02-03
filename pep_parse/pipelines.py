import csv
from datetime import datetime

from pep_parse.constants import BASE_DIR, DATETIME_FORMAT
from pep_parse.database import Pep, create_db

filename_template = 'status_summary_{}.csv'


def prepare_to_write(data):
    return [('Статус', 'Количество')] + [(k, v) for k, v in data.items()]


def write_to_csv(data):
    results_dir = BASE_DIR / 'results'
    # Невозможно перенести эту функцию и/или перенести переменную в constants
    # по той же причине, которая была мной описана в предыдущем задании.
    # Тестирующая система создаёт временную папку в $TMP и не может найти
    # файлы вывода, если results_dir объявлен вне файла pipelines.py
    results_dir.mkdir(exist_ok=True)
    now_formatted = datetime.now().strftime(DATETIME_FORMAT)
    filename = filename_template.format(now_formatted)
    file_path = results_dir / filename
    with open(file_path, 'w', encoding='UTF-8') as file:
        writer = csv.writer(file, dialect=csv.unix_dialect)
        writer.writerows(data)


class PepParsePipeline:
    def open_spider(self, spider):
        self.session = create_db()

    def process_item(self, item, spider):
        quote = Pep(
            number=int(item['number']),
            name=item['name'],
            status=item['status'],
        )

        self.session.add(quote)
        self.session.commit()
        return item

    def close_spider(self, spider):
        statuses = [
            item[0] for item in self.session.query(Pep.status).distinct().all()
        ]

        status_count = {}
        query = self.session.query(Pep)
        for status in statuses:
            status_count[status] = query.filter(Pep.status == status).count()
        status_count['Total'] = query.count()
        write_to_csv(prepare_to_write(status_count))

        self.session.close()
