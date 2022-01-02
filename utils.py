import discord
from youtubesearchpython import VideosSearch


async def on_ready_print(self):
    print("---------")
    print("Logged as")
    print(self.user.name)
    print(self.user.id)
    print("---------")


async def receive_message_then_send(message, received: str, to_send=""):
    if message.content == received:
        if to_send:
            await message.channel.send(to_send)
        return True


def get_commands_from_file(filename: str) -> tuple:
    with open(filename, 'r') as file:
        _help_commands = tuple((command.split('\n')[0] for command in file))
    return _help_commands


async def message_is_video_name(message):
    return message.content.split(' ')[0] == '!song'


async def _get_video_name_from_message(message):
    parsed_msg_list = message.content.split(' ')
    song_name = ' '.join(parsed_msg_list[1:])

    if not song_name:
        raise NameError("Song name can't be empty!")

    return song_name


async def _get_movie_id(video_name):
    videos_search = VideosSearch(video_name, limit=1)
    return videos_search.result()['result'][0]['id']


async def get_video_url_by_name(message):
    url = 'https://www.youtube.com/watch?v='
    video_name = await _get_video_name_from_message(message)

    if not video_name:
        raise NameError

    try:
        video_id = await _get_movie_id(video_name)
    except IndexError:
        raise NameError

    return url + video_id


async def get_embed(url):
    return discord.Embed().set_image(url=url)


async def get_commands_list_to_send(self):
    return "Available commands: \n" + self._help_commands_for_output


async def is_embed(message):
    return message.content == ""


async def in_bot_channel(channel=None, message=None):
    if message:
        channel = message.channel
    return channel.name == 'bot'


async def get_message_by_id(channel, message_id):
    return await discord.GroupChannel.fetch_message(self=channel, id=message_id)


async def _get_reaction_info(self, payload):
    guild = self.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    return payload.emoji, member, payload.message_id


async def create_message_and_add_reactions(self, _channel, _roles_for_send):
    message = await _channel.send(_roles_for_send)
    for key in self._emojis:
        await message.add_reaction(emoji=self._emojis[key])


def create_and_get_roles_dict(_emojis):
    _roles = {}

    for key, i in zip(_emojis, range(1, len(_emojis) + 1)):
        _roles[_emojis[key]] = f"Role {i}"

    return _roles


async def get_roles_for_send(self):
    roles = ""
    for key, value in self._roles.items():
        role_name = value
        role = await _get_role_by_name(self, role_name)
        roles += f"{key} ~ <@&{role.id}>\n"
    return roles


async def _get_role_by_name(self, name):
    return discord.utils.get(self.guilds[0].roles, name=name)


async def get_role_from_payload(self, payload, channel):
    emoji, reacted_user, message_id = await _get_reaction_info(self, payload)
    guild = channel.guild
    emoji = emoji.name.lower()
    role = discord.utils.get(guild.roles, name=self._roles[emoji])
    return role


async def reacted_user_is_bot(self, payload):
    return payload.member == self.user


async def get_on_delete_content(message):
    return f'"{message.content}"' \
            if not await is_embed(message) \
            else 'just an embed or an image.'


async def get_reacted_user(self, payload):
    guild = self.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    return user
