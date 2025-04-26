import requests
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import time

def download_html(url, save_dir="downloaded_html", filename=None):
    """
    Download HTML content from the given URL and save it to a file.
    
    Args:
        url (str): The URL to download HTML from
        save_dir (str): Directory to save the HTML files
        filename (str, optional): Custom filename. If None, extract from URL
        
    Returns:
        tuple: (success status, filename or error message)
    """
    try:
        # Create headers to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        # Send request to get the content
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise exception for 4XX/5XX status codes
        
        # Create the directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            if path_parts and path_parts[-1]:
                filename = path_parts[-1]
                # Add .html extension if not present
                if not filename.endswith('.html'):
                    filename += '.html'
            else:
                # Use the domain if path is empty
                filename = f"{parsed_url.netloc.replace('.', '_')}.html"
        
        # Ensure the file path is valid
        filepath = os.path.join(save_dir, filename)
        
        # Write the content to the file
        with open(filepath, 'wb') as file:
            file.write(response.content)
        
        return True, filename
    
    except requests.exceptions.RequestException as e:
        return False, f"Error downloading {url}: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error with {url}: {str(e)}"

def download_multiple_html(urls, save_dir="downloaded_html", max_workers=5):
    """
    Download multiple HTML files concurrently.
    
    Args:
        urls (list): List of URLs to download
        save_dir (str): Directory to save the HTML files
        max_workers (int): Maximum number of concurrent downloads
        
    Returns:
        dict: Results with URLs as keys and (success, message) as values
    """
    results = {}
    
    print(f"Starting download of {len(urls)} HTML files...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_html, url, save_dir): url for url in urls}
        
        for future in future_to_url:
            url = future_to_url[future]
            try:
                success, message = future.result()
                results[url] = (success, message)
                
                if success:
                    print(f"✓ Downloaded: {url} -> {message}")
                else:
                    print(f"✗ Failed: {url} - {message}")
            
            except Exception as e:
                results[url] = (False, f"Error processing {url}: {str(e)}")
                print(f"✗ Error: {url} - {str(e)}")
    
    # Print summary
    elapsed_time = time.time() - start_time
    success_count = sum(1 for result in results.values() if result[0])
    
    print(f"\nDownload Summary:")
    print(f"- Total: {len(urls)} files")
    print(f"- Successful: {success_count} files")
    print(f"- Failed: {len(urls) - success_count} files")
    print(f"- Time taken: {elapsed_time:.2f} seconds")
    
    return results

# Example usage
def download_reports(urls_to_download):
    # List of URLs to download
    
    # Alternatively, read URLs from a file
    def read_urls_from_file(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    
    # Start the download process
    download_multiple_html(urls_to_download, save_dir="ipl_matches")