import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import re
from typing import Dict, List

# Initialize OpenAI client only if API key is available
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key and api_key != "your_openai_api_key_here" else None

async def scrape_and_analyze_brand(url: str) -> Dict:
    """
    Scrape website and perform comprehensive brand analysis using AI
    """
    try:
        # Scrape website content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        r = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Extract text content from various elements
        text_elements = []
        
        # Get main content
        for tag in ['h1', 'h2', 'h3', 'p', 'div']:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text().strip()
                if text and len(text) > 10:  # Filter out very short text
                    text_elements.append(text)
        
        # Combine and clean text
        full_text = " ".join(text_elements)[:5000]  # Limit to 5000 chars
        
        # Extract meta information
        title = soup.find('title')
        title_text = title.get_text() if title else ""
        
        description = soup.find('meta', attrs={'name': 'description'})
        description_text = description.get('content', '') if description else ""
        
        # Combine all text for analysis
        analysis_text = f"Title: {title_text}\nDescription: {description_text}\nContent: {full_text}"
        
        # AI Analysis
        analysis = await analyze_brand_with_ai(analysis_text)
        
        return {
            'summary': analysis.get('summary', ''),
            'keywords': analysis.get('keywords', []),
            'target_audience': analysis.get('target_audience', ''),
            'brand_values': analysis.get('brand_values', []),
            'content_categories': analysis.get('content_categories', []),
            'tone': analysis.get('tone', ''),
            'unique_selling_points': analysis.get('unique_selling_points', [])
        }
        
    except Exception as e:
        print(f"Brand analysis error: {e}")
        return {
            'summary': 'Brand analysis could not be completed.',
            'keywords': [],
            'target_audience': '',
            'brand_values': [],
            'content_categories': [],
            'tone': '',
            'unique_selling_points': []
        }

async def analyze_brand_with_ai(text: str) -> Dict:
    """
    Use OpenAI to analyze brand characteristics
    """
    try:
        prompt = f"""
        Analyze this brand's website content and provide a comprehensive brand profile. Return a JSON response with the following structure:
        
        {{
            "summary": "A 2-3 sentence summary of what this brand does and its value proposition",
            "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
            "target_audience": "Description of the primary target audience demographics and psychographics",
            "brand_values": ["value1", "value2", "value3"],
            "content_categories": ["category1", "category2", "category3"],
            "tone": "The brand's communication tone (e.g., professional, casual, friendly, authoritative)",
            "unique_selling_points": ["USP1", "USP2", "USP3"]
        }}
        
        Website content:
        {text}
        """
        
        if not client:
            return {
                'summary': 'AI analysis requires OpenAI API key configuration.',
                'keywords': ['technology', 'innovation', 'quality'],
                'target_audience': 'Tech-savvy consumers',
                'brand_values': ['innovation', 'quality', 'reliability'],
                'content_categories': ['Technology'],
                'tone': 'Professional',
                'unique_selling_points': ['Cutting-edge technology', 'Superior quality']
            }
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert brand strategist and marketing analyst. Analyze the provided website content and extract key brand insights. Always return valid JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Parse JSON response
        import json
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"AI analysis error: {e}")
        return {
            'summary': 'AI analysis could not be completed.',
            'keywords': [],
            'target_audience': '',
            'brand_values': [],
            'content_categories': [],
            'tone': '',
            'unique_selling_points': []
        }
