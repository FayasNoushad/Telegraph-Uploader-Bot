import os
import logging
from telegraph import upload_file
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from config import Config
from pyrogram.types import InputMediaPhoto

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable for the Force Sub Channel (numeric ID)
force_sub_channel = '-1001234567890'  # Replace with your channel's numeric ID

# Variable for authorized users (bot owner IDs)
AUTH_USERS = [6974737899]  # Replace with actual user IDs

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "downloads/telegraphbot.jpg")

START_TEXT = """👋 Hello {},

I am an under 5MB media or file to telegra.ph link uploader bot.

Made With ❤️‍🔥 by @Moviez_Botz"""

HELP_TEXT = """**About Me**

- Just give me a media under 5MB
- Then I will download it
- I will then upload it to the telegra.ph link

Made With ❤️‍🔥 by @Moviez_Botz
"""

ABOUT_TEXT = """**About Me**

- **Bot :** `Telegraph Uploader`
- **Developer :** @Moviez_Botz
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""

AJAS_TEXT = """👋 hey, iam 𝗣𝗔𝗟𝗔𝗞𝗚𝗔𝗟 𝗔𝗝𝗔𝗦,

Dont be oversmart infront of me🤬

❌ You still need to join our channel to use the bot. Please join the channel and click 'I Subscribed ✅' again."""


START_BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('📢 UPDATES CHANNEL', url='https://telegram.me/moviez_botz')],
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

async def force_sub(bot, message):
    try:
        logger.info(f"Checking if user is a member of the channel with ID: {force_sub_channel}")
        user = await bot.get_chat_member(force_sub_channel, message.from_user.id)

        # If the user is already a member, allow access
        if user.status in ["member", "administrator", "creator"]:
            return True
    except UserNotParticipant:
        pass  # User is not a participant, proceed to send the subscription message
    except ChatAdminRequired:
        await message.reply_text("❌ I need to be an admin in the channel to generate an invite link.")
        return False
    except Exception as e:
        logger.error(f"Error in force_sub: {e}")
        await message.reply_text(
            text=f"An error occurred: {e}"
        )
        return False

    # If the user is not subscribed, send the force subscription message
    try:
        invite_link = await bot.export_chat_invite_link(force_sub_channel)
    except ChatAdminRequired:
        await message.reply_text("❌ I need to be an admin in the channel to generate an invite link.")
        return False

    # Send a message with a "Check Subscription" button
    await message.reply_text(
        text=f"❌ To use this bot, you must join [our channel]({invite_link}) first.",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('Join Channel', url=invite_link)],
                [InlineKeyboardButton('✅ I Subscribed', callback_data='check_subscription')]
            ]
        )
    )
    return False

@Bot.on_message(filters.private & filters.command("set_fsub"))
async def set_fsub(bot, message: Message):
    global force_sub_channel  # Reference the global variable
    
    # Check if the user is authorized (e.g., bot owner or admin)
    if message.from_user.id not in AUTH_USERS:
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    
    # Get the new channel from the command arguments
    new_channel = message.text.split(" ", 1)[1].strip()
    if not new_channel:
        await message.reply_text("❌ Please provide a valid channel username.")
        return
    
    # Update the force_sub_channel variable
    force_sub_channel = new_channel
    await message.reply_text(f"✅ Force subscription channel updated to: @{force_sub_channel}")


@Bot.on_message(filters.private & filters.command("info"))
async def user_info(bot, message: Message):
    user = message.from_user
    user_info_text = f"""
**User Info:**
- **User ID:** `{user.id}`
- **First Name:** `{user.first_name}`
- **Last Name:** `{user.last_name or 'N/A'}`
- **Username:** `{user.username or 'N/A'}`
- **Language Code:** `{user.language_code}`
"""
    
    await message.reply_text(user_info_text)


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
    elif update.data == "check_subscription":
        # Recheck if the user is now subscribed
        if await force_sub(bot, update.message):
            await update.message.edit_text(
                text="✅ Thank you for subscribing! You can now use the bot.",
                disable_web_page_preview=True,
                reply_markup=START_BUTTONS
            )
        else:
            # Send an alternate message with a photo if the user hasn't joined the channel
            await update.message.edit_media(
                media=InputMediaPhoto(
                    media="https://telegra.ph/file/ca1420ca5bd8f6943f0e4.jpg",  # Replace with a link to the actual image you want to send
                    caption=AJAS_TEXT,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('Join Channel', url=await bot.export_chat_invite_link(force_sub_channel))],
                        [InlineKeyboardButton('✅ I Subscribed', callback_data='check_subscription')]
                    ]
                )
            )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await force_sub(bot, update):
        return
    
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        quote=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & (filters.media | filters.command(["upload", "other_command"])))
async def getmedia(bot, message: Message):
    if not await force_sub(bot, message):
        return
    
    message_id = message.message_id
    medianame = DOWNLOAD_LOCATION + str(message_id)
    
    try:
        processing_message = await message.reply_text(
            text="`Processing...`",
            disable_web_page_preview=True
        )
        await message.download(file_name=medianame)
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
        await processing_message.edit_text(
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
                InlineKeyboardButton(text="🔰 JOIN UPDATES CHANNEL 🔰", url=f"https://t.me/{force_sub_channel}")
            ]
        ]
    )
    
    await processing_message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


Bot.run()
