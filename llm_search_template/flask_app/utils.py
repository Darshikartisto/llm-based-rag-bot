import os
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory



load_dotenv()

SERPER_API_KEY = os.getenv('SERPER_API_KEY')
GOOGLE_API_KEY = os.getenv('AIzaSyDBO2z_rpB7JLpoZpQvdFgfmmovucNo1hI')

genai.configure(api_key=GOOGLE_API_KEY)


def search_articles(query):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "num": 10})
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        search_results = response.json()
        articles = [
            {
                'url': result.get('link', ''),
                'title': result.get('title', ''),
                'snippet': result.get('snippet', '')
            }
            for result in search_results.get('organic', [])[:5]
        ]
        return articles
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching articles from Serper API: {e}")


def fetch_article_content(url):
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "header", "footer", "meta", "svg"]):
            tag.decompose()

        # Try selecting content based on common selectors
        content_selectors = ['article', 'main', 'div.content', 'div.article-body', 'div#content', 'body']
        content = None
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                break

        if not content:
            content = soup.body

        paragraphs = content.find_all(['p', 'h1', 'h2', 'h3'])
        text_content = ' '.join([p.get_text(strip=True) for p in paragraphs])
        return text_content.strip()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching article content: {e}")
def concatenate_content(articles, max_size=5000):
    
    full_text = ""
    for article in articles:
        try:
            content = fetch_article_content(article['url'])
            full_text += f"\n\nTitle: {article['title']}\n"
            full_text += f"Snippet: {article['snippet']}\n"
            full_text += f"Content: {content}\n"
            if len(full_text) > max_size:
                break  # Stop adding content if we exceed the size limit
        except RuntimeError as e:
            full_text += f"\n\nTitle: {article['title']}\n"
            full_text += f"Snippet: {article['snippet']}\n"
            full_text += "Content: [Failed to fetch content]\n"
    return full_text


def generate_answer(content, query):
    """
    Generates a response using Gemini API based on the provided content and query.
    
    Args:
        content (str): Context information from searched articles
        query (str): User's original query
    
    Returns:
        str: Generated response from Gemini API
    """
    # Load environment variables if not already loaded
    load_dotenv()
    
    # Retrieve API key from environment variables
    api_key = os.getenv("OPEN_API_KEY")
    print(api_key)
    # Define the Gemini API URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyDBO2z_rpB7JLpoZpQvdFgfmmovucNo1hI"
    
    # Prepare the payload
    payload = {
        "contents": [
            {
                "parts": [

                    {
                        "text": f"""Context:
{content}

Query:
{query}

Please provide a detailed, precise, and expert-level response addressing the query based on the given context. 
If the context does not contain sufficient information, indicate that additional research may be needed."""
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
            "topP": 0.8,
            "topK": 10
        }
    }
    
   
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
       
        response = requests.post(url, headers=headers, json=payload)
        
       
        response.raise_for_status()
        
        
        response_json = response.json()
        
       
        if (response_json.get('candidates') and 
            response_json['candidates'][0].get('content') and 
            response_json['candidates'][0]['content'].get('parts')):
            
            generated_text = response_json['candidates'][0]['content']['parts'][0].get('text', '')
            return generated_text.strip() if generated_text else "No response generated."
        
        return "Unable to generate a response."
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request error: {e}")
    except KeyError as e:
        raise RuntimeError(f"Unexpected response format: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error generating content: {e}")