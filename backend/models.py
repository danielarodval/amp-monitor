from sqlalchemy import String, Integer, BigInteger, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from .db import Base

class ServerInfo(Base):
    __tablename__ = "server_info"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_name: Mapped[str] = mapped_column(String(128), index=True)
    instance_name: Mapped[str] = mapped_column(String(128), index=True)
    max_users: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Metrics(Base):
    __tablename__ = "metrics"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    application_name: Mapped[str] = mapped_column(String(128), index=True)
    instance_name: Mapped[str] = mapped_column(String(128), index=True)
    user_count: Mapped[int] = mapped_column(Integer)
    max_users: Mapped[int] = mapped_column(Integer)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    uptime: Mapped[int] = mapped_column(BigInteger)  # seconds
    ram_usage: Mapped[float] = mapped_column(Float)  # percent or MB — pick one convention
    cpu_usage: Mapped[float] = mapped_column(Float)  # percent
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
