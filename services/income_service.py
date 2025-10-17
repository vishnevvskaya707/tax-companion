from aiogram import types

from .gas_client import GASClient, GASExceptionError
from modules import *

class IncomeService:

    @staticmethod
    async def update_income(telegram_id, period, amount):
        response = GASClient.make_request({
            'action': 'update_income',
            'telegramId': telegram_id,
            'period': period,
            'amount': amount
        })
        if not response.get('success'):
            logger.error(f'Income input error (id - {telegram_id}): {response.get('error') or 'Unknown error'}')
            raise GASExceptionError()
        return response