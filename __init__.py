import discord
from os import environ
import environment_vars
from decorators import author_is_not_bot
from img_urls import good_face_url
from utils import on_ready_print, receive_message_then_send, get_commands_from_file


class MyClient(discord.Client):
    _help_commands = get_commands_from_file("commands_list_divided_with_newline")
    _help_commands_for_output = ('~ ' + command for command in _help_commands)
    _help_commands_for_output = '\n'.join(_help_commands_for_output)

    async def on_ready(self):
        on_ready_print(self)

    @author_is_not_bot
    async def on_message(self, message):
        if await receive_message_then_send(message, "ping", "pong"):
            return

        if await receive_message_then_send(message, "!help"):
            await message.channel.send("Available commands: \n" + self._help_commands_for_output)
            return

        if message.attachments:
            await message.delete()
            await message.channel.send('No attachments! :)')
            return

        if await receive_message_then_send(message, "face"):
            image_to_send = discord.Embed().set_image(url=good_face_url)
            await message.channel.send(embed=image_to_send)
            return

        await message.channel.send('I cant understand you :(\nType !help for available command list')
        return


bot_token = environ.get('bot_token')
client = MyClient()
client.run(bot_token)
