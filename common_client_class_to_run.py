from discord import Client as ClientToInherit
from on_messages import Messages


class Client(ClientToInherit, Messages):
    pass
