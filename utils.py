def on_ready_print(self):
    print("---------")
    print("Logged as")
    print(self.user.name)
    print(self.user.id)
    print("---------")


async def receive_message_then_send(message, received: str, to_send="") -> None:
    if message.content == received:
        if to_send:
            await message.channel.send(to_send)
        return True


def get_commands_from_file(filename: str) -> tuple:
    with open(filename, 'r') as file:
        _help_commands = tuple((command.split('\n')[0] for command in file))
    return _help_commands
