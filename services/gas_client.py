import requests 
from aiogram import types

from modules import *

class GASClient:
    '''
    Client for making requests to Google Apps Script web app
    '''
    @staticmethod
    def make_request(payload):
        try: 
            response = requests.post(
                Config.GAS_WEBAPP_URL,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f'GAS request error: {e}')
            return {'success': False, 'error': str(e)}
        
class GASExceptionError(Exception):
    '''Exception for GAS API errors'''
    def __init__(self, message='Ошибка соединения с Google Apps Script. Повторите попытку позже.'):
        self.message = message
        super().__init__(self.message)
    
    def notify_user(self, message: types.Message):
         '''Sends an error message to the user'''
         return message.answer(f'❌ {self.message}')