from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from dotenv import load_dotenv
import os

load_dotenv()
postgres_user=os.getenv("POSTGRES_USER")
postgres_password=os.getenv("POSTGRES_PASSWORD")
postgres_host=os.getenv("POSTGRES_HOST")
postgres_port=os.getenv("POSTGRES_PORT")
postgres_database=os.getenv("POSTGRES_DB")


postgres_237_user=os.getenv("DB_CONFIG_237_USER")
postgres_237_password=os.getenv("DB_CONFIG_237_PASSWORD")
postgres_237_host=os.getenv("DB_CONFIG_237_HOST")
postgres_237_port=os.getenv("DB_CONFIG_237_PORT")
postgres_237_schema=os.getenv("DB_CONFIG_237_SCHEMA")
postgres_237_database=os.getenv("DB_CONFIG_237_DATABASE")


DATABASE_URL_237 = f"postgresql://{postgres_237_user}:{postgres_237_password}@{postgres_237_host}:{postgres_237_port}/{postgres_237_database}?options=-csearch_path%3D{postgres_237_schema}"
engine_237 = create_engine(DATABASE_URL_237)
SessionLocal_237 = sessionmaker(autocommit=False, autoflush=False, bind=engine_237)


postgres_236_user=os.getenv("DB_CONFIG_236_USER")
postgres_236_password=os.getenv("DB_CONFIG_236_PASSWORD")
postgres_236_host=os.getenv("DB_CONFIG_236_HOST")
postgres_236_port=os.getenv("DB_CONFIG_236_PORT")
postgres_236_schema=os.getenv("DB_CONFIG_236_SCHEMA")
postgres_236_database=os.getenv("DB_CONFIG_236_DATABASE")


DATABASE_URL_236 = f"postgresql://{postgres_236_user}:{postgres_236_password}@{postgres_236_host}:{postgres_236_port}/{postgres_236_database}?options=-csearch_path%3D{postgres_236_schema}"
engine_236 = create_engine(DATABASE_URL_236)
SessionLocal_236 = sessionmaker(autocommit=False, autoflush=False, bind=engine_236)


postgres_243_user=os.getenv("DB_CONFIG_243_USER")
postgres_243_password=os.getenv("DB_CONFIG_243_PASSWORD")
postgres_243_host=os.getenv("DB_CONFIG_243_HOST")
postgres_243_port=os.getenv("DB_CONFIG_243_PORT")
postgres_243_schema=os.getenv("DB_CONFIG_243_SCHEMA")
postgres_243_database=os.getenv("DB_CONFIG_243_DATABASE")


DATABASE_URL_243 = f"postgresql://{postgres_243_user}:{postgres_243_password}@{postgres_243_host}:{postgres_243_port}/{postgres_243_database}?options=-csearch_path%3D{postgres_243_schema}"
engine_243 = create_engine(DATABASE_URL_243)
SessionLocal_243 = sessionmaker(autocommit=False, autoflush=False, bind=engine_243)

        
DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_database}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_db_1():
    db = SessionLocal_237()
    try:
        yield db
    finally:
        db.close()


def get_db_2():
    db = SessionLocal_236()
    try:
        yield db
    finally:
        db.close()
        
        
def get_db_3():
    db = SessionLocal_243()
    try:
        yield db
    finally:
        db.close()
metadata = MetaData()