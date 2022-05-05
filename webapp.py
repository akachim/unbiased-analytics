import os
from server import create_app, db
from server.models import User, StripeCustomer
from flask_migrate import Migrate




app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_Shell_context():
    return dict(db=db, User=User, StripeCustomer=StripeCustomer)


@app.cli.command()
def test():
    """Run the unit tests."""

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
