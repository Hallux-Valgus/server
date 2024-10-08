from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://jorim:1234@localhost:3306/test", echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

class SessionManager:
    def __enter__(self):
        self.session = SessionLocal()
        return self.session
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()