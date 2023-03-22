from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, time, timedelta
import json

app = FastAPI()

Base = declarative_base()

class FileDetails(Base):
    __tablename__ = "file_details"

    id = Column(String, primary_key=True, index=True)
    file_name = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    uploaded_by = Column(String)
    file_location = Column(String)
    upload_time = Column(DateTime)
    processed_status = Column(String)
    error_message = Column(String)

engine = create_engine("oracle+cx_oracle://user:password@host:port/service_name", pool_size=5, max_overflow=10)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

@app.on_event("startup")
def startup():
    """
    Initialize the database connection pool on app startup.
    """
    engine.connect()

@app.on_event("shutdown")
def shutdown():
    """
    Close the database connection pool on app shutdown.
    """
    engine.dispose()

def get_db():
    """
    Return a database session from the connection pool.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/files/")
async def get_files(
    filter: str = Query(None, max_length=100),
    db: Session = Depends(get_db)
):
    """
    Get a list of files uploaded on the current date and for the specified shift.
    """
    try:
        # Determine the current date and time
        now = datetime.now()
        today = now.date()
        current_time = now.time()

        # Parse the filter string into a dictionary
        if filter is not None:
            filter_dict = json.loads(filter)
        else:
            filter_dict = {}

        # Determine the start and end times for the specified shift
        if "shift" in filter_dict:
            shift = filter_dict["shift"]
            if shift == "morning":
                start_time = time(6, 0, 0)
                end_time = time(14, 0, 0)
            elif shift == "afternoon":
                start_time = time(14, 0, 0)
                end_time = time(22, 0, 0)
            elif shift == "evening":
                start_time = time(22, 0, 0)
                end_time = time(6, 0, 0)
                today = today + timedelta(days=1)
            else:
                start_time = None
                end_time = None
        else:
            start_time = None
            end_time = None

        # Build the query to retrieve files uploaded on the current date and for the specified shift
        query = db.query(FileDetails).filter(
            FileDetails.upload_time >= datetime.combine(today, start_time),
            FileDetails.upload_time < datetime.combine(today, end_time)
        )

        # Execute the query and return the results
        results = query.all()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
