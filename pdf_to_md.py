import argparse
import sys
from pypdf import PdfReader

def pdf_to_md(input_pdf_path, output_md_path):
    try:
        reader = PdfReader(input_pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            text += page.extract_text()
            if text:
                text += "\n\n"

        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully converted {input_pdf_path} to {output_md_path}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF file to a Markdown file by extracting its text.")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_md", help="Path to the output Markdown file")

    args = parser.parse_args()

    pdf_to_md(args.input_pdf, args.output_md)
