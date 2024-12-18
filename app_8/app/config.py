import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance_1', 'my_database.db')


class Config:
	TESTING = False
	JWT_SECRET_KEY="dev"
	SQLALCHEMY_DATABASE_URI="sqlite:///expenses.sqlite3"


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
