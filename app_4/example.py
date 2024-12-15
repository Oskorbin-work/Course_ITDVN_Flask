from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, selectinload, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="users")

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

department_dev = Department(name="DEV")
department_qa = Department(name="QA")
user1 = User(name="John", department=department_dev)
user2 = User(name="Alice", department=department_dev)
user3 = User(name="Bob", department=department_qa)
user4 = User(name="Mary", department=department_qa)

session.add_all([department_dev, department_qa, user1, user2, user3, user4])
session.commit()

"""
departments = session.query(Department).all()
for dep in departments:
    print(f"\tDepartment: {dep.name}")
    for user in dep.users:
        print(f"\t\tUser (lazy loaded): {user.name}")
"""

"""
departments_with_user_count = (
    session.query(Department.name, func.count(User.id))
    .outerjoin(User)
    .group_by(Department.id)
    .all()
)
print("Departments with user count:")
for dep in departments_with_user_count:
    print(f"\tDepartment: {dep[0]}, User count: {dep[1]}")
"""

user = session.query(User).filter_by(name="John").first()
if user:
    user.department.name = "HR"
    session.commit()

departments = session.query(Department).options(selectinload(Department.users)).all()
for dep in departments:
    print(f"\tDepartment: {dep.name}")
    for user in dep.users:
        print(f"\t\tUser (eager loaded): {user.name}")

session.query(User).delete()
session.commit()