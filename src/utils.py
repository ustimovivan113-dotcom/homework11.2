import logging

logging.basicConfig(
    filename='logs/utils.log',
    filemode='w',
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('utils')

def get_date(date_str: str) -> str:
    logger.info(f"Вызвана функция get_date с аргументом: {date_str}")
    try:
        formatted_date = date_str.split('T')[0].split('-')[::-1]
        formatted_date = '.'.join(formatted_date)
        logger.info(f"Результат: {formatted_date}")
        return formatted_date
    except Exception as e:
        logger.error(f"Ошибка в get_date: {str(e)}")
        raise