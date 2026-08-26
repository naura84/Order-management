from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "postgresql+psycopg://order_admin:order_password@localhost:5432/order_management"


engine = create_engine(
    DATABASE_URL,
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass