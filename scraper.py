"""
Scraper script to extract all text from the Scribd document.
Reads Scribd.pdf and outputs clean text to scraped_text.txt.
"""

import re
from pdfminer.high_level import extract_text


def clean_text(raw: str) -> str:
    # Remove single-line page headers/footers produced by the PDF-to-HTML conversion.
    # These look like:  "3/28/26, 5:54 PM   Scribd   file:///…/Scribd.html   1/1623"
    # Note: pdfminer may emit the 'fi' ligature (ﬁ) so we match any non-space chars
    # for the URL portion.
    raw = re.sub(
        r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[AP]M\s+Scribd\s+\S+\s+\d+/\d+',
        '',
        raw,
    )
    # Remove multi-line last-page footer remnants (date, "Scribd", URL, page numbers)
    raw = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[AP]M', '', raw)
    raw = re.sub(r'^\s*Scribd\s*$', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'^\s*\S+scribd\S*\s*$', '', raw, flags=re.MULTILINE | re.IGNORECASE)
    raw = re.sub(r'^\s*\d+\s*/\s*\d+\s*$', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'^\s*Download this PDF\s*$', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'^\s*View on Scribd\s*$', '', raw, flags=re.MULTILINE)
    # Collapse runs of more than two consecutive newlines into a single blank line
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    return raw.strip()


def scrape(pdf_path: str = 'Scribd.pdf', output_path: str = 'scraped_text.txt') -> None:
    print(f'Extracting text from {pdf_path} …')
    raw = extract_text(pdf_path)
    text = clean_text(raw)
    with open(output_path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print(f'Done. {len(text):,} characters written to {output_path}')


if __name__ == '__main__':
    scrape()
