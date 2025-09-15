from typing import Dict, List
from openai import OpenAI
import os

# Initialize OpenAI client only if API key is available
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key and api_key != "your_openai_api_key_here" else None

def calculate_fit_score(product, company, influencer) -> float:
    """
    Calculate comprehensive fit score between influencer and product/brand
    """
    try:
        print(f"Calculating fit score for {influencer.name}")
        
        # Base score components
        content_fit = calculate_content_fit(product, influencer)
        audience_fit = calculate_audience_fit(company, influencer)
        engagement_fit = calculate_engagement_fit(influencer)
        brand_alignment = calculate_brand_alignment(company, influencer)
        
        print(f"Content fit: {content_fit}, Audience fit: {audience_fit}, Engagement fit: {engagement_fit}, Brand alignment: {brand_alignment}")
        
        # Weighted combination (more lenient)
        fit_score = (
            content_fit * 0.2 +
            audience_fit * 0.2 +
            engagement_fit * 0.3 +
            brand_alignment * 0.3
        )
        
        # Boost score to be more lenient
        fit_score = min(1.0, fit_score + 0.2)
        
        print(f"Final fit score: {fit_score}")
        return min(1.0, max(0.0, fit_score))
        
    except Exception as e:
        print(f"Fit score calculation error: {e}")
        return 0.7  # Default good fit

def calculate_content_fit(product, influencer) -> float:
    """Calculate how well influencer's content matches the product"""
    if not influencer.content_categories or not product.category:
        return 0.6  # More lenient default
    
    # Direct category match
    if product.category.lower() in [cat.lower() for cat in influencer.content_categories]:
        return 0.9
    
    # Partial matches for related categories
    category_matches = {
        'beauty & fashion': ['lifestyle', 'fashion', 'beauty'],
        'technology': ['tech', 'gadgets', 'electronics', 'gaming'],
        'food & cooking': ['lifestyle', 'cooking', 'food'],
        'gaming': ['technology', 'entertainment'],
        'lifestyle': ['beauty & fashion', 'food & cooking', 'travel']
    }
    
    product_cat = product.category.lower()
    for inf_cat in influencer.content_categories:
        inf_cat_lower = inf_cat.lower()
        if product_cat in category_matches.get(inf_cat_lower, []) or inf_cat_lower in category_matches.get(product_cat, []):
            return 0.7
    
    # Keyword matching
    product_keywords = extract_keywords(product.name + " " + (product.description or ""))
    influencer_keywords = []
    
    # Extract keywords from influencer's content categories
    for category in influencer.content_categories:
        influencer_keywords.extend(extract_keywords(category))
    
    # Calculate keyword overlap
    common_keywords = set(product_keywords) & set(influencer_keywords)
    if len(product_keywords) > 0:
        keyword_score = len(common_keywords) / len(product_keywords)
    else:
        keyword_score = 0.0
    
    return min(0.8, keyword_score)

def calculate_audience_fit(company, influencer) -> float:
    """Calculate how well influencer's audience matches company's target audience"""
    if not company.target_audience or not influencer.audience_demographics:
        return 0.5
    
    # Use AI to analyze audience alignment
    try:
        audience_analysis = analyze_audience_alignment(
            company.target_audience,
            influencer.audience_demographics
        )
        return audience_analysis.get('alignment_score', 0.5)
    except:
        return 0.5

def calculate_engagement_fit(influencer) -> float:
    """Calculate engagement quality score"""
    engagement_rate = influencer.engagement_rate or 0.0
    
    # Normalize engagement rate (typical range: 0.01 to 0.1)
    if engagement_rate > 0.1:
        return 1.0
    elif engagement_rate > 0.05:
        return 0.8
    elif engagement_rate > 0.02:
        return 0.6
    elif engagement_rate > 0.01:
        return 0.4
    else:
        return 0.2

def calculate_brand_alignment(company, influencer) -> float:
    """Calculate brand values and tone alignment"""
    if not company.brand_values or not influencer.content_categories:
        return 0.5
    
    # Use AI to analyze brand alignment
    try:
        brand_analysis = analyze_brand_alignment(
            company.brand_values,
            company.brand_keywords or [],
            influencer.content_categories,
            influencer.description or ""
        )
        return brand_analysis.get('alignment_score', 0.5)
    except:
        return 0.5

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text"""
    import re
    # Simple keyword extraction
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
    return [word for word in words if word not in stop_words and len(word) > 2]

def analyze_audience_alignment(target_audience: str, influencer_demographics: Dict) -> Dict:
    """Use AI to analyze audience alignment"""
    try:
        prompt = f"""
        Analyze how well this influencer's audience matches the target audience. Return a JSON response with:
        
        {{
            "alignment_score": 0.0-1.0,
            "match_reasons": ["reason1", "reason2"],
            "mismatch_reasons": ["reason1", "reason2"]
        }}
        
        Target Audience: {target_audience}
        Influencer Demographics: {influencer_demographics}
        """
        
        if not client:
            return {"alignment_score": 0.7, "match_reasons": ["Content category match"], "mismatch_reasons": []}
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in audience analysis and demographic matching. Analyze the alignment between target audience and influencer demographics. Always return valid JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    except:
        return {"alignment_score": 0.5, "match_reasons": [], "mismatch_reasons": []}

def analyze_brand_alignment(brand_values: List[str], brand_keywords: List[str], 
                          content_categories: List[str], influencer_description: str) -> Dict:
    """Use AI to analyze brand alignment"""
    try:
        prompt = f"""
        Analyze how well this influencer's content and values align with the brand. Return a JSON response with:
        
        {{
            "alignment_score": 0.0-1.0,
            "match_reasons": ["reason1", "reason2"],
            "mismatch_reasons": ["reason1", "reason2"]
        }}
        
        Brand Values: {brand_values}
        Brand Keywords: {brand_keywords}
        Influencer Categories: {content_categories}
        Influencer Description: {influencer_description}
        """
        
        if not client:
            return {"alignment_score": 0.6, "match_reasons": ["Brand values alignment"], "mismatch_reasons": []}
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in brand alignment and influencer marketing. Analyze how well the influencer's content and values align with the brand. Always return valid JSON format."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    except:
        return {"alignment_score": 0.5, "match_reasons": [], "mismatch_reasons": []}

def estimate_influencer_price(avg_views: int, engagement_rate: float, cpm: float) -> float:
    """
    Estimate influencer pricing based on multiple factors
    """
    try:
        # Base price from CPM
        base_price = (avg_views / 1000) * cpm
        
        # Engagement multiplier
        engagement_multiplier = 1.0
        if engagement_rate > 0.05:  # High engagement
            engagement_multiplier = 1.3
        elif engagement_rate > 0.03:  # Medium engagement
            engagement_multiplier = 1.1
        elif engagement_rate < 0.01:  # Low engagement
            engagement_multiplier = 0.8
        
        # View count multiplier
        view_multiplier = 1.0
        if avg_views > 1000000:  # 1M+ views
            view_multiplier = 1.5
        elif avg_views > 100000:  # 100K+ views
            view_multiplier = 1.2
        elif avg_views < 10000:  # <10K views
            view_multiplier = 0.7
        
        # Calculate final price
        final_price = base_price * engagement_multiplier * view_multiplier
        
        # Add minimum price floor
        min_price = 50.0
        final_price = max(min_price, final_price)
        
        return round(final_price, 2)
        
    except Exception as e:
        print(f"Price estimation error: {e}")
        # Fallback calculation
        return round((avg_views / 1000) * 15.0, 2)

def calculate_roi_estimate(price: float, avg_views: int, conversion_rate: float = 0.02) -> Dict:
    """
    Calculate estimated ROI for influencer collaboration
    """
    try:
        # Estimate clicks (assume 2% of views become clicks)
        estimated_clicks = int(avg_views * 0.02)
        
        # Estimate conversions (assume 2% of clicks convert)
        estimated_conversions = int(estimated_clicks * conversion_rate)
        
        # Estimate revenue (assume $50 average order value)
        estimated_revenue = estimated_conversions * 50.0
        
        # Calculate ROI
        roi = ((estimated_revenue - price) / price) * 100 if price > 0 else 0
        
        return {
            'estimated_clicks': estimated_clicks,
            'estimated_conversions': estimated_conversions,
            'estimated_revenue': round(estimated_revenue, 2),
            'roi_percentage': round(roi, 1),
            'cost_per_conversion': round(price / max(1, estimated_conversions), 2)
        }
    except:
        return {
            'estimated_clicks': 0,
            'estimated_conversions': 0,
            'estimated_revenue': 0,
            'roi_percentage': 0,
            'cost_per_conversion': 0
        }
