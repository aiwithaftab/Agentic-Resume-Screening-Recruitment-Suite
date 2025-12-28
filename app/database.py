from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates the actual database file in your folder
DATABASE_URL = "sqlite:///./candidates.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This is the table structure the Agent will save to
class CandidateRecord(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    final_score = Column(Float)
    reasoning = Column(Text) # The 'Agentic' decision goes here

# This line physically creates the .db file if it doesn't exist
Base.metadata.create_all(bind=engine)