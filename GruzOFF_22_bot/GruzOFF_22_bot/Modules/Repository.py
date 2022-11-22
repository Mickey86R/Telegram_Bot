from email.mime import application
import os
import logging
import asyncio

from sqlalchemy import ForeignKey, MetaData, Column, Integer, BigInteger, Text, String, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

engine = create_engine(f"sqlite:///MyDB")

session_factory = sessionmaker(bind=engine, expire_on_commit=False)
session = scoped_session(session_factory)

Base = declarative_base()
metadata = MetaData()

class UserVerified(Base):
    __tablename__ = 'UserVerified'
    id = Column(Integer, primary_key = True)
    verified = Column(Boolean)
    applications = relation('Application')

class Application(Base):
    __tablename__ = 'Application'
    id = Column(BigInteger, primary_key=True)
    from_user = Column(Integer, ForeignKey(UserVerified.id))
    day = Column(String(15))
    humans = Column(String(10))
    address = Column(String(50))
    time = Column(String(50))
    task = Column(String(200))
    pay = Column(String(100))
    status = Column(String(100))
    from_admin = Column(String(50))

class LastApplication(Base):
    __tablename__ = 'LastApplication'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey(UserVerified.id))
    application_id = Column(BigInteger, ForeignKey(Application.id))

#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)

# Add new or update current user
def new_or_update_user(user_id, verified):
    
    if(check_user_in_db(user_id)):
        item = session.query(UserVerified).get(user_id)
        item.verified = verified
        session.add(item)
    else:
        newItem = UserVerified(id = int(user_id), verified = bool(verified))
        session.add(newItem)

    session.commit()
    session.close()

# Check user in DataBase
def check_user_in_db(user_id):
    return session.query(UserVerified).get(user_id) is not None

# Add new application
def new_app(number_app, user_id, user_data):
    item = Application(
                        id = number_app,
                        from_user = user_id,
                        day = user_data.get('day'),
                        humans = user_data.get('humans'),
                        address = user_data.get('address'),
                        time = user_data.get('time'),
                        task = user_data.get('task'),
                        pay = user_data.get('pay'),
                        status = 'На согласовании'
                        )
    session.add(item)
    
    item = LastApplication(
                        user_id = user_id,
                        application_id = number_app
                        )
    session.add(item)
    session.commit()
    #session.close()

def get_app(number_app):
    
    item:Application = session.query(Application).get(number_app)
    print(f'from get_app: {item}')
    return item

def get_last_app_from_user_id(user_id):
    print(f'user_id == {user_id}')
    item = session.query(LastApplication).filter(LastApplication.user_id == user_id).first()
    return item.application_id

# Edit application  status
def edit_app_status(app_id, status, admin_id):
    
    item = session.query(Application).get(app_id)
    item.status = status
    item.from_admin = admin_id

    session.add(item)
    session.commit()
    #session.close()

def get_user_id_from_number_app(number_app):
    item = session.query(Application).get(number_app)
    session.close()

    return item.from_user