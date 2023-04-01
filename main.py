import cv2
import pytesseract
import numpy as np
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor


# Initialize the Telegram bot
BOT_TOKEN = ""
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

 
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Change this to your Tesseract installation path
pytesseract_config = '--psm 6' 


@dp.message_handler(content_types=ContentType.TEXT)
@dp.message_handler(commands=['start',])
async def handle_photo(message: types.Message):
    print(f"Started to use: {message.from_user.full_name} - {message.from_user.id}")
    await message.reply(f"hi {message.from_user.full_name}. I can convert texts in images to simple text. Send me text photo")


@dp.message_handler(content_types=[ContentType.PHOTO])
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    photo_file = await bot.download_file_by_id(photo.file_id)
    
    photo_bytes = photo_file.read()
    photo_arr = np.asarray(bytearray(photo_bytes), dtype=np.uint8)
    photo_np = cv2.imdecode(photo_arr, cv2.IMREAD_GRAYSCALE)
    
    text = pytesseract.image_to_string(photo_np, config=pytesseract_config)
    
    await message.reply(text)

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp)