import telebot

from django.conf import settings

commands = settings.BOT_COMMANDS

bot = telebot.TeleBot(
    settings.BOT_TOKEN,
    skip_pending=True
)

bot.set_my_commands(commands)