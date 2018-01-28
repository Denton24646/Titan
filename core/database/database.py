import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey
from threading import Lock


db_name = 'core.db'
db_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), db_name)
lock = Lock()
engine = create_engine('sqlite:///{}'.format(db_fullpath), connect_args={'check_same_thread': False}, echo=False)
metadata = MetaData()

OHLCV = Table('OHLCV', metadata,
              Column('ID', Integer, primary_key=True),
              Column('Exchange', String),
              Column('Pair', String),
              Column('Timestamp', String),
              Column('Open', Float),
              Column('High', Float),
              Column('Low', Float),
              Column('Close', Float),
              Column('Volume', Float),
              Column('Interval', String),
              Column('TimestampRaw', Integer)
              )

TradingPairs = Table('TradingPairs', metadata,
                     Column('PairID', String, primary_key=True),
                     Column('BaseCurrency', String),
                     Column('QuoteCurrency', String),
                     )

TAIdentifier = Table('TAIdentifier', metadata,
                      Column('IndicatorID', Integer, primary_key=True),
                      Column('Description', String),
                      )

TAMovingAverage = Table('TAMovingAverage', metadata,
                         Column('AverageID', Integer, primary_key=True),
                         Column('Exchange', String),
                         Column('Pair', String),
                         Column('Time', String),
                         Column('Close', Float),
                         Column('Interval', Integer),
                         Column('MovingAverage', Float),
                         Column('TimestampRaw', Integer)
                         )

TAVolumeChange = Table('TAVolumeChange', metadata,
                         Column('VolumeID', Integer, primary_key=True),
                         Column('Exchange', String),
                         Column('Pair', String),
                         Column('Time', String),
                         Column('Volume', Float),
                         Column('Interval', Integer),
                         Column('PercentVolumeChange', Float),
                         Column('TimestampRaw', Integer)
                         )

TradingOrders = Table('TradingOrders', metadata,
                      Column('Timestamp', String),
                      Column('OrderID', Integer, primary_key=True),
                      Column('Exchange', String),
                      Column('Pair', String),
                      Column('Position', String),
                      Column('Amount', Float),
                      Column('Price', Float),
                      Column('Simulated', String)
                      )

def drop_tables():
    print('Dropping tables...')
    #metadata.drop_all(engine)
    TradingPairs.drop(engine)
    TAIdentifier.drop(engine)
    TAVolumeChange.drop(engine)
    TAMovingAverage.drop(engine)

def create_tables():#
    print('Creating tables...')
    #metadata.create_all(engine)
    TradingPairs.create(engine)
    TAIdentifier.create(engine)
    TAVolumeChange.create(engine)
    TAMovingAverage.create(engine)

def reset_db():
    print('Resetting database...')
    drop_tables()
    create_tables()