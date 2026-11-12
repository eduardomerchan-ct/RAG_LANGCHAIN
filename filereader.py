from pathlib import Path                      # Path makes working with file locations easier
from typing import List                       # List lets us say "a list of X" in type hints
from langchain_core.documents import Document # LangChain's container: text + info about where it came from
from pypdf import PdfReader                   #  The tool that opens and reads PDFs


def read_pdf_text(pdf_path: str | Path) -> str:   # takes a path and gives back a string
    """Read and return the text contents of a pdf file"""

    path = Path(pdf_path)                     # makes the input into a followable path 

    if not path.exists():                    #if the file does not exist
        raise FileNotFoundError(f"The pdf was not found at {path}")  #then we raise an error and the path that raised it

    reader = PdfReader(str(path))             # open the PDF so we can actually read it

    # go through every page, pull out its text.
    #if it is empty then returns and empty string 
    text_parts = [page.extract_text() or "" for page in reader.pages]

    return "\n".join(text_parts)              # puts all the pages toghere with a newline


def read_multiple_pdfs(pdf_paths: List[str | Path]) -> List[Document]:  
    """Read text from multiple pdfs and return a list of documents"""

    docs: List[Document] = []                 # we create an empty list of docs to store them in later

    for path in pdf_paths:                    # go through each PDF path one at a time that was passed in
        path_obj = Path(path)                 # #create the path in python

        text = read_pdf_text(path_obj)        # calls on the fucntion above with this path

        # wrap the text in a Document and make sure we remeber the source of where it comes from
        docs.append(Document(page_content=text, metadata={"source": str(path_obj)}))

    return docs             #returns the list of docs