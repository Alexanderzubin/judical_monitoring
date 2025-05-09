import logging
from pathlib import Path
import sys
from pythonjsonlogger.json import JsonFormatter

PROJECT_ROOT = str(Path(__file__).parent.parent)


class RelativePathFilter(logging.Filter):
    def filter(self, record):
        try:
            record.path = Path(record.pathname).resolve().relative_to(PROJECT_ROOT)
        except ValueError:
            # Если файл вне PROJECT_ROOT, используем абсолютный путь
            record.relpath = Path(record.pathname).resolve()
        return True


def setup_logging(level='INFO'):
    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(path)s:%(lineno)d %(message)s',
        json_ensure_ascii=False,
    )
    handler.setFormatter(formatter)
    handler.addFilter(RelativePathFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

    # Prevent duplicate logs
    root_logger.propagate = False
