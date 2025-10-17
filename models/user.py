import json
from redis import Redis
from dataclasses import dataclass

from modules.Config import Config

@dataclass
class User:
    telegram_id: int
    full_name: str
    birth_date: str
    email: str
    last_payment: dict | None = None

    @staticmethod
    def get_redis_connection() -> Redis:
        '''Creates and returns a Redis connection using configuration from Config.'''
        return Redis.from_url(Config.REDIS_URL)
        
    @classmethod
    def get_session(cls, telegram_id: int) -> 'User | None':
        '''Gets user data from Redis'''
        redis = cls.get_redis_connection()
        if data := redis.get(f'user:{telegram_id}'):
            return cls(**json.loads(data.decode('utf-8')))
        return None
    
    @classmethod
    def get_all_users(cls) -> list['User']:
        '''Get all active users from Redis'''
        redis = cls.get_redis_connection()
        users = []

        for key in redis.scan_iter('user:*'):
            if data := redis.get(key):
                try:
                    users.append(cls(**json.loads(data.decode('utf-8'))))
                except json.JSONDecodeError:
                    continue
        return users
    
    def store_session(self) -> None:
        '''Stores user data in Redis'''
        redis = self.get_redis_connection()
        redis.set(
            f'user:{self.telegram_id}',
            json.dumps({
                'telegram_id': self.telegram_id,
                'full_name': self.full_name,
                'birth_date': self.birth_date,
                'email': self.email,
                'last_payment': self.last_payment
            })
        )
