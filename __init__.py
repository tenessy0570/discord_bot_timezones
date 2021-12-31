import environment_vars
import discord
from os import environ
from img_urls import good_face_url
from decorators import (
    author_is_not_bot,
    notify_if_wrong_command
)
from utils import (
    on_ready_print,
    receive_message_then_send,
    get_commands_from_file,
    message_is_song_name,
    get_video_url_by_song_name,
    get_embed,
    get_commands_list_to_send,
    in_bot_channel,
    create_message_and_add_reactions,
    create_and_get_roles_dict,
    get_roles_for_send,
    get_role_from_payload,
    reacted_user_is_bot,
    get_on_delete_content
)


class MyClient(discord.Client):
    _help_commands = get_commands_from_file("commands_list_divided_with_newline")
    _help_commands_for_output = ('~ ' + command for command in _help_commands)
    _help_commands_for_output = '\n'.join(_help_commands_for_output)

    _emojis = {
        ":smiling_face_with_3_hearts:": u"\U0001F970",
        ":train:": u"\U0001F68B",
        ":kimono:": u"\U0001F458"
    }

    _roles = create_and_get_roles_dict(_emojis)

    async def on_ready(self):
        await on_ready_print(self)
        _channel = None

        for channel in self.get_all_channels():
            if channel.name != 'bot':
                _channel = channel

        _roles_for_send = await get_roles_for_send(self)
        await create_message_and_add_reactions(self, _channel, _roles_for_send)

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
            except (NameError, discord.errors.HTTPException):
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

    async def on_raw_reaction_add(self, payload):
        if await reacted_user_is_bot(self, payload):
            return

        channel = self.get_channel(payload.channel_id)
        if await in_bot_channel(channel=channel):
            return

        role = await get_role_from_payload(self, payload, channel)
        await payload.member.add_roles(role)


bot_token = environ.get('bot_token')
client = MyClient()
client.run(bot_token)
