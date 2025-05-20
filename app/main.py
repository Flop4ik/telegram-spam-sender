from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import InviteRequestSentError, ChannelPrivateError
import time
import logging
import os

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

client = TelegramClient('anon', API_ID, API_HASH)

async def join_channel(channel_link):
    try:
        await client(JoinChannelRequest(channel_link))
        logger.info(f"Успешно присоединились: {channel_link}")
        return True
    except InviteRequestSentError:
        logger.warning(f"Запрос на вступление отправлен: {channel_link}")
        return False
    except ChannelPrivateError:
        logger.error(f"Чат приватный или недоступен: {channel_link}")
        return False
    except Exception as e:
        logger.error(f"Ошибка для {channel_link}: {str(e)}")
        return False

async def main():
    await client.start(PHONE_NUMBER)
    logger.info("Selfbot запущен!")

    with open("/home/flop4ik/GitHub/telegram-spam-sender/channels/ru-chatlinks.txt", "r", encoding="utf-8") as f:
        for line in f:
            channel_link = line.strip()
            if not channel_link:
                continue

            channel_link = f"https://{channel_link}"

            await join_channel(channel_link)
            time.sleep(2)  

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())