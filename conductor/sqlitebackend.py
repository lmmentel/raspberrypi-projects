
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Float, String, MetaData, DateTime

metadata = MetaData()

sensor_data = Table('sensor_data', metadata,
                    Column('timestamp', DateTime, primary_key=True),
                    Column('temperature', Float),
                    Column('pressure', Float),
                    Column('humidity', Float),
                    Column('light_dep_resistance', Float)
                    )


def create_db(db_path):

    engine = create_engine('sqlite:///{}'.format(db_path), debug=True)
    metadata.create_all(engine)


def insert_row(db_path, sensor, ts, temp, pressure, humidity, ldr):
    '''
    Save to the db
    '''

    engine = create_engine('sqlite:///{}'.format(db_path),
                           echo=False)

    with engine.begin() as conn:
        conn.execute(sensor_data.insert(),
                     timestamp=ts,
                     temperature=temp,
                     pressure=pressure,
                     humidity=humidity,
                     light_dep_resistance=ldr)
