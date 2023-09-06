# to run the test
# cd to the main directory PDFInsight which houses both src and tests
# run python -m unittest tests.test_pdf_extractor
import unittest

from src.pdfinsight import df2docstore, pdf_extractor, pivot_df_by_heading, remove_toc


class TestCategory(unittest.TestCase):
    # The setUp method is provided by the unittest.TestCase class and is automatically called before each test method within the class. It's used to set up any common resources or configurations needed for the tests.
    def setUp(self):
        self.df = pdf_extractor("tests/sample.pdf", toc_pages=1)

    def test_categories(self):
        df = self.df

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

    def test_remove_toc(self):
        df = self.df

        df = remove_toc(df)
        self.assertEqual("toc" in df.cat.unique(), False)


class TestDocStore(unittest.TestCase):
    # The setUp method is provided by the unittest.TestCase class and is automatically called before each test method within the class. It's used to set up any common resources or configurations needed for the tests.
    def setUp(self):
        self.df = pdf_extractor("tests/sample.pdf", toc_pages=1)
        self.df = remove_toc(self.df)

    def test_pivot_df_by_heading(self):
        df = self.df
        df = pivot_df_by_heading(df)
        self.assertEqual(
            (df.columns == ["file", "heading1", "heading2", "content"]).all(), True
        )
        self.assertEqual(df.loc[1, "file"], "tests/sample.pdf")
        self.assertEqual(df.loc[1, "heading1"], "TITLE")
        self.assertEqual(df.loc[1, "heading2"], "Maecenas eu dapibus diam.")
        self.assertEqual(
            df.loc[2, "content"],
            "Proin at lorem eu urna volutpat dignissim vel nec erat. Mauris ac dui vel felis rutrum malesuada eget quis ante. Phasellus elementum porta lorem, eu sagittis tortor congue sed. Vivamus nec diam sagittis, sagittis erat nec, lacinia erat. Maecenas at leo metus. Vestibulum sit amet diam ut leo accumsan pharetra. Proin tincidunt vestibulum tincidunt. Pellentesque purus nibh, fermentum sit amet dui at, maximus porttitor sapien.\nColumn 1 Column 2 Column 3 Praesent varius consequat id ultricies diam aliquam 456 justo, volutpat\nVestibulum ante ipsum\net posuere elit elit sed orc 567\nprimis in faucibus orci luctus et ultrices posuere cubilia curae;\ncongue nec molestie et, Nullam posuere nibh ut nisi 3956 euismod sit amet tortor. rhoncus semper.",
        )

    def test_df2docstore(self):
        df = self.df
        df = pivot_df_by_heading(df)
        link_dict = dict(zip(df.file.unique(), df.file.unique()))
        df = df2docstore(df, chunk_size=100, link_dict=link_dict)

        self.assertEqual(
            df[2]["content"],
            "TITLE\nProin at lorem eu\nProin at lorem eu urna volutpat dignissim vel nec erat. Mauris ac dui vel felis rutrum malesuada eget quis ante. Phasellus elementum porta lorem, eu sagittis tortor congue sed. Vivamus nec diam sagittis, sagittis erat nec, lacinia erat. Maecenas at leo metus. Vestibulum sit amet diam ut leo accumsan pharetra. Proin tincidunt vestibulum tincidunt. Pellentesque purus nibh, fermentum sit amet dui at, maximus porttitor sapien.\nColumn 1 Column 2 Column 3 Praesent varius consequat id ultricies diam aliquam 456 justo, volutpat\nVestibulum ante ipsum\net posuere elit elit sed orc 567\nprimis in faucibus orci luctus et ultrices posuere cubilia curae;\ncongue nec molestie et, Nullam posuere nibh ut nisi 3956 euismod sit amet tortor. rhoncus semper.",
        )
        self.assertEqual(df[1]["source"], "tests/sample.pdf")
        self.assertEqual(df[1]["update"], "")


if __name__ == "__main__":
    unittest.main()
