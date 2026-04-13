import argparse
import sys
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract

def pdf_to_md(input_pdf_path, output_md_path):
    try:
        reader = PdfReader(input_pdf_path)
        text = ""

        # We need to extract images only when text extraction fails, but converting
        # the whole PDF to images page by page is easier with pdf2image.
        # However, it's more efficient to just convert the specific pages that failed.
        # pdf2image can convert specific pages.

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()

            # If text extraction fails or returns very little text, try OCR
            if not page_text or len(page_text.strip()) < 10:
                print(f"Page {i+1} has no/little extractable text. Attempting OCR...")
                # pdf2image first_page and last_page are 1-indexed
                images = convert_from_path(input_pdf_path, first_page=i+1, last_page=i+1)
                if images:
                    page_text = pytesseract.image_to_string(images[0])

            if page_text:
                text += page_text
                text += "\n\n"

        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully converted {input_pdf_path} to {output_md_path}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF file to a Markdown file by extracting its text or using OCR.")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_md", help="Path to the output Markdown file")

    args = parser.parse_args()

    pdf_to_md(args.input_pdf, args.output_md)
