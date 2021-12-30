from youtubesearchpython import VideosSearch


def on_ready_print(self):
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


def message_is_song_name(message):
    return message.content.split(' ')[0] == '!song'


def _get_song_name_from_message(message):
    parsed_msg = message.content.split(' ')
    if len(parsed_msg) == 1:
        raise NameError("Song name can't be empty!")
    return ''.join(parsed_msg[1:])


def _get_movie_id(videos_search):
    return videos_search.result()['result'][0]['id']


def get_video_url_by_song_name(message):
    url = 'https://www.youtube.com/watch?v='
    song_name = _get_song_name_from_message(message)
    videos_search = VideosSearch(song_name, limit=1)
    video_id = _get_movie_id(videos_search)
    return url + video_id
