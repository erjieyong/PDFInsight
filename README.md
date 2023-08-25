# PDFInsight
Text Mining &amp; Classification Toolkit

Extract and categorise text-based PDFs into the following categories
- table of contents
- header
- heading
- tables
- content
- footnote
- footer
- page number
- unsure (text that cannot be categorised)

## Example
```
import pdfinsight
df = pdfinsight.pdf_extractor("sample.pdf")
```

## Installation
`pip install pdfinsight`

## References
[https://github.com/pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF)