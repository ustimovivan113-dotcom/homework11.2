import logging

# Настройка логирования для модуля utils
logging.basicConfig(
    filename='logs/utils.log',  # Путь к файлу лога
    filemode='w',  # Перезаписывать при каждом запуске
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',  # Формат
    level=logging.INFO  # Уровень логирования
)
logger = logging.getLogger('utils')

def get_date(date_str: str) -> str:
    logger.info(f"Вызвана функция get_date с аргументом: {date_str}")
    try:
        # Преобразование даты из формата ГГГГ-ММ-ДДTЧЧ:ММ:СС в ДД.ММ.ГГГГ
        formatted_date = date_str.split('T')[0].split('-')[::-1]
        formatted_date = '.'.join(formatted_date)
        logger.info(f"Результат: {formatted_date}")
        return formatted_date
    except Exception as e:
        logger.error(f"Ошибка в get_date: {str(e)}")
        raise