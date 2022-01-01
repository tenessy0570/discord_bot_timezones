from discord.errors import HTTPException
from utils import (
    in_bot_channel,
    receive_message_then_send,
    get_commands_list_to_send,
    get_embed,
    message_is_song_name,
    get_video_url_by_song_name,
    get_on_delete_content
)
from img_urls import good_face_url
from decorators import (
    author_is_not_bot,
    notify_if_wrong_command
)


class Messages:
    @author_is_not_bot
    @notify_if_wrong_command
    async def on_message(self, message):
        if not await in_bot_channel(message=message):
            return

        if await receive_message_then_send(message, "ping", "pong"):
            return

        if await receive_message_then_send(message, "avatar"):
            image_to_send = await get_embed(self.user.avatar_url)
            await message.channel.send(embed=image_to_send)
            return

        if await receive_message_then_send(message, "!help"):
            await message.channel.send(await get_commands_list_to_send(self))
            return

        if message.attachments:
            await message.delete()
            await message.channel.send('No attachments! :)')
            return

        if await receive_message_then_send(message, "face"):
            image_to_send = await get_embed(url=good_face_url)
            await message.channel.send(embed=image_to_send)
            return

        if await message_is_song_name(message):

            try:
                url = await get_video_url_by_song_name(message)
            except (NameError, HTTPException):
                await message.channel.send('Bad song name!')
                return

            await message.channel.send(url)
            return

        return True

    async def on_typing(self, channel, user, when):
        if not await in_bot_channel(channel=channel):
            return

        await channel.send(f"{user.mention} started typing something on {when}. I saw it!")

    async def on_message_delete(self, message):
        if not await in_bot_channel(message=message):
            return

        message_content = await get_on_delete_content(message)

        await message.channel.send(
            f"{message.author.mention}'s message has just been deleted which was {message_content}"
        )
