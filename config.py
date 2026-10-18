import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL: "postgresql+psycopg2://postgres:11111111@localhost:5432/weather_db"
# MySQL: "mysql+pymysql://root:11111111@localhost:3306/weather_db"
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:11111111@localhost:3306/weather_db"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()