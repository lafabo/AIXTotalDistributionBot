# -*- coding: utf-8 -*-
"""
REPORTS

All about processing saved in DB TotalDistributionEvent objects to make text message report.

format_duration() -- for human durations like "8m ago"
prepare_report_data() -- aggregating list of TotalDistributionEvents to statistical data to be included in report
create_report_message() -- inserting prepared statistical data in markdown2 telegram message
"""
import datetime
from blockchain.events import get_wallet_balance, web3
from settings import CONTRACT_ADDRESS


def format_duration(delta: datetime.timedelta) -> str:
    """ Formats durations into a more human format like "1h20m ago" """
    hours, remainder = divmod(delta.total_seconds(), 3600)
    minutes = remainder // 60
    if hours and minutes:
        return f"{int(hours)}h{int(minutes)}m ago"
    elif hours:
        return f"{int(hours)}h ago"
    else:
        return f"{int(minutes)}m ago"


def prepare_report_data(events) -> dict[str, any]:
    """ Process TotalDistributionEvent objects to aggregate data for reporting """
    if events:
        # Make sure all events have been in ascending order of timestamp
        events.sort(key=lambda event: event.timestamp)

        report_data = {
            'first_tx_ago': format_duration(datetime.datetime.utcnow() - events[0].timestamp),
            'last_tx_ago': format_duration(datetime.datetime.utcnow() - events[-1].timestamp),

            'aix_processed': web3.from_wei(sum(event.input_aix_amount for event in events), "ether"),
            'aix_distributed': web3.from_wei(sum(event.distributed_aix_amount for event in events), "ether"),
            'eth_bought': web3.from_wei(sum(event.swapped_eth_amount for event in events), "ether"),
            'eth_distributed': web3.from_wei(sum(event.distributed_eth_amount for event in events), "ether"),
            'distributor_wallets': {event.distributor_wallet: get_wallet_balance(event.distributor_wallet) for event in events}
            # Not sure if there can be only one distributor wallet, so predict the situation where appear few wallets
        }
        return report_data
    return


def create_report_message(data: dict[str, any]) -> str:
    """ Generates the report message from aggregated data """
    if not data:
        return (f"Sorry, no updates for the last 24 hours. Maybe an issue."
                f"Check manually at https://etherscan.io/address/{CONTRACT_ADDRESS}")

    # in case there can be more than one wallet
    wallets_info = "\n".join(
        [f"Distributor wallet: {wallet}\n"
         f"Distributor balance: {balance:.4f} ETH" for wallet, balance in data['distributor_wallets'].items()])

    report = (f"\nDaily $AIX Stats:\n"
              f"- First TX: {data['first_tx_ago']}\n"
              f"- Last TX: {data['last_tx_ago']}\n"
              f"- AIX processed: {data['aix_processed']:,.2f}\n"
              f"- AIX distributed: {data['aix_distributed']:,.2f}\n"
              f"- ETH bought: {data['eth_bought']:,.2f}\n"
              f"- ETH distributed: {data['eth_distributed']:,.2f}\n\n"
              f"{wallets_info}")
    return "```" + report + "```"  # Format as code in Telegram
