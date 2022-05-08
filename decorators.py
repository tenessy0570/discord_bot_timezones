def author_is_not_bot(func):
    async def wrapper(self, message, *args, **kwargs):
        if message.author == self.user:
            return None
        return await func(self, message, *args, **kwargs)
    return wrapper

