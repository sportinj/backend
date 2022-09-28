from asyncio.log import logger
import flask
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """

    logger.info('hello, world')


if __name__ == "__main__":
    main()
