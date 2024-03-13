# -*- coding: utf-8 -*-
"""
BLOCKCHAIN EVENTS

Module with all functions to get data from ETH blockchain

fetch_logs() -- filter and get smart contracts event logs
decode_log() -- decode and process each fetched from blockchain event log to event dict
get_wallet_balance() -- used for creating reports
last_block() -- get last block num
"""
import logging
from datetime import datetime
from web3 import Web3
from decimal import Decimal
from settings import WEB3_PROVIDER_URL, CONTRACT_ADDRESS, TOTAL_DISTRIBUTION_EVENT_SIGNATURE_TEXT


# Setup logging for monitoring and debugging
logger = logging.getLogger(__name__)


# Initialize Web3
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
assert web3.is_connected(), logger.error("Failed to connect to the Ethereum network. Check WEB3_PROVIDER_URL.")


# Keccak hash of the TotalDistribution event signature
event_signature = web3.keccak(text=TOTAL_DISTRIBUTION_EVENT_SIGNATURE_TEXT).hex()


def fetch_logs(start_block, end_block):
    """ Fetches logs with TotalDistribution event from smart contract in the given block range.

    :params start_block, end_block: blockchain block range
    :return list: of blockchain smart contract filtered by block range, contract address and event signature logs """
    filter_params = {
        'fromBlock': start_block,
        'toBlock': end_block,
        'address': CONTRACT_ADDRESS,
        'topics': [event_signature],
    }
    try:
        return web3.eth.get_logs(filter_params)
    except Exception as e:
        logger.error(f"Failed to fetch logs: {e}")
        return []


def decode_log(log):
    """Decodes TotalDistribution event data and extracting relevant information from blockchain log entry.

    :param log: single blockchain event log entire
    :return decoded_log_event dict: with cleared and transformed data from event log entire"""
    try:
        total_distribution_data = web3.codec.decode(['uint256', 'uint256', 'uint256', 'uint256'], log['data'])
        transaction = web3.eth.get_transaction(log['transactionHash'])
        block = web3.eth.get_block(log['blockNumber'])  # we need it to get timestamp
        return {
            'block': log['blockNumber'],
            'tx_hash': log['transactionHash'].hex(),
            'timestamp': datetime.utcfromtimestamp(block['timestamp']),
            'distributor_wallet': transaction['from'],

            # TotalDistribution decoded data:
            'input_aix_amount': Decimal(total_distribution_data[0]),
            'distributed_aix_amount': Decimal(total_distribution_data[1]),
            'swapped_eth_amount': Decimal(total_distribution_data[2]),
            'distributed_eth_amount': Decimal(total_distribution_data[3])
            }  # Decimal() accurate enough for storing in db ETH wei, ether and other converted from HexBytes num values

    except Exception as e:
        logger.error(f"Failed to process log: {e}")
        return None


def get_wallet_balance(wallet):
    """ Retrieves the current balance of a given wallet address, converting the value from Wei to Ether. """
    return web3.from_wei(web3.eth.get_balance(wallet), "ether")


def last_block():
    """ returns last block number; needed to get timerange (default equal 7200 blocks / 24h ) """
    return web3.eth.block_number
