import sqlalchemy as db
from requests import Session
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = db.create_engine('sqlite:///user.db', echo=True)
meta = db.MetaData()


mail = Table(
   'mail', meta,
   Column('id', Integer, primary_key=True),
   Column('mail_to', String(255)),
   Column('mail_from', VARCHAR),
   Column('mail_subject', String),
   Column('mail_date',String)
)
session = Session()
meta.create_all(engine)




