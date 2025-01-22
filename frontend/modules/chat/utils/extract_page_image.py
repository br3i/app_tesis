import fitz
from PIL import Image
import io


def extract_page_image(pdf_path, page_number):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number - 1)  # PyMuPDF usa indexación 0
    pix = page.get_pixmap(dpi=300)  # type: ignore
    img = Image.open(io.BytesIO(pix.tobytes()))
    return img
