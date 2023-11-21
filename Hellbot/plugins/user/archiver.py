import os
import time
import zipfile

from pyrogram.types import Message

from Hellbot.functions.formatter import readable_time
from Hellbot.functions.tools import get_files_from_directory, progress

from . import HelpMenu, hellbot, on_message


@on_message("zip", allow_stan=True)
async def zip_files(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a message to zip it.")

    media = message.reply_to_message.media
    if not media:
        return await hellbot.delete(message, "Reply to a media message to zip it.")

    hell = await hellbot.edit(message, "`Zipping...`")
    start = time.time()
    download_path = await message.reply_to_message.download(
        f"temp_{round(time.time())}",
        progress=progress,
        progress_args=(hell, start, "📦 Zipping"),
    )

    with zipfile.ZipFile(download_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(download_path)

    await hellbot.delete(hell, "Zipped Successfully.")
    await message.reply_document(
        download_path + ".zip",
        caption=f"**Zipped in {readable_time(time.time() - start)}.**",
        progress=progress,
        progress_args=(hell, start, "⬆️ Uploading"),
    )

    os.remove(download_path + ".zip")
    os.remove(download_path)


@on_message("unzip", allow_stan=True)
async def unzip_file(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a message to unzip it.")

    media = message.reply_to_message.media
    if not media:
        return await hellbot.delete(message, "Reply to a media message to unzip it.")

    hell = await hellbot.edit(message, "`Unzipping...`")
    start = time.time()
    download_path = await message.reply_to_message.download(
        f"temp_{round(time.time())}",
        progress=progress,
        progress_args=(hell, start, "📦 Unzipping"),
    )

    with zipfile.ZipFile(download_path, "r") as zip_file:
        zip_file.extractall(download_path)

    await hellbot.delete(hell, "Unzipped Successfully.")
    files = await get_files_from_directory(download_path)

    for file in files:
        if os.path.exists(file):
            try:
                await message.reply_document(
                    file,
                    caption=f"**Unzipped {os.path.basename(file)}.**",
                    force_document=True,
                    progress=progress,
                    progress_args=(hell, start, "⬆️ Uploading"),
                )
            except Exception as e:
                await message.reply_text(f"**{file}:** `{e}`")
                continue
            os.remove(file)

    os.remove(download_path)


HelpMenu("archiver").add(
    "zip", "<reply to a media>", "Zip the replied media and upload it in the chat."
).add(
    "unzip", "<reply to a zip file>", "Unzip the replied zip file and upload it in the chat.",
).info(
    "Manage Archives"
).done()
