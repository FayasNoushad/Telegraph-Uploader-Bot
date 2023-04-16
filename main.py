import os
from telegraph import upload_file
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Telegraph Uploader Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")

START_TEXT = """👋 Hello {},

I am an under 5MB media or file to telegra.ph link uploader bot.

Made With ❤️‍🔥by @Movies_Botz"""

HELP_TEXT = """**About Me**

- Just give me a media under 5MB
- Then I will download it
- I will then upload it to the telegra.ph link

Made With ❤️‍🔥by @Movies_Botz
"""

ABOUT_TEXT = """**About Me**

- **Bot :** `Telegraph Uploader`
- **Developer :** @Movies_Botz
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('📢 UPDATES CHANNEL', url='https://telegram.me/movies_botz')
        ],
        [
            InlineKeyboardButton('✨ HELP', callback_data='help'),
            InlineKeyboardButton('⚠️ ABOUT', callback_data='about'),
            InlineKeyboardButton('CLOSE ⛔', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('💸 HOME', callback_data='home'),
            InlineKeyboardButton('⚠️ ABOUT', callback_data='about'),
            InlineKeyboardButton('CLOSE ⛔', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('💸 HOME', callback_data='home'),
            InlineKeyboardButton('⚠️ ABOUT', callback_data='about'),
            InlineKeyboardButton('CLOSE ⛔', callback_data='close')
        ]
    ]
)


@Bot.on_callback_query()
async def cb_data(bot, update):
    
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    
    else:
        await update.message.delete()
    

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        quote=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.media)
async def getmedia(bot, update):
    
    medianame = DOWNLOAD_LOCATION + str(update.from_user.id)
    
    try:
        message = await update.reply_message(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
        await bot.download_media(
            message=update,
            file_name=medianame
        )
        response = upload_file(medianame)
        try:
            os.remove(medianame)
        except:
            pass
    except Exception as error:
        text=f"Error :- <code>{error}</code>"
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('More Help', callback_data='help')]]
        )
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        return
    
    text=f"`https://telegra.ph{response[0]}`"
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="OPEN LINK ↗️", url=f"https://telegra.ph{response[0]}"),
                InlineKeyboardButton(text="SHARE LINK ↩️", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
            ],
            [
                InlineKeyboardButton(text="🔰 JOIN UPDATES CHANNEL 🔰", url="https://telegram.me/Movies_Botz")
            ]
        ]
    )
    
    await message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


Bot.run()
