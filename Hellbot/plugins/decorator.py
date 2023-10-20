from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from Hellbot.core import Config, hellbot
from Hellbot.functions.admins import is_user_admin

from .utils import edit_or_reply


def on_message(
    command: list = None,
    group: int = 0,
    chat_type: ChatType = None,
    admin_only: bool = False,
    allow_sudo: bool = False,
    help_dict: dict = None,
):
    if allow_sudo:
        _filter = (
            filters.command(command, Config.HANDLERS)
            & (filters.me | Config.SUDO_USERS)
            & ~filters.forwarded
            & ~filters.via_bot
        )
    else:
        _filter = (
            filters.command(command, Config.SUDO_USERS)
            & filters.me
            & ~filters.forwarded
            & ~filters.via_bot
        )

    # add command help
    # todo

    def decorator(func):
        async def wrapper(client: Client, message: Message):
            client.eor = edit_or_reply
            if admin_only and not await is_user_admin(message, client.me.id):
                await client.eor(message, "I am not admin here!")
                return

            if chat_type and message.chat.type != chat_type:
                await client.eor(
                    message, f"Use this command in {chat_type.value} only!"
                )
                return

            await func(client, message)

        for user in hellbot.users:
            user.add_handler(MessageHandler(wrapper, _filter), group)

        return wrapper

    return decorator
