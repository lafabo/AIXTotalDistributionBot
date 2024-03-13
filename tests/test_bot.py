import datetime
from decimal import Decimal
import pytest
from unittest.mock import MagicMock
from bot.report import format_duration, prepare_report_data


@pytest.mark.parametrize("timedelta,expected", [
    (datetime.timedelta(hours=1, minutes=1), "1h1m ago"),  # 1 hour and 1 minute
    (datetime.timedelta(hours=1), "1h ago"),  # Exactly 1 hour
    (datetime.timedelta(minutes=59), "59m ago"),  # 59 minutes
])
def test_format_duration(timedelta, expected):
    assert format_duration(timedelta) == expected


def test_get_report_data(mocker):
    # mock eth address
    mock_wallet_address = "0x1234567890123456789012345678901234567890"

    # Mock get_distribution_events to return a predictable list of events
    mock_events = [
        MagicMock(timestamp=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
                  input_aix_amount=Decimal('1000000000000000000'),  # 1 AIX
                  distributed_aix_amount=Decimal('500000000000000000'),  # 0.5 AIX
                  swapped_eth_amount=Decimal('2000000000000000000'),  # 2 ETH
                  distributed_eth_amount=Decimal('1000000000000000000'),  # 1 ETH
                  distributor_wallet=mock_wallet_address),
    ]

    mocker.patch('bot.report.prepare_report_data', return_value=mock_events)
    mocker.patch('blockchain.events.get_wallet_balance', return_value=Decimal('1.5'))  # Mock wallet balance

    data = prepare_report_data(mock_events)

    assert data['aix_processed'] == Decimal('1')


