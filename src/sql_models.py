from datetime import datetime

from sqlalchemy import DateTime, Integer, String, inspect
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(16200), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    rubrics: Mapped[list[str]] = mapped_column(JSON, nullable=False)


async def create_table(engine: AsyncEngine) -> bool:
    async with engine.begin() as connection:

        def check_table(conn):
            return inspect(conn).has_table("documents")

        has_table = await connection.run_sync(check_table)

        if not has_table:
            await connection.run_sync(Base.metadata.create_all)
            return False

        return True
