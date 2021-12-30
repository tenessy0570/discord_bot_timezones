def author_is_not_bot(func):
    async def wrapper(self, message, *args, **kwargs):
        if message.author == self.user:
            return None
        return await func(self, message, *args, **kwargs)
    return wrapper


def notify_if_wrong_command(func):
    async def wrapper(self, message, *args, **kwargs):
        function_return = func(self, message, *args, **kwargs)
        if await function_return:
            await message.channel.send('I cant understand you :(\nType !help for available command list')
    return wrapper
