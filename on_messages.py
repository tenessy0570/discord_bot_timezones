from utils import (
    in_bot_channel,
    send_timezones_to_channel
)
from decorators import author_is_not_bot


class Messages:
    @author_is_not_bot
    async def on_message(self, message):
        if not in_bot_channel(message=message):
            return

        if message.content.startswith('!time'):
            await message.channel.send("Отправляю время...")
            await send_timezones_to_channel(message)
