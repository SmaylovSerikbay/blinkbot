"""
Модели базы данных
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Integer, DateTime, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database.engine import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False, default="ru")
    role: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 'driver' или 'passenger'
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    car_photo_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Telegram file_id
    rating: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    trip_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Связи
    trips_as_driver: Mapped[list["Trip"]] = relationship("Trip", back_populates="driver", foreign_keys="Trip.driver_id")
    reviews_as_driver: Mapped[list["Review"]] = relationship("Review", back_populates="driver", foreign_keys="Review.driver_id")
    reviews_as_passenger: Mapped[list["Review"]] = relationship("Review", back_populates="passenger", foreign_keys="Review.passenger_id")

    def __repr__(self):
        return f"<User(id={self.telegram_id}, role={self.role}, lang={self.language_code})>"


class Trip(Base):
    """Модель поездки"""
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    driver_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    from_city: Mapped[str] = mapped_column(String(255), nullable=False)
    to_city: Mapped[str] = mapped_column(String(255), nullable=False)
    trip_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # Цена в тенге
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Связи
    driver: Mapped["User"] = relationship("User", back_populates="trips_as_driver", foreign_keys=[driver_id])

    def __repr__(self):
        return f"<Trip(id={self.id}, {self.from_city} -> {self.to_city})>"


class Review(Base):
    """Модель отзыва"""
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    driver_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    passenger_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Связи
    driver: Mapped["User"] = relationship("User", back_populates="reviews_as_driver", foreign_keys=[driver_id])
    passenger: Mapped["User"] = relationship("User", back_populates="reviews_as_passenger", foreign_keys=[passenger_id])

    def __repr__(self):
        return f"<Review(id={self.id}, driver={self.driver_id}, score={self.score})>"

