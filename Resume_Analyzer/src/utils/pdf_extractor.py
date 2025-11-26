from langchain_community.document_loaders import PyPDFLoader

def extract_text_from_pdf(path):
    loader = PyPDFLoader(path)
    docs = loader.load()
    return "\n".join(d.page_content for d in docs)
