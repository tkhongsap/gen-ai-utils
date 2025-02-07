import requests
import xml.etree.ElementTree as ET
from time import sleep
from typing import List, Dict

ARXIV_API_URL = "http://export.arxiv.org/api/query"
SEARCH_QUERY = "all:physics"  # Example query for physics papers
MAX_RESULTS = 50
SORT_BY = "submittedDate"  # Alternatives: "relevance", "lastUpdatedDate"
SORT_ORDER = "descending"  # Alternatives: "ascending"

def fetch_arxiv_articles() -> List[Dict]:
    """Fetch articles from arXiv API with error handling and rate limiting"""
    params = {
        "search_query": SEARCH_QUERY,
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": SORT_BY,
        "sortOrder": SORT_ORDER
    }

    try:
        # Respect arXiv's API rate limiting
        sleep(3)
        response = requests.get(ARXIV_API_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Failed to fetch data from arXiv API: {e}")

    return parse_response(response.text)

def parse_response(xml_data: str) -> List[Dict]:
    """Parse arXiv API XML response into structured data"""
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        raise SystemExit(f"Failed to parse XML response: {e}")

    articles = []
    namespace = {'atom': 'http://www.w3.org/2005/Atom',
                 'arxiv': 'http://arxiv.org/schemas/atom'}

    for entry in root.findall('atom:entry', namespace):
        # Safe element access with fallbacks
        title_elem = entry.find('atom:title', namespace)
        id_elem = entry.find('atom:id', namespace)
        published_elem = entry.find('atom:published', namespace)
        updated_elem = entry.find('atom:updated', namespace)
        summary_elem = entry.find('atom:summary', namespace)
        
        article = {
            'title': title_elem.text.strip() if title_elem is not None else "No title",
            'id': id_elem.text.split('/')[-1] if id_elem is not None else "No ID",
            'published': published_elem.text if published_elem is not None else "No date",
            'updated': updated_elem.text if updated_elem is not None else "No update date",
            'summary': summary_elem.text.strip() if summary_elem is not None else "No abstract",
            'authors': [
                author.find('atom:name', namespace).text 
                for author in entry.findall('atom:author', namespace)
                if author.find('atom:name', namespace) is not None
            ],
            'categories': [
                cat.attrib.get('term', 'Uncategorized') 
                for cat in entry.findall('atom:category', namespace)
            ],
            'primary_category': (entry.find('arxiv:primary_category', namespace) or 
                                {}).get('term', 'Uncategorized'),
            'links': (lambda: {
                'abstract': next(
                    (link.attrib.get('href', '#') for link in entry.findall('atom:link', namespace)
                     if link.attrib.get('rel') == 'alternate'),
                    '#'
                ),
                'pdf': next(
                    (link.attrib.get('href', '#') for link in entry.findall('atom:link', namespace)
                     if link.attrib.get('title', '').lower() == 'pdf'),
                    '#'
                )
            })(),
        }
        
        # Optional fields
        comment = entry.find('arxiv:comment', namespace)
        if comment is not None:
            article['comment'] = comment.text
            
        doi = entry.find('arxiv:doi', namespace)
        if doi is not None:
            article['doi'] = doi.text
            
        articles.append(article)

    return articles

if __name__ == "__main__":
    try:
        articles = fetch_arxiv_articles()
        print(f"Successfully fetched {len(articles)} articles:")
        for idx, article in enumerate(articles, 1):
            print(f"\n{idx}. {article['title']}")
            print(f"   Authors: {', '.join(article['authors'])}")
            print(f"   Published: {article['published']}")
            print(f"   PDF: {article['links']['pdf']}")
    except Exception as e:
        print(f"Error: {e}")
