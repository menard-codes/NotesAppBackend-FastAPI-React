from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = "sqlite:///./db.sql"

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)
DBSession = sessionmaker(engine, autoflush=False)
