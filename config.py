"""
Конфигурация приложения
"""
from typing import Optional
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Настройки приложения"""
    BOT_TOKEN: str
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "blink_db"
    DB_USER: str = "blink_user"
    DB_PASSWORD: str = ""  # Опционально, по умолчанию пустая строка
    ADMIN_ID: str = ""  # ID администратора в Telegram (строка, будет конвертироваться в int)
    
    def get_admin_id(self) -> Optional[int]:
        """Получить ID администратора как int, или None если не установлен или некорректный"""
        if not self.ADMIN_ID or self.ADMIN_ID.strip() == "":
            return None
        try:
            return int(self.ADMIN_ID.strip())
        except (ValueError, TypeError):
            return None

    @property
    def DATABASE_URL(self) -> str:
        """URL подключения к базе данных"""
        # Если пароль не указан, используем формат без пароля
        if self.DB_PASSWORD:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            return f"postgresql+asyncpg://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


config = Config()

