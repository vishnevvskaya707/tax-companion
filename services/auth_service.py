from modules import *
from .gas_client import GASClient, GASExceptionError

class AuthService:
    '''
    Service handling user authentication operations through GAS (Google Apps Script) API
    '''
    
    @staticmethod
    async def check_user_exists(telegram_id):
        response = GASClient.make_request({
            'action': 'check_user',
            'telegramId': telegram_id
        })
        if not response.get('success'):
            logger.error(f'Check user error (id - {telegram_id}): {response.get('error') or 'Unknown error'}')
            raise GASExceptionError()
        return response
    
    @staticmethod
    async def activate_user(telegram_id, access_code):
        response = GASClient.make_request({
            'action': 'activate',
            'telegramId': telegram_id,
            'accessCode': access_code
        })
        if not response.get('success'):
            logger.error(f'Activate user error (id - {telegram_id}): {response.get('error') or 'Unknown error'}')
            raise GASExceptionError()
        return response
    
    @staticmethod
    async def deactivate_user(telegram_id):
        response = GASClient.make_request({
            'action': 'deactivate',
            'telegramId': telegram_id
        })
        if not response.get('success'):
            logger.error(f'Deactivate user error (id - {telegram_id}): {response.get('error') or 'Unknown error'}')