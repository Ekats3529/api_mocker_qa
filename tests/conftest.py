import pytest
import allure
import coloredlogs
import logging

# Инициализируем логгер для этого файла
logger = logging.getLogger(__name__)


def pytest_configure(config):
    # Настраиваем красивые логи в терминале
    coloredlogs.install(
        level='INFO',
        fmt='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S',
        level_styles={
            'info': {'color': 'green'},
            'error': {'color': 'red', 'bold': True},
            'warning': {'color': 'yellow'}
        }
    )
