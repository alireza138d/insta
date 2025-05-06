import logging
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '7564121742:AAFdvksrJO35qfJpj8nL9G6gWw2bxtHzl18'  # جایگزین کن با توکن ربات خود
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

L = instaloader.Instaloader()

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)

async def send_media(message: types.Message, media_url: str):
    if media_url.endswith('.mp4'):
        await message.answer_video(media_url)
    else:
        await message.answer_photo(media_url)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("سلام! من ربات دانلودر اینستاگرام هستم.\nلطفا لینک پست، ریلز یا IGTV اینستاگرام را ارسال کن.")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def download_instagram_media(message: types.Message):
    url = message.text.strip()

    if "instagram.com" not in url:
        await message.reply("لطفا یک لینک معتبر اینستاگرام ارسال کنید.")
        return

    try:
        # استخراج shortcode
        shortcode = url.split('/p/')[1].split('/')[0] if "/p/" in url else None
        if not shortcode:
            await message.reply("فرمت لینک اشتباه است.")
            return

        # دانلود پست
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        media_url = post.url

        # ارسال مدیا به کاربر
        await send_media(message, media_url)

    except Exception as e:
        await message.reply(f"خطا در دانلود محتوا: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
