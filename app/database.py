from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_dbname}"

while True:
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL
        )
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("Connection established....")
        break
    except Exception as e:
        print("Some error occured : ", e)
        time.sleep(2)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()