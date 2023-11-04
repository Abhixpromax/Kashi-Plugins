from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from Hellbot.core import Config, Symbols, hellbot

from .. import COMMAND_MENU_TEXT, HELP_MENU_TEXT
from ..btnsG import gen_inline_help_buttons


async def check_auth_click(cb: CallbackQuery) -> bool:
    if cb.from_user.id not in Config.AUTH_USERS:
        await cb.answer(
            "You are not authorized to use this bot. \n\n</> @Its_HellBot",
            show_alert=True,
        )
        return False
    return True


@hellbot.bot.on_callback_query(filters.regex(r"auth_close"))
async def auth_close_cb(_, cb: CallbackQuery):
    if await check_auth_click(cb):
        await cb.message.delete()


@hellbot.bot.on_callback_query(filters.regex(r"close"))
async def close_cb(_, cb: CallbackQuery):
    await cb.message.delete()


@hellbot.bot.on_callback_query(filters.regex(r"help_page"))
async def help_page_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    page = int(cb.data.split(":")[1])
    buttons, max_page = await gen_inline_help_buttons(page, sorted(Config.CMD_MENU))

    await cb.edit_message_text(
        HELP_MENU_TEXT.format(
            cb.from_user.mention,
            len(Config.CMD_MENU),
            len(Config.CMD_INFO),
            page + 1,
            max_page,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@hellbot.bot.on_callback_query(filters.regex(r"help_menu"))
async def help_menu_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    page = int(cb.data.split(":")[1])
    plugin = str(cb.data.split(":")[2])

    try:
        buttons = [
            InlineKeyboardButton(
                f"{Symbols.bullet} {i}", f"help_cmd:{page}:{plugin}:{i}"
            )
            for i in sorted(Config.HELP_DICT[plugin]["commands"])
        ]
    except KeyError:
        await cb.answer("No description provided for this plugin!", show_alert=True)
        return

    buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    buttons.append([InlineKeyboardButton(Symbols.back, f"help_page:{page}")])

    await cb.edit_message_text(
        COMMAND_MENU_TEXT.format(
            plugin,
            Config.HELP_DICT[plugin]["info"],
            len(sorted(Config.HELP_DICT[plugin]["commands"])),
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@hellbot.bot.on_callback_query(filters.regex(r"help_cmd"))
async def help_cmd_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    page = int(cb.data.split(":")[1])
    plugin = str(cb.data.split(":")[2])
    command = str(cb.data.split(":")[3])
    result = ""
    cmd_dict = Config.HELP_DICT[plugin]["commands"][command]

    if cmd_dict["parameters"] is None:
        result += f"**{Symbols.radio_select} 𝖢𝗈𝗆𝗆𝖺𝗇𝖽:** `{Config.HANDLERS[0]}{cmd_dict['command']}`"
    else:
        result += f"**{Symbols.radio_select} 𝖢𝗈𝗆𝗆𝖺𝗇𝖽:** `{Config.HANDLERS[0]}{cmd_dict['command']} {cmd_dict['parameters']}`"

    if cmd_dict["description"]:
        result += (
            f"\n\n**{Symbols.arrow_right} 𝖣𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇:** __{cmd_dict['description']}__"
        )

    if cmd_dict["example"]:
        result += f"\n\n**{Symbols.arrow_right} 𝖤𝗑𝖺𝗆𝗉𝗅𝖾:** `{Config.HANDLERS[0]}{cmd_dict['example']}`"

    if cmd_dict["note"]:
        result += f"\n\n**{Symbols.arrow_right} 𝖭𝗈𝗍𝖾:** __{cmd_dict['note']}__"

    result += f"\n\n**<\> @Its_HellBot 🍀**"

    buttons = [
        [
            InlineKeyboardButton(Symbols.back, f"help_menu:{page}:{plugin}"),
            InlineKeyboardButton(Symbols.close, "help_close:close"),
        ]
    ]

    await cb.edit_message_text(
        result,
        ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@hellbot.bot.on_callback_query(filters.regex(r"help_close"))
async def help_close_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    action = str(cb.data.split(":")[1])
    if action == "close":
        await cb.edit_message_text(
            "**𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎 𝖢𝗅𝗈𝗌𝖾𝖽!**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Reopen Menu", "help_close:reopen")]]
            ),
        )
    elif action == "reopen":
        buttons, pages = await gen_inline_help_buttons(0, sorted(Config.CMD_MENU))
        await cb.edit_message_text(
            HELP_MENU_TEXT.format(
                cb.from_user.mention,
                len(Config.CMD_MENU),
                len(Config.CMD_INFO),
                1,
                pages,
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
