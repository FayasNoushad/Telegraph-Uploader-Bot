# Made with python3
# (C) @FayasNoushad
# Copyright permission under GNU General Public License v3.0
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Telegraph-Uploader-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file

FayasNoushad = Client("Telegraph Uploader Bot", bot_token = os.environ["BOT_TOKEN"], api_id = int(os.environ["API_ID"]), api_hash = os.environ["API_HASH"])

@FayasNoushad.on_message(filters.command(["start"]))
async def start(bot, update):
    text = f"""
Hello {update.from_user.mention}, I am small media or file to telegra.ph link uploader bot.

- Just give me a media under 5MB
- Then I will download it
- I will then upload it to the telegra.ph link
"""
    reply_markup=InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/FayasNoushad'),
        InlineKeyboardButton('Feedback', url='https://telegram.me/TheFayas')
        ]]
    )
    await bot.send_message(
        chat_id=update.chat.id,
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        reply_to_message_id=update.message_id
    )

@FayasNoushad.on_message(filters.media & filters.private)
async def getmedia(bot, update):
    medianame = "./DOWNLOADS/" + "FayasNoushad/FnTelegraphBot"
    text = await bot.send_message(
        chat_id=update.chat.id,
        text="<code>Downloading to My Server ...</code>",
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
    await bot.download_media(message=update, file_name=medianame)
    await text.edit_text(text="<code>Downloading Completed. Now I'am Uploading to telegra.ph Link ...</code>")
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"Error :- {error}", disable_web_page_preview=True)
        return
    text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>Join :-</b> @FayasNoushad",
    reply_markup=InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{response[0]}"),
        InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}"),
        ],[
        InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/FayasNoushad")
        ]]
    )
    await text.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    try:
        os.remove(medianame)
    except:
        pass

FayasNoushad.run()
