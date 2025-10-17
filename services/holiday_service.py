import json
from datetime import datetime

from modules import *

class HolidayService:
    def __init__(self, file_path='./templates/holidays.json'):
        self.file_path = file_path
        self.holidays = self._load_holidays() or []

    def _load_holidays(self):
        '''Loading holidays from JSON'''
        try:
            with open(self.file_path, 'r', encoding='utf-8') as holidays:
                data = json.load(holidays)
                return self._parse_holidays(data['holidays'])
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            logger.error(f'Error loading holidays: {e}')
            return []
    
    def _parse_holidays(self, holidays_data):
        '''Converts string dates to date objects'''
        parsed_holidays = []
        for holiday in holidays_data:
            try:
                month, day = map(int, holiday['date'].split('-'))
                parsed_holidays.append({
                    'name': holiday['name'],
                    'month': month,
                    'day': day
                })
            except (ValueError, KeyError) as e:
                logger.error(f'Error parsing holiday date: {e}')
        return parsed_holidays
    
    def get_current_holiday(self):
        '''Returns the name of today's holiday or None'''
        today = datetime.now()
        for holiday in self.holidays:
            if holiday['month'] == today.month and holiday['day'] == today.day:
                return holiday['name']
        return None