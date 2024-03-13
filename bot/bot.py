# -*- coding: utf-8 -*-
"""
TELEGRAM BOT

The only command is /start. After that the only way it interacts - through sending report messages.
"""
import datetime
import logging
import telebot
from settings import TELEGRAM_API_KEY, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

# initializing Telegram bot
bot = telebot.TeleBot(TELEGRAM_API_KEY)


@bot.message_handler(commands=['start'])
def start_command(message):
    """ Responds to the /start command """
    welcome_message = "Welcome to the TotalDistributionBot!\nHottest AIX TotalDistribution statistics every 4 hours."
    bot.send_message(message.chat.id, welcome_message)


def send_report(report):
    """ Just sends a prepared report to chat """
    bot.send_message(TELEGRAM_CHAT_ID, report, parse_mode='MarkdownV2')
    logger.info(f"Report at {datetime.datetime.now()} was sent:\n{report}\n")
