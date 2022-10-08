import logging

from backend.players.views import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info('hello, world')
    app.run()


if __name__ == '__main__':
    main()
