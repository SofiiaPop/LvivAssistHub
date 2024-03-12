
import sqlite3
from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///users.db', echo=True)

Base = declarative_base()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

class Employee(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    description = Column(String)
    price = Column(Integer)

class VentilationCleaners(Employee):
    __tablename__ = 'ventilation_cleaners'

class PlumbingTechnicians(Employee):
    __tablename__ = 'plumbing_technicians'

class FurnitureRepair(Employee):
    __tablename__ = 'furniture_repair'

class SecuritySystem(Employee):
    __tablename__ = 'security_system'

class Electricians(Employee):
    __tablename__ = 'electricians'

class WindowDoorReplacement(Employee):
    __tablename__ = 'window_and_door_replacement'

class Landscape(Employee):
    __tablename__ = 'landscape'

class HeatingSystem(Employee):
    __tablename__ = 'heating_system'

class Cleaning(Employee):
    __tablename__ = 'cleaning'

class RoofRepair(Employee):
    __tablename__ = 'roof_repair'

class Other(Employee):
    __tablename__ = 'other'
    hashtag = Column(String)

Base.metadata.create_all(engine)
# def add_new_user(name, surname, email, phone, hashtag):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     # session.query(VentilationCleaners).delete()
#     # session.query(PlumbingTechnicians).delete()
#     # session.query(FurnitureRepair).delete()
#     # session.query(SecuritySystem).delete()
#     # session.query(Electricians).delete()
#     # session.query(WindowDoorReplacement).delete()
#     # session.query(Landscape).delete()
#     # session.query(HeatingSystem).delete()
#     # session.query(Cleaning).delete()
#     # session.query(RoofRepair).delete()
#     # session.query(Other).delete()
#     new_user = add_hashtag_profile(name, surname, email, description, hashtag)
#     session.add(new_user)
#     session.commit()
#     session.close()

def add_hashtag_profile(name, surname, email, description, price, hashtag):
    Session = sessionmaker(bind=engine)
    session = Session()
    if hashtag == 'VentilationCleaners':
        new_user = VentilationCleaners(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'PlumbingTechnicians':
        new_user = PlumbingTechnicians(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'FurnitureRepair':
        new_user = FurnitureRepair(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'SecuritySystem':
        new_user = SecuritySystem(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'Electricians':
        new_user = Electricians(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'WindowDoorReplacement':
        new_user = WindowDoorReplacement(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'Landscape':
        new_user = Landscape(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'HeatingSystem':
        new_user = HeatingSystem(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'Cleaning':
        new_user = Cleaning(name=name, surname=surname, email=email, description=description, price=price)
    elif hashtag == 'RoofRepair':
        new_user = RoofRepair(name=name, surname=surname, email=email, description=description, price=price)
    else:
        new_user = Other(name=name, surname=surname, email=email, description=description, price=price, hashtag=hashtag)
    session.add(new_user)
    session.commit()
    session.close()
    return new_user

def get_hashtags():
    Session = sessionmaker(bind=engine)
    session = Session()
    service_providers = session.query(Other).all()
    hashtags = [sp.hashtag for sp in service_providers]
    session.close()
    return set(list(hashtags))

def show_employees(hashtag):
    engine = create_engine('sqlite:///users.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    employee_class = globals().get(hashtag)
    if employee_class:
        service_providers = session.query(employee_class).all()
        employees_data = [{
            'name': sp.name,
            'surname': sp.surname,
            'email': sp.email,
            'description': sp.description,
        } for sp in service_providers]
        session.close()

        if employees_data:
            return render_template("employee.html", employees=employees_data)

    other_table = globals().get('Other')
    if other_table:
        service_providers = session.query(other_table).filter(other_table.hashtag == hashtag).all()
        employees_data = [{
            'name': sp.name,
            'surname': sp.surname,
            'email': sp.email,
            'description': sp.description,
        } for sp in service_providers]
        session.close()

        if employees_data:
            return render_template("employee.html", employees=employees_data)
    if hashtag is None:
        return render_template("index.html", hashtags=get_hashtags())
    alert_script = f'''
        <script>
        window.onload = function() {{
            alert("Unfortunately, we are still searching for employees that could fulfill your request for {hashtag}");
        }}
        </script>
        '''
    return render_template("index.html", hashtags=get_hashtags(), alert_script=alert_script)

if __name__ == "__main__":
    app.run(debug=True)
