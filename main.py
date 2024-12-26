from PyPDF2.errors import PdfReadError
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from PyPDF2 import PdfReader
from io import BytesIO
from starlette.responses import StreamingResponse
from utils.database import fs, pdf_col
from utils.util import extract_metadata, save_image

app = FastAPI()

# Endpoint to scan the pdf and store the metadata in MongoDB
@app.post("/scan")
async def scan_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):

    file_content = await file.read()
    try:
        PdfReader(BytesIO(file_content))
    except PdfReadError:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid PDF")

    pdf_reader = PdfReader(BytesIO(file_content))
    pdf_metadata = extract_metadata(pdf_reader, file_content)
    sha = pdf_metadata["sha256_hash"]

    pdf_col.update_one({"sha256_hash": sha},
                       {"$set": pdf_metadata}, upsert=True)

    # Running image processing and storing in background
    background_tasks.add_task(save_image, file_content, sha)

    return {"sha256_hash": sha}

# Endpoint to retrieve the metadata from MongoDB using the SHA256 hash
@app.get("/lookup/{sha256_hash}")
async def get_metadata(sha256_hash: str):
    metadata = pdf_col.find_one({"sha256_hash": sha256_hash})

    if not metadata:
        raise HTTPException(status_code=404, detail="File with provided SHA256 not found")

    metadata.pop('_id', None)
    return {"metadata": metadata}

# Endpoint to retrieve the image from MongoDB using the SHA256 hash
@app.get("/image/{sha256_hash}")
async def get_pdf_image(sha256_hash: str):
    image = fs.find_one({"filename": f"{sha256_hash}.png"})

    if not image:
        raise HTTPException(status_code=404, detail="Image with provided SHA256 not found")

    return StreamingResponse(image, media_type="image/png")
