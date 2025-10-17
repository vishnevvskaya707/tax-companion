from modules import *
from services.gas_client import GASClient, GASExceptionError

class NotificationService:

    @staticmethod
    async def payment_details(telegram_id):
        response = GASClient.make_request({
            'action': 'payment_details',
            'telegramId': telegram_id
        })
        if not response.get('success'):
            raise GASExceptionError()
        return response