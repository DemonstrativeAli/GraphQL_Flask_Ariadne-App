from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./db.sqlite3"

# creating engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# creating session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creating base class for models
Base = declarative_base()