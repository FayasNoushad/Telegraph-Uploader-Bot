import os
from pyrogram import Client, filters
from pyrogram.types import Message
from rembg import remove
from PIL import Image
from io import BytesIO

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "downloads/")

@Client.on_message(filters.private & filters.command("remove_bg"))
async def remove_bg(bot, message: Message):
    if not await force_sub(bot, message):
        return
    
    if message.photo:
        # Download the photo
        file = await message.download_media(file_name=DOWNLOAD_LOCATION + "temp.jpg")
        
        # Process the image
        input_image = Image.open(file)
        output_image = remove(input_image)
        
        # Save the result
        output_path = DOWNLOAD_LOCATION + "result.png"
        output_image.save(output_path)

        # Send the result
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=output_path,
            caption="Here is the image with the background removed."
        )

        # Clean up
        os.remove(file)
        os.remove(output_path)
    else:
        await message.reply_text("❌ Please send a photo to remove the background.")
