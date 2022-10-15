import logging

from flask import Flask
from pydantic import ValidationError

from backend.database import db_session
from backend.errors import AppError
from backend.players.views import player_view
from backend.teams.views import team_view

app = Flask(__name__)

app.register_blueprint(team_view, url_prefix='/api/teams')

app.register_blueprint(player_view, url_prefix='/api/players')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def shutdown_session(exception=None):
    db_session.remove()


def handle_app_error(error: AppError):
    return {'error': str(error)}, error.code


def handle_validation_error(error: ValidationError):
    return {'error': str(error)}, 400


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)

app.teardown_appcontext(shutdown_session)


def main():
    logger.info('hello, world')
    app.run()


if __name__ == '__main__':
    main()
