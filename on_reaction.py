from utils import (
    reacted_user_is_bot,
    in_bot_channel,
    get_role_from_payload,
    get_reacted_user
)


class Reactions:
    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        if await reacted_user_is_bot(self, payload) or await in_bot_channel(channel=channel):
            return

        role = await get_role_from_payload(self, payload, channel)
        await payload.member.add_roles(role)

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        if await reacted_user_is_bot(self, payload) or await in_bot_channel(channel=channel):
            return

        role = await get_role_from_payload(self, payload, channel)
        reacted_user = await get_reacted_user(self, payload)

        await reacted_user.remove_roles(role)
