from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
import os
import uuid

app = FastAPI()

# Define database schema
Base = declarative_base()

class FileDetails(Base):
    __tablename__ = "file_details"

    id = Column(String, primary_key=True, index=True)
    file_name = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    upload_time = Column(DateTime)

    def __repr__(self):
        return f"<FileDetails(id={self.id}, file_name={self.file_name}, file_size={self.file_size}, file_type={self.file_type}, upload_time={self.upload_time})>"

# Create database engine and connection pool
engine = create_engine("oracle+cx_oracle://user:password@host:port/service_name", pool_size=5, max_overflow=10)

# Create a scoped session factory that uses the connection pool
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

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), file_type: str = Form(...)):
    """
    Upload a file and save it to disk with a specified file type.
    """
    try:
        # Generate a unique ID for the file
        file_id = generate_id()

        # Save the file to disk
        with open(file_id, "wb") as f:
            contents = await file.read()
            f.write(contents)

        # Log the file details in the database
        file_details = FileDetails(
            id=file_id,
            file_name=file.filename,
            file_size=os.path.getsize(file_id),
            file_type=file_type,
            upload_time=datetime.now(),
        )

        session = Session()
        session.add(file_details)
        session.commit()
        session.close()

        return {"filename": file.filename, "file_type": file_type, "file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_id():
    """
    Generate a random ID with the current timestamp and a random number.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    random_number = uuid.uuid4().hex[:6].upper()
    return f"{timestamp}-{random_number}"


'''
--------------

from sqlalchemy.orm import Session

class Database:
    def __init__(self, session: Session):
        self.session = session

    def create_file_details(self, file_id: str, file_name: str, file_size: int, file_type: str, upload_time: datetime):
        """
        Log the file details in the database.
        """
        file_details = FileDetails(
            id=file_id,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            upload_time=upload_time,
        )
        self.session.add(file_details)
        self.session.commit()

    def get_file_details(self, file_id: str) -> FileDetails:
        """
        Retrieve the file details with the specified ID.
        """
        return self.session.query(FileDetails).filter(FileDetails.id == file_id).first()

--------
@app.get("/file_details/{file_id}")
async def read_file_details(file_id: str, db: Database = Depends(get_db)):
    """
    Retrieve the file details with the specified ID.
    """
    file_details = db.get_file_details(file_id)
    if not file_details:
        raise HTTPException(status_code=404, detail="File not found")
    return file_details
'''