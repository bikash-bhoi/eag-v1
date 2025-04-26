from hmac import new
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import os
import json
import faiss
import numpy as np
from pathlib import Path
import requests
from markitdown import MarkItDown
import time
from models import AddInput, AddOutput, SqrtInput, SqrtOutput, StringsToIntsInput, StringsToIntsOutput, ExpSumInput, ExpSumOutput
from download_html_files import download_reports
from PIL import Image as PILImage
from tqdm import tqdm
import hashlib
import re
from bs4 import BeautifulSoup
import trafilatura

mcp = FastMCP("Calculator")

EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 256
CHUNK_OVERLAP = 40
ROOT = Path(__file__).parent.resolve()

ipl_matches_dir = Path(__file__).parent / "ipl_matches"

def get_embedding(text: str) -> np.ndarray:
    response = requests.post(EMBED_URL, json={"model": EMBED_MODEL, "prompt": text})
    response.raise_for_status()
    return np.array(response.json()["embedding"], dtype=np.float32)

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    for i in range(0, len(words), size - overlap):
        yield " ".join(words[i:i+size])

def mcp_log(level: str, message: str) -> None:
    """Log a message to stderr to avoid interfering with JSON communication"""
    sys.stderr.write(f"{level}: {message}\n")
    sys.stderr.flush()

@mcp.tool()
def search_documents(query: str) -> list[str]:
    """Search for relevant content from uploaded documents."""
    ensure_faiss_ready()
    mcp_log("SEARCH", f"Query: {query}")
    try:
        index = faiss.read_index(str(ROOT / "faiss_index" / "index.bin"))
        metadata = json.loads((ROOT / "faiss_index" / "metadata.json").read_text())
        query_vec = get_embedding(query).reshape(1, -1)
        D, I = index.search(query_vec, k=5)
        results = []
        for idx in I[0]:
            data = metadata[idx]
            results.append(f"{data['chunk']}\n[Source: {data['doc']}, ID: {data['chunk_id']}]")
        return results
    except Exception as e:
        return [f"ERROR: Failed to search: {str(e)}"]

@mcp.tool()
def add(input: AddInput) -> AddOutput:
    print("CALLED: add(AddInput) -> AddOutput")
    return AddOutput(result=input.a + input.b)

@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Square root of a number"""
    print("CALLED: sqrt(SqrtInput) -> SqrtOutput")
    return SqrtOutput(result=input.a ** 0.5)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)


# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringsToIntsInput) -> StringsToIntsOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(StringsToIntsInput) -> StringsToIntsOutput")
    ascii_values = [ord(char) for char in input.string]
    return StringsToIntsOutput(ascii_values=ascii_values)

@mcp.tool()
def int_list_to_exponential_sum(input: ExpSumInput) -> ExpSumOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(ExpSumInput) -> ExpSumOutput")
    result = sum(math.exp(i) for i in input.int_list)
    return ExpSumOutput(result=result)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

def fetch_ipl_match_reports():
    """
    Fetches match reports for all matches in the given IPL season from IPL Website.
    Returns a list of dicts: [{"title": ..., "report": ..., "url": ...}, ...]
    """
    
    reports = []
    match_reports = []
    
    # Get all HTML files from the ipl_matches directory
    for html_file in ipl_matches_dir.glob("*.html"):
        match_reports.append(html_file)
        
    for filepath in tqdm(match_reports, desc="Fetching match reports"):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            clean_text = re.sub(r'\\u[0-9A-Fa-f]{4}', '', content)
        markdown_content = trafilatura.extract(
            clean_text,
            include_comments=False,
            include_tables=True,
            include_images=False,
            output_format='markdown'
        ) or ""

        reports.append({"title": filepath.name.split(".")[0], "report": markdown_content, "file": filepath.name})
    # print(f"\nMatch Reports : {reports}")
    
    return reports

def build_faiss_index_from_reports(reports):
    """
    Given a list of match reports, build a FAISS index and save metadata.
    """
    embeddings = []
    metadata = []
    for i, report in enumerate(reports):
        for chunk in chunk_text(report["report"]):
            emb = get_embedding(chunk)
            embeddings.append(emb)
            metadata.append({
                "chunk": chunk,
                "doc": report["title"],
                "file": report["file"],
                "chunk_id": i
            })
    embeddings = np.stack(embeddings)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss_dir = ROOT / "faiss_index"
    faiss_dir.mkdir(exist_ok=True)
    faiss.write_index(index, str(faiss_dir / "index.bin"))
    (faiss_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

def sync_reports():
    """Synchronzie files from IPL Website to local"""
    url = "https://www.iplt20.com/news/match-reports"

    # Add headers to pretend we are a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/112.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all 'a' tags with href
    links = soup.find_all("a", href=True)
    match_report_links = set()
    for link in links:
        href = link['href']
        if 'match-report' in href and href.startswith("https://www.iplt20.com/news") and "/tata-ipl-2025-match-" in href:
            if href.startswith('/'):
                full_link = "https://www.espncricinfo.com" + href
            else:
                full_link = href
            
            file_name = f"{full_link.split("/")[-1]}.html"
            if file_name not in os.listdir(ipl_matches_dir):
                match_report_links.add(full_link)
    new_reports = list(match_report_links)
    if not match_report_links:
        mcp_log("SKIP", f"No New Match Reports to update")
    else:
        mcp_log("INFO", f"Reports Download Pending :  {new_reports}")
        download_reports(new_reports)

def process_documents():
    """Process documents and create FAISS index"""
    mcp_log("INFO", "Indexing documents with MarkItDown...")
    ROOT = Path(__file__).parent.resolve()
    DOC_PATH = ROOT / "ipl_matches"
    INDEX_CACHE = ROOT / "faiss_index"
    INDEX_CACHE.mkdir(exist_ok=True)
    INDEX_FILE = INDEX_CACHE / "index.bin"
    METADATA_FILE = INDEX_CACHE / "metadata.json"
    CACHE_FILE = INDEX_CACHE / "doc_index_cache.json"

    def file_hash(path):
        return hashlib.md5(Path(path).read_bytes()).hexdigest()

    CACHE_META = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    metadata = json.loads(METADATA_FILE.read_text()) if METADATA_FILE.exists() else []
    index = faiss.read_index(str(INDEX_FILE)) if INDEX_FILE.exists() else None
    all_embeddings = []
    converter = MarkItDown()

    for file in DOC_PATH.glob("*.*"):
        fhash = file_hash(file)
        if file.name in CACHE_META and CACHE_META[file.name] == fhash:
            mcp_log("SKIP", f"Skipping unchanged file: {file.name}")
            continue

        mcp_log("PROC", f"Processing: {file.name}")
        try:
            result = converter.convert(str(file))
            markdown_utf = result.text_content
            markdown = re.sub(r'\\u[0-9A-Fa-f]{4}', '', markdown_utf)
            chunks = list(chunk_text(markdown))
            embeddings_for_file = []
            new_metadata = []
            for i, chunk in enumerate(tqdm(chunks, desc=f"Embedding {file.name}")):
                embedding = get_embedding(chunk)
                embeddings_for_file.append(embedding)
                new_metadata.append({"doc": file.name, "chunk": chunk, "chunk_id": f"{file.stem}_{i}"})
            if embeddings_for_file:
                if index is None:
                    dim = len(embeddings_for_file[0])
                    index = faiss.IndexFlatL2(dim)
                index.add(np.stack(embeddings_for_file))
                metadata.extend(new_metadata)
            CACHE_META[file.name] = fhash
        except Exception as e:
            mcp_log("ERROR", f"Failed to process {file.name}: {e}")

    CACHE_FILE.write_text(json.dumps(CACHE_META, indent=2))
    METADATA_FILE.write_text(json.dumps(metadata, indent=2))
    if index and index.ntotal > 0:
        faiss.write_index(index, str(INDEX_FILE))
        mcp_log("SUCCESS", "Saved FAISS index and metadata")
    else:
        mcp_log("WARN", "No new documents or updates to process.")

def ensure_faiss_ready():
    from pathlib import Path
    index_path = ROOT / "faiss_index" / "index.bin"
    meta_path = ROOT / "faiss_index" / "metadata.json"
    if not (index_path.exists() and meta_path.exists()):
        mcp_log("INFO", "Index not found — running process_documents()...")
        process_documents()
    else:
        mcp_log("INFO", "Index already exists. Skipping regeneration.")


if __name__ == "__main__":
    print("STARTING THE SERVER AT AMAZING LOCATION")

    
    
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run() # Run without transport for dev server
    else:
        # Start the server in a separate thread
        import threading
        server_thread = threading.Thread(target=lambda: mcp.run(transport="stdio"))
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Process documents after server is running
        sync_reports()
        process_documents()
        # print(f"\nFetching IPL match reports...")
        # reports = fetch_ipl_match_reports()
        # print(f"\nFetched {len(reports)} reports. Building FAISS index...")
        # build_faiss_index_from_reports(reports)
        # print("\nFAISS index built and saved.\n")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
