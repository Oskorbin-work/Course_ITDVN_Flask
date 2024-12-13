from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, selectinload, DeclarativeBase


class Base(DeclarativeBase):
    pass


# Клас для таблиці "Користувачі"
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="users")


# Клас для таблиці "Департаменти"
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship("User", back_populates="department")


# PostgreSQL
# username = 'your_username'
# password = 'your_password'
# host = 'localhost'
# port = '5432'
# database = 'database_name'
# postgresql_url = f'postgresql://{username}:{password}@{host}:{port}/{database}'
# engine_postgresql = create_engine(postgresql_url, echo=True)

#SQLite в файле
# engine = create_engine("sqlite:///example.db", echo=True)

#SQLite в памяти
engine = create_engine("sqlite:///:memory:", echo=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Створення об'єктів
department_dev = Department(name="DEV")
department_qa = Department(name="QA")
user1 = User(name="John", department=department_dev)
user2 = User(name="Alice", department=department_dev)
user3 = User(name="Bob", department=department_qa)
user4 = User(name="Mary", department=department_qa)

