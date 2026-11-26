from dotenv import load_dotenv
from pypdf import PdfReader
from mineru import MinerU
import os

load_dotenv()

# pdf = PdfReader(r"C:\Users\v1252\Documents\高嘉豪-15031482956.pdf")

# print(f"共{len(pdf.pages)}页")

# full_text = "".join(page.extract_text() or "" for page in pdf.pages)
# print(full_text)


client = MinerU(os.environ.get("MINERU_API_KEY"))
result = client.extract(r"C:\Users\v1252\Documents\高嘉豪-15031482956.pdf")
print(result.markdown)
print(result.html)
print(result.images)  # Access extracted images
