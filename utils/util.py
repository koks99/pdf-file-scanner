from hashlib import sha256
from io import BytesIO
from PIL import Image
from datetime import datetime

import pdf2image

from utils.database import fs

def extract_metadata(pdf_reader, file_content):
    metadata = pdf_reader.metadata

    return {
        "sha256_hash": sha256(file_content).hexdigest(),
        "title": metadata.title_raw,
        "pdf_version": pdf_reader.pdf_header.split()[0][1:],
        "producer":metadata.producer,
        "author": metadata.author_raw,
        "created_date": parse_pdf_date(metadata.creation_date_raw),
        "updated_date": parse_pdf_date(metadata.modification_date_raw),
        "scan_submitted_utc": datetime.utcnow().isoformat() + "Z"
    }

def parse_pdf_date(date_str):
    if date_str is None:
        return None
    cleaned_date_str = date_str.replace("D:", "")
    cleaned_date_str = cleaned_date_str.split('Z')[0]
    cleaned_date_str = cleaned_date_str.split('+')[0]
    cleaned_date_str = cleaned_date_str.split('-')[0]
    try:
        date_obj = datetime.strptime(cleaned_date_str, "%Y%m%d%H%M%S")
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

#Convert PDF into image and save it in DB
async def save_image(file_content, sha256_hash):
    if fs.find_one({"filename": f"{sha256_hash}.png"}):
        return None

    images = pdf2image.convert_from_bytes(file_content)

    # Vertically stitching images into one
    widths, heights = zip(*(i.size for i in images))
    total_height = sum(heights)
    max_width = max(widths)
    combined_image = Image.new('RGB', (max_width, total_height))
    current_y = 0
    for image in images:
        combined_image.paste(image, (0, current_y))
        current_y += image.height

    img_byte_arr = BytesIO()
    combined_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    fs.put(img_byte_arr, filename=f"{sha256_hash}.png")