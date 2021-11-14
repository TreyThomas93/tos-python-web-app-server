from assets.multifilehandler import MultiFileHandler
from assets.extensions import mongo, bcrypt
from api.accounts import accounts
from api.strategies import strategies
from api.positions import positions
from api.queue import queue
from auth.routes import auth
from assets.timeformatter import Formatter

from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import certifi
ca = certifi.where()

load_dotenv(dotenv_path="config.env")


def create_app():

    app = Flask(__name__)

    CORS(app)

    app.config["MONGO_URI"] = os.getenv('MONGO_URI')

    app.config["ENV"] = os.getenv('ENV')

    app.config["DEBUG"] = os.getenv('DEBUG')

    mongo.init_app(app, tlsCAFile=ca)

    bcrypt.init_app(app)

    app.config["SECRET_KEY"] = list(mongo.db.users.find())[0]["Password"]

    # setup logger only if not in debug mode
    if app.debug:

        limiter = Limiter(app, key_func=get_remote_address)

        # 100 requests per minute allowed
        limiter.limit("100/minute")(accounts)

        limiter.limit("100/minute")(strategies)

        limiter.limit("100/minute")(positions)

        limiter.limit("100/minute")(queue)

        # 30 requests per minute allowed
        limiter.limit("30/minute")(auth)

        file_handler = MultiFileHandler(filename='logs/error.log', mode='a')

        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler.setFormatter(formatter)

        app.logger.addHandler(file_handler)

        limiter.logger.addHandler(file_handler)

    app.register_blueprint(accounts)

    app.register_blueprint(strategies)

    app.register_blueprint(positions)

    app.register_blueprint(queue)

    app.register_blueprint(auth)

    return app


if __name__ == "__main__":

    app = create_app()

    app.run()
