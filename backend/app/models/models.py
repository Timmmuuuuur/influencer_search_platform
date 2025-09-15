from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    website = Column(String, nullable=True)
    brand_summary = Column(Text, nullable=True)
    brand_keywords = Column(JSON, nullable=True)  # AI-extracted keywords
    target_audience = Column(Text, nullable=True)
    brand_values = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", back_populates="company")
    campaigns = relationship("Campaign", back_populates="company")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=True)
    target_keywords = Column(JSON, nullable=True)  # Keywords for matching
    price_range = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="products")
    influencer_matches = relationship("InfluencerMatch", back_populates="product")

class Influencer(Base):
    __tablename__ = 'influencers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    channel_id = Column(String, unique=True, nullable=False)
    channel_title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    subscriber_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    video_count = Column(Integer, default=0)
    avg_views = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    cpm = Column(Float, default=15.0)
    email = Column(String, nullable=True)
    contact_info = Column(JSON, nullable=True)
    content_categories = Column(JSON, nullable=True)
    audience_demographics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_analyzed = Column(DateTime, nullable=True)
    
    # Relationships
    matches = relationship("InfluencerMatch", back_populates="influencer")

class InfluencerMatch(Base):
    __tablename__ = 'influencer_matches'
    id = Column(Integer, primary_key=True)
    influencer_id = Column(Integer, ForeignKey('influencers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    fit_score = Column(Float, nullable=False)
    price_estimate = Column(Float, nullable=False)
    match_reasons = Column(JSON, nullable=True)  # Why they match
    status = Column(String, default="pending")  # pending, approved, rejected, contacted
    contacted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    influencer = relationship("Influencer", back_populates="matches")
    product = relationship("Product", back_populates="influencer_matches")

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    budget = Column(Float, nullable=True)
    target_fit_score = Column(Float, default=0.7)
    auto_contact = Column(Boolean, default=True)
    status = Column(String, default="active")  # active, paused, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="campaigns")
