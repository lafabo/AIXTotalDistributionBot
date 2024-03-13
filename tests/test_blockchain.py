import pytest
from unittest.mock import MagicMock
from blockchain.events import fetch_logs


@pytest.fixture
def mock_web3(monkeypatch):
    # Mocking Web3 object
    class MockWeb3:
        eth = MagicMock()

    mock_web3 = MockWeb3()
    monkeypatch.setattr("blockchain.events.web3", mock_web3)
    return mock_web3


def test_fetch_logs(mock_web3):
    expected_logs = [{'blockNumber': 12345, 'data': 'mocked_data', 'transactionHash': '0xhash'}]
    mock_web3.eth.get_logs.return_value = expected_logs

    start_block = 10000
    end_block = 10100
    logs = fetch_logs(start_block, end_block)

    assert logs == expected_logs
    mock_web3.eth.get_logs.assert_called_once()
