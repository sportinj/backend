from asyncio.log import logger
import flask
import logging
from backend.teams import app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """

    logger.info('hello, world')
    app.run()


if __name__ == "__main__":
    main()
