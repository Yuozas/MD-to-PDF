import markdown
import pdfkit
from PyPDF2 import PdfReader, PdfWriter
import re
import os

def markdown_to_html(markdown_content):
    html = markdown.markdown(markdown_content, extensions=['extra', 'toc'])

    css = """
    <style>
        @page {
            margin: 0;
            padding: 0;
        }
        html, body {
            margin: 0;
            padding: 0;
            background-color: #1e1e1e;
        }
        body {
            font-family: Arial, sans-serif;
            color: #e0e0e0;
            line-height: 1.6;
            min-height: 100vh;
            box-sizing: border-box;
        }
        .content {
            padding: 40px 60px 40px 60px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
        }
        a {
            color: #4da6ff;
        }
        code {
            background-color: #2d2d2d;
            padding: 2px 4px;
            border-radius: 4px;
        }
        pre {
            background-color: #2d2d2d;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
    </style>
    """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Converted Markdown</title>
        {css}
    </head>
    <body>
        <div class="content">
            {html}
        </div>
    </body>
    </html>
    """

def html_to_pdf(html_content, output_file):
    options = {
        'page-size': 'Letter',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None,
        'print-media-type': None,
        'disable-smart-shrinking': None,
        'zoom': 1.0,
        'dpi': 300,
        'enable-local-file-access': None
    }

    pdfkit.from_string(html_content, output_file, options=options)

def add_bookmarks(input_pdf, output_pdf, markdown_content):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    bookmarks = []
    lines = markdown_content.split('\n')
    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            bookmarks.append((level, title))

    bookmark_stack = [None] * 6  # Max header level is 6
    for level, title in bookmarks:
        # Find the page number for this title
        page_num = None
        for i, page in enumerate(reader.pages):
            if title in page.extract_text():
                page_num = i
                break

        if page_num is None:
            page_num = 0  # Default to first page if not found

        parent = bookmark_stack[level - 2] if level > 1 else None
        bookmark = writer.add_outline_item(title, page_num, parent=parent)
        bookmark_stack[level - 1] = bookmark

    with open(output_pdf, 'wb') as f:
        writer.write(f)

def convert_markdown_to_pdf(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    html_content = markdown_to_html(markdown_content)

    temp_pdf = 'temp.pdf'
    html_to_pdf(html_content, temp_pdf)

    add_bookmarks(temp_pdf, output_file, markdown_content)

    os.remove(temp_pdf)

# Usage
input_file = 'input.md'
output_file = 'output.pdf'
convert_markdown_to_pdf(input_file, output_file)
print(f"Conversion complete. PDF saved as {output_file}")