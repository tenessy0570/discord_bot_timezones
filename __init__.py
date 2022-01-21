from os import getenv
from dotenv import load_dotenv
from discord import Intents
from common_client_class_to_run import Client

load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")

client = Client(intents=Intents.all())
client.run(BOT_TOKEN)
