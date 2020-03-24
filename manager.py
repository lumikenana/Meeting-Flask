from Meeting import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


"""
数据库迁移命令：
    # 新增加数据库时，执行三个命令
    python manager.py db init
    # 修改数据库字段定义时，执行下面两个就好了
    python manager.py db migrate
    python manager.py db upgrade
    
"""
manager.add_command('db', MigrateCommand)

# @manager.command
# def create_all():
#     """执行：python manager create_all"""
#     with app.app_context():
#         db.create_all()


@manager.command
def custom(arg):
    """自定义命令：python manager.py custom 123"""
    print(arg)


@manager.option('-n', '--name', dest='name')
@manager.option('-u', '--url', dest='url')
def cmd(name, url):
    """自定义命令：python manager.py cmd -n lipipi -u http://www.baidu.com"""
    print(name, url)


if __name__ == '__main__':
    manager.run()
#     运行程序时，执行：python manager.py runserver
