from aiogram.filters import Command
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from modules import *
from models.user import User
from templates.messages import BotMessages
from services.gas_client import GASExceptionError
from services.income_service import IncomeService
from templates.keyboards import get_periods_keyboard

router = Router()

class IncomeStates(StatesGroup):
    WAITING_FOR_PERIOD = State()
    WAITING_FOR_INCOME = State()

@router.message(Command('report_income'))
async def cmd_report_income(message: types.Message, state: FSMContext):
    '''Initiates the income entry process'''
    if User.get_session(message.from_user.id):
        await message.answer(BotMessages.INCOME['start'], parse_mode='HTML', reply_markup=get_periods_keyboard())
        await state.set_state(IncomeStates.WAITING_FOR_PERIOD)
    else:
        await message.answer(BotMessages.ERROR['authorized'])

@router.callback_query(IncomeStates.WAITING_FOR_PERIOD, F.data.startswith('period_'))
async def proccess_period_selection(callback: types.CallbackQuery, state: FSMContext):
    '''Handles period selection'''
    period = callback.data.replace('period_', '')
    await state.update_data(period=period)
    await callback.message.answer(BotMessages.INCOME['enter_amount'].format(period=period), parse_mode='HTML')
    await state.set_state(IncomeStates.WAITING_FOR_INCOME)
    await callback.answer()

@router.message(IncomeStates.WAITING_FOR_INCOME, F.text)
async def proccess_report_income(message: types.Message, state: FSMContext):
    '''Processes the entered income amount'''
    try:
        amount = float(message.text.replace(',', '.'))
        if amount <= 0: raise ValueError

        period = (await state.get_data()).get('period', 'неизвестный период')
        payment = await IncomeService.update_income(message.from_user.id, period, amount)

        if user := User.get_session(message.from_user.id):
            user.last_payment = payment.get('lastPayment')
            user.store_session()

        logger.info(f'The user ({user.telegram_id}) entered the income amount ({user.last_payment['amount']}) ' \
                    f'for the period ({user.last_payment['date']})')
        await message.answer(BotMessages.INCOME['success'].format(amount=amount, period=period), parse_mode='HTML')
    except ValueError:
        await message.answer(BotMessages.ERROR['invalid_amount'])
    except GASExceptionError as e:
        await e.notify_user(message)
    except Exception as e:
        logger.error(f'Report income error: {e}')
        await message.answer(BotMessages.ERROR['system_error'])
    finally:
        await state.clear()