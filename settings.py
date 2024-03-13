# -*- coding: utf-8 -*-
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
"""
SETTINGS

If you prefer not to use Infura (e.g., if you have your own Ethereum node), you can select an alternative provider from:
https://web3py.readthedocs.io/en/stable/providers.html
Then, change the WEB3_PROVIDER variable in blockchain/worker.py to your chosen provider.


After creating a new Telegram bot, you must:
1. Make it an admin in the group.
2. Turn off Group Privacy in the bot's settings at @BotFather (Settings > Group Privacy > OFF).


Enhance security by storing sensitive information such as API keys or PostgreSQL passwords in environment variables:
1. In the terminal (with virtualenv activated): export PASSWORD="password"
2. Install python-dotenv: pip install python-dotenv
In the config file:
3. Import dotenv: from dotenv import load_dotenv
4. Load environment variables: load_dotenv()
5. Replace hardcoded PASSWORD with: PASSWORD = os.getenv('PASSWORD')
"""

# WEB3 Provider
INFURA_KEY = "..."  # "YOUR-KEY"  # You can get one free KEY at https://www.infura.io
WEB3_PROVIDER_URL = f'https://mainnet.infura.io/v3/{INFURA_KEY}'


# Telegram
TELEGRAM_API_KEY = "..."  # Telegram > @BotFather > Create New Bot
TELEGRAM_CHAT_ID = -1002027272548  # Add @raw_data_bot to your chat or send to the bot chat's invite link to get id


# ETH SMART CONTRACT DETAILS
CONTRACT_ADDRESS = "0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0"
TOTAL_DISTRIBUTION_EVENT_SIGNATURE_TEXT = "TotalDistribution(uint256,uint256,uint256,uint256)"


# DATABASE / PostgreSQL SETTINGS
DB_HOST = "127.0.0.1"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "distributions"
DB_PORT = "5432"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DB_URL = f"sqlite:///sqlite.db"  # sqlite for dev env


# SCHEDULE
# The schedule can be adjusted to more human-friendly times, such as the start and end of the workday.
# Note: The schedule uses the server's time zone (e.g., Europe/Moscow in this case).

# run.get_and_process_blockchain_logs() retrieves new TotalDistribution events from smart contract logs, stores into db
# once a half hour
blockchain_events_trigger = OrTrigger(
    [CronTrigger(hour=0, minute=28),
     CronTrigger(hour=0, minute=58),
     CronTrigger(hour=1, minute=28),
     CronTrigger(hour=1, minute=58),
     CronTrigger(hour=2, minute=28),
     CronTrigger(hour=2, minute=58),
     CronTrigger(hour=3, minute=28),
     CronTrigger(hour=3, minute=58),
     CronTrigger(hour=4, minute=28),
     CronTrigger(hour=4, minute=58),
     CronTrigger(hour=5, minute=28),
     CronTrigger(hour=5, minute=58),
     CronTrigger(hour=6, minute=28),
     CronTrigger(hour=6, minute=58),
     CronTrigger(hour=6, minute=5),  # todo remove
     CronTrigger(hour=6, minute=7),  # todo remove
     CronTrigger(hour=7, minute=28),
     CronTrigger(hour=7, minute=58),
     CronTrigger(hour=8, minute=28),
     CronTrigger(hour=8, minute=58),
     CronTrigger(hour=9, minute=28),
     CronTrigger(hour=9, minute=58),
     CronTrigger(hour=10, minute=28),
     CronTrigger(hour=10, minute=58),
     CronTrigger(hour=11, minute=28),
     CronTrigger(hour=11, minute=58),
     CronTrigger(hour=12, minute=28),
     CronTrigger(hour=12, minute=58),
     CronTrigger(hour=13, minute=28),
     CronTrigger(hour=13, minute=58),
     CronTrigger(hour=14, minute=28),
     CronTrigger(hour=14, minute=58),
     CronTrigger(hour=15, minute=28),
     CronTrigger(hour=15, minute=58),
     CronTrigger(hour=16, minute=28),
     CronTrigger(hour=16, minute=58),
     CronTrigger(hour=17, minute=28),
     CronTrigger(hour=17, minute=58),
     CronTrigger(hour=18, minute=28),
     CronTrigger(hour=18, minute=58),
     CronTrigger(hour=19, minute=28),
     CronTrigger(hour=19, minute=58),
     CronTrigger(hour=20, minute=28),
     CronTrigger(hour=20, minute=58),
     CronTrigger(hour=21, minute=28),
     CronTrigger(hour=21, minute=58),
     CronTrigger(hour=22, minute=28),
     CronTrigger(hour=22, minute=58),
     CronTrigger(hour=23, minute=28),
     CronTrigger(hour=23, minute=58)])

# run.generate_and_send_report() function creates from db data reports and send them to the (TELEGRAM_CHAT_ID) chat
# once an hour
telegram_report_trigger = OrTrigger(
    [CronTrigger(hour=0),
     CronTrigger(hour=1),
     CronTrigger(hour=2),
     CronTrigger(hour=3),
     CronTrigger(hour=4),
     CronTrigger(hour=5),
     CronTrigger(hour=6),
     CronTrigger(hour=6, minute=6),  # todo remove
     CronTrigger(hour=6, minute=8),  # todo remove
     CronTrigger(hour=7),
     CronTrigger(hour=8),
     CronTrigger(hour=9),
     CronTrigger(hour=10),
     CronTrigger(hour=11),
     CronTrigger(hour=12),
     CronTrigger(hour=13),
     CronTrigger(hour=14),
     CronTrigger(hour=15),
     CronTrigger(hour=16),
     CronTrigger(hour=17),
     CronTrigger(hour=18),
     CronTrigger(hour=19),
     CronTrigger(hour=20),
     CronTrigger(hour=21),
     CronTrigger(hour=22),
     CronTrigger(hour=23)])
