from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from Hellbot.core import Config, hellbot

from .. import HELP_MENU_TEXT
from ..btnsG import gen_inline_help_buttons


@hellbot.bot.on_inline_query(filters.regex(r"help_menu"))
async def help_inline(_, query: InlineQuery):
    if not query.from_user.id in Config.AUTH_USERS:
        return
    no_of_plugins = len(Config.CMD_MENU)
    no_of_commands = len(Config.CMD_INFO)
    buttons, pages = await gen_inline_help_buttons(0, sorted(Config.CMD_MENU))
    await query.answer(
        results=[
            (
                InlineQueryResultArticle(
                    "HellBot Help Menu 🍀",
                    InputTextMessageContent(
                        HELP_MENU_TEXT.format(
                            query.from_user.mention,
                            no_of_plugins,
                            no_of_commands,
                            1,
                            pages,
                        ),
                        disable_web_page_preview=True,
                    ),
                    description="Inline Query for Help Menu of HellBot",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            )
        ],
    )
