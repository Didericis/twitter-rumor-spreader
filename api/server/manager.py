# manage.py

from flask_script import Manager

from application import application

manager = Manager(application)

if __name__ == "__main__":
    manager.run()
