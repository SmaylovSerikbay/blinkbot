"""
Запросы к базе данных
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Trip, Review


class UserRepository:
    """Репозиторий для работы с пользователями"""

    @staticmethod
    async def get_by_telegram_id(session: AsyncSession, telegram_id: int) -> Optional[User]:
        """Получить пользователя по telegram_id"""
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(session: AsyncSession, telegram_id: int, **kwargs) -> User:
        """Создать нового пользователя"""
        user = User(telegram_id=telegram_id, **kwargs)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update_language(session: AsyncSession, telegram_id: int, language_code: str) -> Optional[User]:
        """Обновить язык пользователя"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user:
            user.language_code = language_code
            await session.commit()
            await session.refresh(user)
        return user

    @staticmethod
    async def update_role(session: AsyncSession, telegram_id: int, role: str) -> Optional[User]:
        """Обновить роль пользователя"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user:
            user.role = role
            await session.commit()
            await session.refresh(user)
        return user

    @staticmethod
    async def get_or_create(session: AsyncSession, telegram_id: int, **kwargs) -> User:
        """Получить или создать пользователя"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if not user:
            user = await UserRepository.create(session, telegram_id, **kwargs)
        return user

    @staticmethod
    async def update_phone(session: AsyncSession, telegram_id: int, phone_number: str) -> Optional[User]:
        """Обновить номер телефона пользователя"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user:
            user.phone_number = phone_number
            await session.commit()
            await session.refresh(user)
        return user

    @staticmethod
    async def update_verification(session: AsyncSession, telegram_id: int, is_verified: bool) -> Optional[User]:
        """Обновить статус верификации"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user:
            user.is_verified = is_verified
            await session.commit()
            await session.refresh(user)
        return user

    @staticmethod
    async def update_car_photo(session: AsyncSession, telegram_id: int, car_photo_id: str) -> Optional[User]:
        """Обновить фото машины"""
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user:
            user.car_photo_id = car_photo_id
            await session.commit()
            await session.refresh(user)
        return user

    @staticmethod
    async def recalculate_rating(session: AsyncSession, telegram_id: int) -> Optional[User]:
        """Пересчитать рейтинг водителя на основе отзывов"""
        from sqlalchemy import func
        user = await UserRepository.get_by_telegram_id(session, telegram_id)
        if user:
            # Вычисляем средний рейтинг из отзывов
            result = await session.execute(
                select(func.avg(Review.score))
                .where(Review.driver_id == telegram_id)
            )
            avg_rating = result.scalar()
            if avg_rating:
                user.rating = round(float(avg_rating), 2)
            await session.commit()
            await session.refresh(user)
        return user


class TripRepository:
    """Репозиторий для работы с поездками"""

    @staticmethod
    async def create(session: AsyncSession, driver_id: int, from_city: str, to_city: str,
                     trip_date, price: int, description: Optional[str] = None) -> Trip:
        """Создать новую поездку"""
        trip = Trip(
            driver_id=driver_id,
            from_city=from_city,
            to_city=to_city,
            trip_date=trip_date,
            price=price,
            description=description
        )
        session.add(trip)
        await session.commit()
        await session.refresh(trip)
        return trip

    @staticmethod
    async def get_active_trips(session: AsyncSession, limit: int = 10, offset: int = 0) -> list[Trip]:
        """Получить активные поездки"""
        result = await session.execute(
            select(Trip)
            .where(Trip.is_active == True)
            .order_by(Trip.trip_date.asc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(session: AsyncSession, trip_id: int) -> Optional[Trip]:
        """Получить поездку по ID"""
        result = await session.execute(
            select(Trip).where(Trip.id == trip_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def increment_trip_count(session: AsyncSession, driver_id: int) -> Optional[User]:
        """Увеличить счетчик поездок водителя"""
        user = await UserRepository.get_by_telegram_id(session, driver_id)
        if user:
            user.trip_count += 1
            await session.commit()
            await session.refresh(user)
        return user


class ReviewRepository:
    """Репозиторий для работы с отзывами"""

    @staticmethod
    async def create(session: AsyncSession, driver_id: int, passenger_id: int, 
                     score: int, comment: Optional[str] = None) -> Review:
        """Создать новый отзыв"""
        review = Review(
            driver_id=driver_id,
            passenger_id=passenger_id,
            score=score,
            comment=comment
        )
        session.add(review)
        await session.commit()
        await session.refresh(review)
        
        # Пересчитываем рейтинг водителя
        await UserRepository.recalculate_rating(session, driver_id)
        
        return review

    @staticmethod
    async def get_by_driver(session: AsyncSession, driver_id: int) -> list[Review]:
        """Получить все отзывы водителя"""
        result = await session.execute(
            select(Review)
            .where(Review.driver_id == driver_id)
            .order_by(Review.created_at.desc())
        )
        return list(result.scalars().all())

