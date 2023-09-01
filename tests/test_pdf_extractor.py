# to run the test
# cd to the main directory PDFInsight which houses both src and tests
# run python -m unittest tests.test_pdf_extractor
import unittest

from src.pdfinsight import pdf_extractor

df = pdf_extractor("tests/sample.pdf", toc_pages=1)


class TestCategory(unittest.TestCase):
    def test_categories(self):
        self.assertEqual(
            df[(df["page"] == 1) & (df["text"] == "SAMPLE PDF")]["cat"].values[0], "toc"
        )
        self.assertEqual(
            df[(df["page"] == 2) & (df["text"] == "Sample PDF")]["cat"].values[0],
            "header",
        )
        self.assertEqual(
            df[(df["page"] == 2) & (df["text"] == "TITLE")]["cat"].values[0],
            "heading1",
        )
        self.assertEqual(
            df[(df["page"] == 3) & (df["text"] == "Column 1")]["cat"].values[0], "table"
        )
        self.assertEqual(
            df[
                (df["page"] == 2) & (df["text"] == "in nunc sed, sodales accumsan dui.")
            ]["cat"].values[0],
            "content",
        )
        self.assertEqual(
            df[
                (df["page"] == 2)
                & (
                    df["text"]
                    == "Footnote: Nulla quis mi leo. Integer efficitur felis eget leo commodo, sed suscipit eros suscipit. Sed dictum"
                )
            ]["cat"].values[0],
            "footnote",
        )
        self.assertEqual(
            df[(df["page"] == 3) & (df["text"] == "THIS IS A FOOTER")]["cat"].values[0],
            "footer",
        )
        self.assertEqual(
            df[(df["page"] == 2) & (df["text"] == "Page 2 of 3")]["cat"].values[0],
            "page_number",
        )


if __name__ == "__main__":
    unittest.main()
