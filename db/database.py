# -*- coding: utf-8 -*-
"""
DATABASE FUNCTIONS
All functions to use DB in the project in one module.

get_session() -- database session. Made separate and selectable for easy testing
create_db_and_tables() -- init the db and tables from SQLAlchemy models metadata
store_event() -- store decoded and processed blockchain event log into TotalDistributionEvent object and db
get_events() -- get from db TotalDistributionEvent objects with timestamp in last x hours
"""
import datetime
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from db.models import TotalDistributionEvent, Base
from settings import DB_URL


logger = logging.getLogger(__name__)


engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    db_session = Session()
    try:
        yield db_session
    except SQLAlchemyError as e:
        logger.error(f"Can't connect to database: {e}")
        db_session.rollback()
    finally:
        db_session.close()


def create_db_and_tables():
    """ Create the tables for models in the database if they not exists yet """
    Base.metadata.create_all(engine)


def store_event(decoded_log_event, db_session=get_session()):
    """ Store single TotalDistributionEvent object into db

    I wasn't sure about opportunity of multiple TotalDistribution Events for a single transaction.
    So the code is designed to pass only unique events to avoid storing duplicate values even
    there is more than one TotalDistribution Event in single transaction.

    :param decoded_log_event: decoded and processed log TotalDistribution event dict """
    with db_session:
        try:
            # It's uncertain if it's possible to have multiple TotalDistribution events in a single transaction.
            # Theoretically, it's possible with tools like https://furucombo.app/ or through arbitrage bots,
            # MEV, sandwich strategies and so on. So decided to check if any existing event fully matches the new event
            existing_event = db_session.query(TotalDistributionEvent).filter_by(
                tx_hash=decoded_log_event['tx_hash'],
                distributor_wallet=decoded_log_event['distributor_wallet'],
                input_aix_amount=decoded_log_event['input_aix_amount'],
                distributed_aix_amount=decoded_log_event['distributed_aix_amount'],
                swapped_eth_amount=decoded_log_event['swapped_eth_amount'],
                distributed_eth_amount=decoded_log_event['distributed_eth_amount']
            ).one_or_none()

            if existing_event:
                logger.info(f"Event already added, skipping. Event tx: {existing_event.tx_hash}")
            else:
                # No matching event found; add the new event.
                new_event = TotalDistributionEvent(**decoded_log_event)
                db_session.add(new_event)
                db_session.commit()
                logger.info(f"Event {new_event.tx_hash} stored successfully.")

        except SQLAlchemyError as e:
            db_session.rollback()  # Ensure the session is rolled back on error.
            logger.error(f"Error storing event: {e}")


def get_events(hours=24, db_session=get_session()) -> [TotalDistributionEvent]:
    """ Get from db a TotalDistributionEvent objects list matching time range from now """
    now = datetime.datetime.utcnow()  # we store timestamps in utc tz, as in eth blockchain
    start_time = now - datetime.timedelta(hours=hours)
    with get_session() as session:
        events = session.query(TotalDistributionEvent).filter(TotalDistributionEvent.timestamp >= start_time).all()
        return events
