import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types

from modules import *
from handlers.auth import router as auth_router
from handlers.income import router as income_router
from services.notification_sender import NotificationSender

load_dotenv()

bot = Bot(token=Config.TELEGRAM_TOKEN)
dp = Dispatcher()

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='login', description='Вход в систему'),
        types.BotCommand(command='info', description='Персональная информация'),
        types.BotCommand(command='logout', description='Выход из системы'),
        types.BotCommand(command='report_income', description='Ввод суммы дохода'),
        types.BotCommand(command='help', description='Помощь'),
    ]
    await bot.set_my_commands(commands)

async def on_startup(bot: Bot):
    await set_commands(bot)
    notification_sender = NotificationSender(bot)
    asyncio.create_task(notification_sender.send_sheduled_notifications())
    logger.info('Sheduled notifications started')

async def main():
    try:
        logger.info('Bot launched successfully')
        dp.include_router(auth_router)
        dp.include_router(income_router)
        dp.startup.register(on_startup)

        await dp.start_polling(bot)
    except Exception as e:
        logger.error('Error starting bot: ', e)
    finally:
        logger.info('Bot stopped')

if __name__ == '__main__':
    asyncio.run(main())