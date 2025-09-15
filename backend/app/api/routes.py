from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.models import Company, Product, Influencer, InfluencerMatch, Campaign
from app.services.scrape_brand import scrape_and_analyze_brand
from app.services.youtube_search import search_youtube_influencers, analyze_influencer
from app.services.send_email import send_outreach_email
from app.utils.fit_and_pricing import calculate_fit_score, estimate_influencer_price

router = APIRouter()

# Helper function to get database session
def get_db():
    from app.main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request/response
class CompanyCreate(BaseModel):
    name: str
    email: str
    website: Optional[str] = None

class ProductCreate(BaseModel):
    name: str
    description: str
    category: Optional[str] = None
    price_range: Optional[str] = None

class InfluencerSearchRequest(BaseModel):
    product_id: int
    max_results: int = 20
    min_fit_score: float = 0.5

class CampaignCreate(BaseModel):
    product_id: int
    name: str
    description: Optional[str] = None
    budget: Optional[float] = None
    target_fit_score: float = 0.7
    auto_contact: bool = True

# Company endpoints
@router.post("/companies/", response_model=dict)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    # Check if company already exists
    existing = db.query(Company).filter(Company.email == company.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company with this email already exists")
    
    # Create company
    db_company = Company(
        name=company.name,
        email=company.email,
        website=company.website
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    # If website provided, analyze brand
    if company.website:
        try:
            brand_analysis = await scrape_and_analyze_brand(company.website)
            db_company.brand_summary = brand_analysis.get('summary', '')
            db_company.brand_keywords = brand_analysis.get('keywords', [])
            db_company.target_audience = brand_analysis.get('target_audience', '')
            db_company.brand_values = brand_analysis.get('brand_values', [])
            db.commit()
        except Exception as e:
            print(f"Brand analysis error: {e}")
    
    return {
        "id": db_company.id,
        "name": db_company.name,
        "email": db_company.email,
        "website": db_company.website,
        "brand_summary": db_company.brand_summary,
        "brand_keywords": db_company.brand_keywords
    }

@router.get("/companies/{company_id}", response_model=dict)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {
        "id": company.id,
        "name": company.name,
        "email": company.email,
        "website": company.website,
        "brand_summary": company.brand_summary,
        "brand_keywords": company.brand_keywords,
        "target_audience": company.target_audience,
        "brand_values": company.brand_values
    }

# Product endpoints
@router.post("/products/", response_model=dict)
async def create_product(product: ProductCreate, company_id: int, db: Session = Depends(get_db)):
    # Verify company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_product = Product(
        company_id=company_id,
        name=product.name,
        description=product.description,
        category=product.category,
        price_range=product.price_range
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return {
        "id": db_product.id,
        "name": db_product.name,
        "description": db_product.description,
        "category": db_product.category,
        "price_range": db_product.price_range,
        "company_id": db_product.company_id
    }

@router.get("/companies/{company_id}/products", response_model=List[dict])
async def get_company_products(company_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.company_id == company_id).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "price_range": p.price_range,
            "created_at": p.created_at
        } for p in products
    ]

# Influencer search endpoint
@router.post("/influencers/search", response_model=List[dict])
async def search_influencers(request: InfluencerSearchRequest, db: Session = Depends(get_db)):
    # Get product details
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get company details for brand context
    company = db.query(Company).filter(Company.id == product.company_id).first()
    
    # Search YouTube influencers
    search_query = f"{product.name} {product.category or ''} review unboxing"
    youtube_results = await search_youtube_influencers(search_query, request.max_results)
    
    results = []
    for channel_data in youtube_results:
        # Check if influencer already exists
        existing_influencer = db.query(Influencer).filter(
            Influencer.channel_id == channel_data['channel_id']
        ).first()
        
        if existing_influencer:
            influencer = existing_influencer
        else:
            # Analyze new influencer
            influencer_data = await analyze_influencer(channel_data['channel_id'])
            influencer = Influencer(
                name=influencer_data.get('name', channel_data['name']),
                channel_id=channel_data['channel_id'],
                channel_title=influencer_data.get('title', ''),
                description=influencer_data.get('description', ''),
                subscriber_count=influencer_data.get('subscriber_count', 0),
                view_count=influencer_data.get('view_count', 0),
                video_count=influencer_data.get('video_count', 0),
                avg_views=influencer_data.get('avg_views', 0),
                engagement_rate=influencer_data.get('engagement_rate', 0.0),
                cpm=influencer_data.get('cpm', 15.0),
                content_categories=influencer_data.get('categories', []),
                audience_demographics=influencer_data.get('demographics', {}),
                last_analyzed=datetime.utcnow()
            )
            db.add(influencer)
            db.commit()
            db.refresh(influencer)
        
        # Calculate fit score
        fit_score = calculate_fit_score(
            product, company, influencer
        )
        
        # Only include if meets minimum fit score
        if fit_score >= request.min_fit_score:
            # Calculate price estimate
            price_estimate = estimate_influencer_price(
                influencer.avg_views, influencer.engagement_rate, influencer.cpm
            )
            
            # Create or update match record
            match = db.query(InfluencerMatch).filter(
                InfluencerMatch.influencer_id == influencer.id,
                InfluencerMatch.product_id == request.product_id
            ).first()
            
            if not match:
                match = InfluencerMatch(
                    influencer_id=influencer.id,
                    product_id=request.product_id,
                    fit_score=fit_score,
                    price_estimate=price_estimate,
                    status="pending"
                )
                db.add(match)
                db.commit()
            
            results.append({
                "id": influencer.id,
                "name": influencer.name,
                "channel_title": influencer.channel_title,
                "subscriber_count": influencer.subscriber_count,
                "avg_views": influencer.avg_views,
                "engagement_rate": influencer.engagement_rate,
                "fit_score": fit_score,
                "price_estimate": price_estimate,
                "content_categories": influencer.content_categories,
                "match_id": match.id,
                "status": match.status
            })
    
    # Sort by fit score descending
    results.sort(key=lambda x: x['fit_score'], reverse=True)
    
    return results

# Campaign endpoints
@router.post("/campaigns/", response_model=dict)
async def create_campaign(campaign: CampaignCreate, company_id: int, db: Session = Depends(get_db)):
    # Verify company and product exist
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    product = db.query(Product).filter(Product.id == campaign.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_campaign = Campaign(
        company_id=company_id,
        product_id=campaign.product_id,
        name=campaign.name,
        description=campaign.description,
        budget=campaign.budget,
        target_fit_score=campaign.target_fit_score,
        auto_contact=campaign.auto_contact
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return {
        "id": db_campaign.id,
        "name": db_campaign.name,
        "description": db_campaign.description,
        "budget": db_campaign.budget,
        "target_fit_score": db_campaign.target_fit_score,
        "auto_contact": db_campaign.auto_contact,
        "status": db_campaign.status
    }

# Influencer approval endpoint
@router.post("/influencers/{match_id}/approve")
async def approve_influencer(match_id: int, db: Session = Depends(get_db)):
    match = db.query(InfluencerMatch).filter(InfluencerMatch.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    match.status = "approved"
    db.commit()
    
    return {"message": "Influencer approved successfully"}

# Auto-contact influencers endpoint
@router.post("/campaigns/{campaign_id}/contact-influencers")
async def contact_influencers(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get approved matches above target fit score
    matches = db.query(InfluencerMatch).filter(
        InfluencerMatch.product_id == campaign.product_id,
        InfluencerMatch.fit_score >= campaign.target_fit_score,
        InfluencerMatch.status == "pending"
    ).all()
    
    contacted_count = 0
    for match in matches:
        try:
            # Send outreach email
            await send_outreach_email(match, campaign)
            match.status = "contacted"
            match.contacted_at = datetime.utcnow()
            contacted_count += 1
        except Exception as e:
            print(f"Failed to contact influencer {match.influencer_id}: {e}")
    
    db.commit()
    
    return {"message": f"Contacted {contacted_count} influencers"}
