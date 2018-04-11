# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/6 13:32
@Author  : zhaoguoqing600689
@File    : manage.py
@Software: PyCharm
"""
import os
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

COV = None
if os.environ.get('TOPNEWS_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('TOPNEWS_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests"""
    if coverage and not os.environ.get('TOPNEWS_COVERAGE'):
        import sys
        os.environ['TOPNEWS_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade, init
    from app.models import Role, User

    # init()

    # 把数据库迁移到最新版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()

    User.add_self_follows()


if __name__ == '__main__':
    manager.run()

