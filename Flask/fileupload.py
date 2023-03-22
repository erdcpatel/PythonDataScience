import asyncio
import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def validate_file(file_path):
    """
    Validate the contents of a file at the specified path.
    """
    # Perform some file validation here, such as checking file size or format
    # ...
    print(f"File {file_path} has been validated.")

@app.post("/uploadfile/", tags=["File Operations"])
async def create_upload_file(file: UploadFile = File(...), file_type: str = Form(...)):
    """
    Upload a file and save it to disk with a specified file type.
    """
    try:

        # Save the file to disk
        with open(f"{file.filename}", "wb") as f:
            contents = await file.read()
            f.write(contents)

        # Start a new thread to perform file validation
        loop = asyncio.get_event_loop()
        file_path = os.path.abspath(file.filename)
        loop.run_in_executor(None, validate_file, file_path)

        return {"filename": file.filename, "file_type": file_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{file_path:path}", tags=["File Operations"])
async def download_file(file_path: str):
    """
    Download a file from disk and stream its contents to the client.
    """
    try:
        # Check if file exists
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Open the file in binary mode and stream its contents to the client
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_stream = open(file_path, mode="rb")
        return StreamingResponse(file_stream, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_name}", "Content-Length": str(file_size)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    ## Read Item

    This endpoint returns information about a specific item.

    - `item_id` - The ID of the item to retrieve.

    ### Response

    If the item is found, the endpoint returns a JSON object with the following fields:

    - `id` - The ID of the item.
    - `name` - The name of the item.
    - `description` - A description of the item.

    If the item is not found, the endpoint returns a 404 Not Found error.
    """

def custom_openapi():
    """
    Generate a custom OpenAPI schema for the FastAPI application.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="0.1.0",
        description="API for file operations",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi