import environment_vars
from os import environ
from discord import Intents
from common_client_class_to_run import Client

bot_token = environ.get('bot_token')

client = Client(intents=Intents.all())
client.run(bot_token)
