from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import json

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

class FileTemplate(Base):
    __tablename__ = "file_template"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String)
    template_id = Column(String)

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

def get_db():
    """
    Return a database session from the connection pool.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), file_type: str = Form(...), db: Session = Depends(get_db)):
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

        db.add(file_details)
        db.commit()

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

@app.get("/file_templates")
async def get_file_templates(db: Session = Depends(get_db)):
    """
    Retrieve the list of file templates from the database.
    """
    templates = db.query(FileTemplate).all()

    # Convert the list of templates to a JSON response
    response_data = [{"display_name": t.display_name, "template_id": t.template_id} for t in templates]
    return json.dumps(response_data)

'''
CREATE TABLE file_details (
    id VARCHAR2(50) NOT NULL,
    file_name VARCHAR2(255) NOT NULL,
    file_location VARCHAR2(255) NOT NULL,
    file_type VARCHAR2(50) NOT NULL,
    uploaded_by VARCHAR2(100) NOT NULL,
    file_size NUMBER NOT NULL,
    upload_time TIMESTAMP NOT NULL,
    processed_status VARCHAR2(20),
    error_message VARCHAR2(1000),
    CONSTRAINT file_details_pk PRIMARY KEY (id)
);

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import uuid
from datetime import datetime
import os

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

@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...),
    file_type: str = Form(...),
    uploaded_by: str = Form(...),
    db: Session = Depends(get_db)
):
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
        file_location = os.path.abspath(file_id)
        file_size = os.path.getsize(file_location)
        upload_time = datetime.now()
        file_details = FileDetails(
            id=file_id,
            file_name=file.filename,
            file_size=file_size,
            file_type=file_type,
            uploaded_by=uploaded_by,
            file_location=file_location,
            upload_time=upload_time,
            processed_status=None,
            error_message=None
        )

        db.add(file_details)
        db.commit()

        return {
            "filename": file.filename,
            "file_type": file_type,
            "file_id": file_id,
            "file_location": file_location,
            "file_size": file_size,
            "upload_time": upload_time,
            "uploaded_by": uploaded_by,
            "processed_status": None,
            "error_message": None
        }
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