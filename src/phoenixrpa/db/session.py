from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from phoenixrpa.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)