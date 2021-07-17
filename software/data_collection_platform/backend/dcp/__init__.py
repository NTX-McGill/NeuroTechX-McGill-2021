from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dcp.extensions import celery, db
from dcp.utils.celery import init_celery

from dcp.cfg.config import app_configs

# FLASK EXTENSIONS
# global database object
migrate = Migrate(compare_type=True)

cors = CORS()


def create_app():
    app = Flask(__name__)

    app.config.from_object(app_configs)

    celery.conf.update(app.config)
    # configure celery tasks to run within app context
    init_celery(app=app, celery=celery)

    with app.app_context():
        from dcp import api
        app.register_blueprint(api.bp)

        # importing models so that Flask-Migrate can detect them
        from dcp.models.collection import CollectionInstance
        from dcp.models.configurations import OpenBCIConfig
        from dcp.models.data import CollectedData
        from dcp.models.video import Video

        # initialize extensions
        cors.init_app(app)
        db.init_app(app)
        db.create_all()  # NOTE: will not recreate tables that already exist
        migrate.init_app(app, db)

    return app
