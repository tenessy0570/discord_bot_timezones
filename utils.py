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
