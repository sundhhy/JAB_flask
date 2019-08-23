import os
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Photo

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Photo=Photo)


@app.cli.command()
@click.argument('test_name', nargs=-1)
def test(test_name):
    """运行单元测试"""
    import unittest
    if test_name:
        tests = unittest.TestLoader().loadTestsFromNames(test_name)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
