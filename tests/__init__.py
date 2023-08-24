import os
import sys
# we have to set the src path so that the import pdfinsight in test_pdf_extractor.py 
# will work properly
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)