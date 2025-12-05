from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base


DB_URL="mysql+pymysql://root:ravi@localhost:3306/zippee_assign"

engine=create_engine(DB_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db:Session=SessionLocal()
    try:
        yield db
    finally:
        db.close()    
  



