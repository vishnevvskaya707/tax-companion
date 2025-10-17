import asyncio
from aiogram import Bot
from datetime import datetime, timedelta

from modules import *
from models.user import User
from templates.messages import BotMessages
from services.gas_client import GASExceptionError
from services.holiday_service import HolidayService
from services.notification_service import NotificationService

class NotificationSender:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.holiday_service = HolidayService()
    
    async def send_sheduled_notifications(self):
        '''Send all scheduled notifications'''
        while True:
            now = datetime.now()

            if 1 <= now.day <= 3:
                await self._send_monthly_notifications()
            
            await self._send_special_occasions_notifications()
            
            await asyncio.sleep(12 * 60 * 60)
    
    async def _send_monthly_notifications(self):
        '''Monthly notifications'''
        for user in User.get_all_users():
            if user.telegram_id:
                try:
                    payment_details = await NotificationService.payment_details(user.telegram_id)
                    message = (BotMessages.build_payment_message(payment_details))
                    await self.bot.send_message(chat_id=user.telegram_id, text=message, parse_mode='HTML')

                    logger.info(f'Send monthly notifications {user.telegram_id}')
                except GASExceptionError as e:
                    logger.error(f'GAS connection error')
                except Exception as e:
                    logger.error(f'Failed send monthly notifications: {e}')
    
    async def _send_special_occasions_notifications(self):
        '''Send all special occasions notifications'''
        today = datetime.now().date()

        for user in User.get_all_users():
            if not user.telegram_id:
                return
            
            try:
                if user.birth_date:
                    date_obj = datetime.fromisoformat(user.birth_date.replace('Z', '+03:00'))
                    if date_obj.month == today.month and date_obj.day == today.day:
                        await self._send_birthday_greetings(user)

                if holiday := self.holiday_service.get_current_holiday():
                    await self._send_holiday_greetings(user, holiday)
                    logger.info(f'Users successfully congratulated on holiday')

            except GASExceptionError as e:
                logger.error(f'GAS connection error')
            except Exception as e:
                logger.error(f'Failed send special occasions notifications: {e}')
    
    async def _send_birthday_greetings(self, user):
        '''Birthday notifications'''
        await self.bot.send_message(chat_id=user.telegram_id,
                                    text=BotMessages.GREETINGS['birthday'].format(full_name=user.full_name),
                                    parse_mode='HTML')
        logger.info(f'User ({user.telegram_id}) successfully congratulated on birthday')
    
    async def _send_holiday_greetings(self, user, holiday_name):
        '''Holiday notifications'''
        await self.bot.send_message(chat_id=user.telegram_id, 
                                    text=BotMessages.GREETINGS['holiday'].format(full_name=user.full_name, holiday_name=holiday_name),
                                    parse_mode='HTML')