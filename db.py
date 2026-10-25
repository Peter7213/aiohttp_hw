import os
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, MappedColumn
from sqlalchemy import Integer, String, DateTime, func

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Uberion")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ad_app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

POSTGRES_DSN = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_async_engine(POSTGRES_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Ad(Base):
    __tablename__ = "ads"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    header: MappedColumn[str] = mapped_column(String)
    ad_body: MappedColumn[str] = mapped_column(String)
    owner: MappedColumn[str] = mapped_column(String)
    publication_date: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    @property
    def id_dict(self):
        return {'id': self.id}

    @property
    def dict(self):
        return {'id': self.id, 'header': self.header,
                'ad_body': self.ad_body, 'owner': self.owner,
                'publication_date': int(self.publication_date.timestamp())}


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()