from sqlalchemy import create_engine
from sqalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(
    settings.database_url,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
