from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./chat.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
