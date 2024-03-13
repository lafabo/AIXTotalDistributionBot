import pytest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import store_event, get_events
from db.models import Base, TotalDistributionEvent

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="module")
def test_session(test_engine):
    """Creates a new database session for a test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_store_event_successful_storage(test_session):
    # sample event
    event_data = {
        "block": 12345,
        "tx_hash": "unique_tx_hash",
        "timestamp": datetime.datetime.utcnow(),
        "distributor_wallet": "wallet_address",
        "input_aix_amount": "1000",
        "distributed_aix_amount": "900",
        "swapped_eth_amount": "0.5",
        "distributed_eth_amount": "0.45",
    }
    # Store the event
    store_event(event_data, db_session=test_session)
    # Verify the event was stored
    with test_session as session:
        stored_events = session.query(TotalDistributionEvent).filter_by(tx_hash="unique_tx_hash").all()
        assert len(stored_events) == 1
        assert stored_events[0].distributor_wallet == "wallet_address"


def test_get_distribution_events_returns_correct_events(test_session):
    # Fetch events from the last 24 hours
    with test_session as db_test_session:
        recent_events = get_events(hours=24, db_session=db_test_session)
        # Verify that only events within the last 24 hours are returned
        assert all(event.timestamp > datetime.datetime.utcnow() - datetime.timedelta(hours=24) for event in recent_events)