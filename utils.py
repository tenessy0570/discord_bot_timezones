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


async def message_is_song_name(message):
    return message.content.split(' ')[0] == '!song'


async def _get_song_name_from_message(message):
    parsed_msg_list = message.content.split(' ')
    song_name = ' '.join(parsed_msg_list[1:])

    if not song_name:
        raise NameError("Song name can't be empty!")

    return song_name


async def _get_movie_id(videos_search):
    return videos_search.result()['result'][0]['id']


async def get_video_url_by_song_name(message):
    url = 'https://www.youtube.com/watch?v='
    song_name = await _get_song_name_from_message(message)

    if song_name:
        videos_search = VideosSearch(song_name, limit=1)
    else:
        raise NameError

    try:
        video_id = await _get_movie_id(videos_search)
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


async def get_reaction_info(payload):
    return payload.emoji, payload.member, payload.message_id


async def create_message_and_add_reactions(self, _channel):
    message = await _channel.send(self._roles_for_send)
    for key in self._emojis:
        await message.add_reaction(emoji=self._emojis[key])


def create_and_get_roles_dict(_emojis):
    _roles = {}

    for key, i in zip(_emojis, range(1, len(_emojis) + 1)):
        _roles[_emojis[key]] = f"Role {i}"

    return _roles


def get_roles_for_send(_roles):
    roles = ""
    for key, value in _roles.items():
        roles += f"{key} ~ @{value}\n"
    return roles


async def get_role_from_payload(self, payload, channel):
    emoji, reacted_user, message_id = await get_reaction_info(payload)
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
