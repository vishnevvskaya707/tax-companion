from aiogram.filters import Command
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from modules import *
from models.user import User
from templates.messages import BotMessages
from services.auth_service import AuthService
from services.gas_client import GASExceptionError

router = Router()

class AuthStates(StatesGroup):
    WAITING_FOR_ACCESS_CODE = State()
    AUTHORIZED = State()

@router.message(Command('login'))
async def cmd_login(message: types.Message, state: FSMContext):
    '''Sends a welcome message for the bot'''
    try:
        if user := User.get_session(message.from_user.id):
            await state.set_state(AuthStates.AUTHORIZED)
            await message.answer(BotMessages.AUTH['welcome'].format(full_name=user.full_name))
            return
        if await AuthService.check_user_exists(message.from_user.id):
            await message.answer(BotMessages.AUTH['enter_code'])
            await state.set_state(AuthStates.WAITING_FOR_ACCESS_CODE)
        else:
            await message.answer(BotMessages.ERROR['not_user'])
    except GASExceptionError as e:
        await e.notify_user(message)
    except Exception as e:
        logger.error(f'Start login error: {e}')
        await message.answer(BotMessages.ERROR['system_error'])

@router.message(AuthStates.WAITING_FOR_ACCESS_CODE, F.text)
async def process_access_code(message: types.Message, state: FSMContext):
    '''Checks access code via GAS'''
    try:
        if data := await AuthService.activate_user(message.from_user.id, message.text.strip()):
            user = User(message.from_user.id, 
                        data['user']['fullName'], 
                        data['user']['birthDate'], 
                        data['user']['email'], 
                        data.get('lastPayment'))
            user.store_session()
            await state.update_data(user=user)
            await state.set_state(AuthStates.AUTHORIZED)
            await message.answer(BotMessages.AUTH['success'].format(full_name=user.full_name))
            logger.info(f'User ({user.telegram_id}) successfully authorized in system')
        else:
            await message.answer(BotMessages.ERROR['invalid_code'])
    except GASExceptionError as e:
        await e.notify_user(message)
    except Exception as e:
        logger.error(f'Proccess login error: {e}')
        await message.answer(BotMessages.ERROR['system_error'])

@router.message(Command('logout'))
async def cmd_logout(message: types.Message, state: FSMContext):
    '''Clears user session'''
    try:
        if user := User.get_session(message.from_user.id):
            User.get_redis_connection().delete(f'user:{user.telegram_id}')
            await AuthService.deactivate_user(user.telegram_id)
        
            await state.clear()
            await message.answer(BotMessages.AUTH['exit'])
            logger.info(f'User ({user.telegram_id}) successfully logout')
        else:
            await message.answer(BotMessages.ERROR['authorized'])
    except GASExceptionError as e:
        await e.notify_user(message)
    except Exception as e:
        logger.error(f'Logout error: {e}')
        await message.answer(BotMessages.ERROR['system_error'])

@router.message(Command('info'))
async def cmd_info(message: types.Message):
    '''Displays user information'''
    try:
        if user := User.get_session(message.from_user.id):
            message_text = BotMessages.AUTH['user_info'].format(
                full_name=user.full_name,
                email=user.email
            )
            if hasattr(user, 'last_payment') and user.last_payment:
                message_text += BotMessages.AUTH['payment_info'].format(
                    amount=user.last_payment['amount'],
                    date=BotMessages.format_date(user.last_payment['date'])
                )
            await message.answer(message_text, parse_mode='HTML')
        else:
            await message.answer(BotMessages.ERROR['authorized'])
    except Exception as e:
        logger.error(f'Dislpay info error: {e}')
        await message.answer(BotMessages.ERROR['system_error'])