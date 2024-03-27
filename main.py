import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import argparse
import os

def fetch_js_files(base_url, visited_urls=set(), download=False, find_endpoints=False):
    if base_url in visited_urls:
        return
    print(f"Visiting: {base_url}")
    visited_urls.add(base_url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    try:
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        with open('javascript_files.txt', 'a') as js_file, open('endpoints.txt', 'a') as endpoint_file:
            script_tags = soup.find_all('script')
            for tag in script_tags:
                src = tag.get('src')
                if src and src.endswith('.js'):
                    src = urljoin(base_url, src)
                    print(f"Found JavaScript: {src}")
                    js_file.write(src + '\n')

                    if download:
                        js_content = download_js_file(src, headers)
                        if find_endpoints and js_content:
                            endpoints = extract_endpoints(js_content, src)  # Pass the JS file URL as base_url
                            for endpoint in endpoints:
                                endpoint_file.write(endpoint + '\n')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and (href.startswith('http') or href.startswith('/')):
                full_url = urljoin(base_url, href)
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    fetch_js_files(full_url, visited_urls, download, find_endpoints)

    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")

def download_js_file(url, headers):
    try:
        response = requests.get(url, headers=headers)
        file_name = url.split('/')[-1]
        with open(file_name, 'w') as file:
            file.write(response.text)
        print(f"Downloaded {file_name}")
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def extract_endpoints(js_content, base_url):
    patterns = [
        r"https?://[^\s\"'<>()]+",
        r"(?<=['\"])/[^\s\"'<>()]*"
    ]
    raw_endpoints = set()
    for pattern in patterns:
        raw_endpoints.update(re.findall(pattern, js_content))

    endpoints = set()
    for endpoint in raw_endpoints:
        if endpoint.startswith('/'):
            endpoints.add(urljoin(base_url, endpoint))
        else:
            endpoints.add(endpoint)

    return endpoints

def process_input(input_arg, download=False, find_endpoints=False):
    if os.path.isfile(input_arg):
        with open(input_arg, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    fetch_js_files(url, download=download, find_endpoints=find_endpoints)
    else:
        fetch_js_files(input_arg, download=download, find_endpoints=find_endpoints)

def main():
    parser = argparse.ArgumentParser(description='Fetch JavaScript files from a URL or list of URLs in a text file.')
    parser.add_argument('input', type=str, help='A URL or a text file containing URLs')
    parser.add_argument('--download', action='store_true', help='Download JavaScript files')
    parser.add_argument('--find-endpoints', action='store_true', help='Find and save endpoints')

    args = parser.parse_args()
    process_input(args.input, download=args.download, find_endpoints=args.find_endpoints)

if __name__ == "__main__":
    main()
