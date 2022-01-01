from discord import Client as ClientToInherit
from on_messages import Messages
from on_ready import Ready
from on_reaction import Reactions


class Client(ClientToInherit, Ready, Messages, Reactions):
    pass
