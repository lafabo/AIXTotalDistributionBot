#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MAIN PROGRAM
"""
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from blockchain.events import last_block, fetch_logs, decode_log
from bot.bot import send_report
from bot.report import prepare_report_data, create_report_message
from db.database import get_session, store_event, get_events, create_db_and_tables
from settings import blockchain_events_trigger, telegram_report_trigger

# initialising and configuring logger to use in multiply project modules
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setting up schedule
schedule = BlockingScheduler()


def get_and_process_blockchain_logs():
    """ Main blockchain worker;
    Used to fetch from blockchain, decode and process logs, then store as events """
    current_block = last_block()
    start_block = current_block - 7200  # ~24h. 1 block each 12 seconds, 5 blocks a minute, 24h * 60m * 5 blocks = 7200

    # getting smart contract's logs with TotalDistribution event
    logs = fetch_logs(start_block, current_block)

    # decoding and processing logs
    for log in logs:
        event_data = decode_log(log)

        # saving them as TotalDistribution objects to db
        if event_data:
            with get_session() as session:
                store_event(event_data, session)


def generate_and_send_report(hours=24):
    """ Getting TotalDistributionEvents from db in time range and process them to create report message """
    report_events = get_events(hours=hours)
    report_data = prepare_report_data(report_events)
    report_message = create_report_message(report_data)
    send_report(report_message)


if __name__ == "__main__":
    # At startup checks DB, fetches new logs with TotalDistribution event, create and send report
    create_db_and_tables()  # db/database init db if needed
    get_and_process_blockchain_logs()  # (blockchain/events) looks is there new TotalDistribution Event Logs
    generate_and_send_report()  # (bot/report) creates and send report to Telegram group

    # After that script uses schedule from settings.py
    # task was to send reports every 4 hours, but in demonstration porpoise that was changed to a once an hour
    schedule.add_job(get_and_process_blockchain_logs, trigger=blockchain_events_trigger, misfire_grace_time=1000)
    schedule.add_job(generate_and_send_report, trigger=telegram_report_trigger, misfire_grace_time=1000)
    schedule.start()
