import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BotMessages:
    INCOME = {
        'start': '📊 <b>Выберите период для ввода дохода:</b>',
        'enter_amount': '💰 Введите сумму дохода за <b>{period}</b>:',
        'success': '✅ Доход <b>{amount:.2f}</b> руб. за <b>{period}</b> успешно сохранён!',
    }

    AUTH = {
        'welcome': 'С возвращением, {full_name}!',
        'enter_code': 'Введите Ваш уникальный код доступа:',
        'success': '✅ Авторизация успешна!\nДобро пожаловать, {full_name}!',
        'exit': 'Вы успешно вышли из системы.',
        'user_info': (
            '👤 <b>Информация о пользователе</b>:\n\n'
            '<b>Имя</b>: {full_name};\n'
            '<b>Email</b>: {email}.'
        ),
        'payment_info': (
            '\n\n💰 <b>Последний платёж</b>:\n'
            'Сумма: {amount} руб.;\n'
            'Дата: {date}.\n'
        )
    }

    PAYMENT = {
        'monthly_notification': '📅 <b>ЕЖЕМЕСЯЧНОЕ УВЕДОМЛЕНИЕ</b>\n',
        'tax_payment': '\n▪️ <b>Налоги:</b> {amount} руб.',
        'accounting_tariff': '\n▪️ <b>Тариф {tariff_name}:</b> {amount} руб.',
        'accounting_service': '\n▪️ <b>Доп. услуга «{service_name}»:</b> {amount} руб.',
        'payment_details': (
            '\n💳 <b>Реквизиты для оплаты:</b>\n'
            '\n🏦 Банк: {bank}'
            '\n📄 Счет: {account}'
            '\n👤 Получатель: {recipient}'
            '\nℹ️ ИНН: {inn}'
            '\n🔢 БИК: {bic}'
            '\n🏛 Корр. счет: {corr_account}'
            '\n📌 Назначение: {purpose}'
        ),
        'total': '\n💠 <b>Итого к оплате:</b> {total} руб.',
        'divider': '\n' + '-' * 30
    }

    GREETINGS = {
        'birthday': (
            '🎉 <b>Дорогой(ая) {full_name}!</b>\n\n'
            'Поздравляем Вас с Днем рождения! 🎂\n'
            'Желаем успехов в бизнесе и личной жизни!'
        ),
        'holiday': (
            '🎊 <b>Уважаемый(ая) {full_name}!</b>\n\n'
            'Поздравляем с {holiday_name}!\n'
            'Пусть праздник принесет радость и хорошее настроение!'
        )
    }

    ERROR = {
        'invalid_amount': '❌ Пожалуйста, введите корректную положительную сумму:',
        'invalid_code': '❌ Неверный код доступа. Попробуйте ещё раз.',
        'system_error': '❌ Произошла системная ошибка.',
        'authorized': 'Вы не авторизованы в системе.',
        'not_user': 'Ваш Telegram ID не найден в системе.'
    }

    @staticmethod
    def format_date(iso_date: str) -> str:
        try:
            return datetime.fromisoformat(iso_date.replace('Z', '')).strftime('%d.%m.%Y %H:%M')
        except (ValueError, AttributeError):
            return iso_date or 'нет данных'

    @staticmethod
    def build_payment_message(payment_details):
        message = [BotMessages.PAYMENT['monthly_notification']]

        if payment_details.get('taxAmount'):
            message.append(BotMessages.PAYMENT['tax_payment'].format(amount=payment_details['taxAmount']))
        
        if accounting := payment_details.get('accountingAmount'):
            if tariff := accounting.get('tariff'):
                message.append(BotMessages.PAYMENT['accounting_tariff'].format(tariff_name=tariff['name'], amount=tariff['amount']))
            if service := accounting.get('additionalService'):
                message.append(BotMessages.PAYMENT['accounting_service'].format(service_name=service['name'], amount=service['amount']))

        message.append(BotMessages.PAYMENT['divider'])
        message.append(BotMessages.PAYMENT['total'].format(total=payment_details.get('totalAmount', 0)))
        message.append(BotMessages.PAYMENT['divider'])
        message.append(BotMessages.PAYMENT['payment_details'].format(**BotMessages.get_requisites()))

        return ''.join(message)
    
    @staticmethod
    def get_requisites():
        return {
            'bank': os.getenv('PAYMENT_BANK_NAME'),
            'account': os.getenv('PAYMENT_ACCOUNT'),
            'recipient': os.getenv('PAYMENT_RECIPIENT'),
            'inn': os.getenv('PAYMENT_INN'),
            'bic': os.getenv('PAYMENT_BIC'),
            'corr_account': os.getenv('PAYMENT_CORR_ACCOUNT'),
            'purpose': os.getenv('PAYMENT_PURPOSE')
        }