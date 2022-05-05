import os

from server import create_app

app = create_app(os.environ.get("FLASK_CONFIG") or 'default')

app.app_context().push()


from server import celery_app