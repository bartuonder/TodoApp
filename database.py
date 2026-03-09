from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#"postgresql://postgres:test1234!@localhost/TodoApplicationDatabase"
DATABASE_URL = "sqlite:///./todos_app.db"
#"mysql+pymysql://root:test1234!@127.0.0.1:3306/todoappdatabase"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()