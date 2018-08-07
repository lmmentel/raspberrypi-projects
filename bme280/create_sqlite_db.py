
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, String, MetaData, DateTime

metadata = MetaData()

tsdta = Table('sensor_data', metadata,
              Column('timestamp', DateTime, primary_key=True),
              Column('temperature', Float),
              Column('pressure', Float),
              Column('humidity', Float)
             )

engine = create_engine('sqlite:///rpisensor.db', debug=True)

metadata.create_all(engine)