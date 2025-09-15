import { useState, useEffect } from 'react';
import Head from 'next/head';
import { 
  Search, 
  Users, 
  TrendingUp, 
  DollarSign, 
  Star, 
  Mail, 
  CheckCircle,
  XCircle,
  ExternalLink,
  Plus,
  Settings,
  BarChart3
} from 'lucide-react';

interface Company {
  id: number;
  name: string;
  email: string;
  website: string;
  brand_summary: string;
  brand_keywords: string[];
}

interface Product {
  id: number;
  name: string;
  description: string;
  category: string;
  price_range: string;
  company_id: number;
}

interface Influencer {
  id: number;
  name: string;
  channel_title: string;
  subscriber_count: number;
  avg_views: number;
  engagement_rate: number;
  fit_score: number;
  price_estimate: number;
  content_categories: string[];
  match_id: number;
  status: string;
}

export default function Home() {
  const [currentStep, setCurrentStep] = useState<'company' | 'product' | 'search' | 'results'>('company');
  const [companies, setCompanies] = useState<Company[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [influencers, setInfluencers] = useState<Influencer[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useState({
    max_results: 20,
    min_fit_score: 0.5
  });

  // Company form state
  const [companyForm, setCompanyForm] = useState({
    name: '',
    email: '',
    website: ''
  });

  // Product form state
  const [productForm, setProductForm] = useState({
    name: '',
    description: '',
    category: '',
    price_range: ''
  });

  // Load companies on mount
  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      // In a real app, you'd fetch from API
      // For demo, we'll use mock data
      setCompanies([
        {
          id: 1,
          name: "TechGear Inc",
          email: "contact@techgear.com",
          website: "https://techgear.com",
          brand_summary: "Premium technology accessories and gadgets",
          brand_keywords: ["technology", "gadgets", "premium", "innovation"]
        }
      ]);
    } catch (error) {
      console.error('Error loading companies:', error);
    }
  };

  const createCompany = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/companies/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(companyForm)
      });
      
      if (response.ok) {
        const newCompany = await response.json();
        setCompanies([...companies, newCompany]);
        setSelectedCompany(newCompany);
        setCurrentStep('product');
        setCompanyForm({ name: '', email: '', website: '' });
      }
    } catch (error) {
      console.error('Error creating company:', error);
    }
    setLoading(false);
  };

  const createProduct = async () => {
    if (!selectedCompany) return;
    
    setLoading(true);
    try {
      const response = await fetch(`/api/products/?company_id=${selectedCompany.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productForm)
      });
      
      if (response.ok) {
        const newProduct = await response.json();
        setProducts([...products, newProduct]);
        setSelectedProduct(newProduct);
        setCurrentStep('search');
        setProductForm({ name: '', description: '', category: '', price_range: '' });
      }
    } catch (error) {
      console.error('Error creating product:', error);
    }
    setLoading(false);
  };

  const searchInfluencers = async () => {
    if (!selectedProduct) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/influencers/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: selectedProduct.id,
          ...searchParams
        })
      });
      
      if (response.ok) {
        const results = await response.json();
        setInfluencers(results);
        setCurrentStep('results');
      }
    } catch (error) {
      console.error('Error searching influencers:', error);
    }
    setLoading(false);
  };

  const approveInfluencer = async (matchId: number) => {
    try {
      const response = await fetch(`/api/influencers/${matchId}/approve`, {
        method: 'POST'
      });
      
      if (response.ok) {
        setInfluencers(influencers.map(inf => 
          inf.match_id === matchId ? { ...inf, status: 'approved' } : inf
        ));
      }
    } catch (error) {
      console.error('Error approving influencer:', error);
    }
  };

  const contactInfluencers = async () => {
    if (!selectedProduct) return;
    
    try {
      const response = await fetch(`/api/campaigns/1/contact-influencers`, {
        method: 'POST'
      });
      
      if (response.ok) {
        alert('Outreach emails sent to qualifying influencers!');
      }
    } catch (error) {
      console.error('Error contacting influencers:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Head>
        <title>Influencer Search Platform</title>
        <meta name="description" content="AI-powered influencer discovery and outreach platform" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-primary-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">InfluencerAI</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                {selectedCompany && `Company: ${selectedCompany.name}`}
              </div>
              <div className="text-sm text-gray-500">
                {selectedProduct && `Product: ${selectedProduct.name}`}
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-8">
            {[
              { key: 'company', label: 'Company Setup', icon: Users },
              { key: 'product', label: 'Add Product', icon: Plus },
              { key: 'search', label: 'Search Influencers', icon: Search },
              { key: 'results', label: 'Review & Contact', icon: BarChart3 }
            ].map((step, index) => {
              const Icon = step.icon;
              const isActive = currentStep === step.key;
              const isCompleted = ['company', 'product', 'search', 'results'].indexOf(currentStep) > index;
              
              return (
                <div key={step.key} className="flex items-center">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                    isActive || isCompleted 
                      ? 'bg-primary-600 border-primary-600 text-white' 
                      : 'bg-white border-gray-300 text-gray-400'
                  }`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className={`ml-2 text-sm font-medium ${
                    isActive ? 'text-primary-600' : 'text-gray-500'
                  }`}>
                    {step.label}
                  </span>
                  {index < 3 && (
                    <div className={`w-16 h-0.5 ml-4 ${
                      isCompleted ? 'bg-primary-600' : 'bg-gray-300'
                    }`} />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          {currentStep === 'company' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Company Registration</h2>
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name
                  </label>
                  <input
                    type="text"
                    value={companyForm.name}
                    onChange={(e) => setCompanyForm({...companyForm, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Enter your company name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={companyForm.email}
                    onChange={(e) => setCompanyForm({...companyForm, email: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Enter your email"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Website URL
                  </label>
                  <input
                    type="url"
                    value={companyForm.website}
                    onChange={(e) => setCompanyForm({...companyForm, website: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="https://yourcompany.com"
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    We'll analyze your website to understand your brand and target audience
                  </p>
                </div>
                <button
                  onClick={createCompany}
                  disabled={loading || !companyForm.name || !companyForm.email}
                  className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Creating Company...' : 'Create Company & Analyze Brand'}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'product' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Add Product</h2>
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Product Name
                  </label>
                  <input
                    type="text"
                    value={productForm.name}
                    onChange={(e) => setProductForm({...productForm, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Enter product name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    value={productForm.description}
                    onChange={(e) => setProductForm({...productForm, description: e.target.value})}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Describe your product"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Category
                    </label>
                    <select
                      value={productForm.category}
                      onChange={(e) => setProductForm({...productForm, category: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="">Select category</option>
                      <option value="Technology">Technology</option>
                      <option value="Beauty & Fashion">Beauty & Fashion</option>
                      <option value="Gaming">Gaming</option>
                      <option value="Lifestyle">Lifestyle</option>
                      <option value="Food & Cooking">Food & Cooking</option>
                      <option value="Health & Fitness">Health & Fitness</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Price Range
                    </label>
                    <select
                      value={productForm.price_range}
                      onChange={(e) => setProductForm({...productForm, price_range: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="">Select range</option>
                      <option value="Under $25">Under $25</option>
                      <option value="$25-$50">$25-$50</option>
                      <option value="$50-$100">$50-$100</option>
                      <option value="$100-$250">$100-$250</option>
                      <option value="$250+">$250+</option>
                    </select>
                  </div>
                </div>
                <button
                  onClick={createProduct}
                  disabled={loading || !productForm.name || !productForm.description}
                  className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Adding Product...' : 'Add Product & Search Influencers'}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'search' && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Search Parameters</h2>
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Max Results
                    </label>
                    <input
                      type="number"
                      value={searchParams.max_results}
                      onChange={(e) => setSearchParams({...searchParams, max_results: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      min="1"
                      max="50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Minimum Fit Score
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="1"
                      value={searchParams.min_fit_score}
                      onChange={(e) => setSearchParams({...searchParams, min_fit_score: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                </div>
                <div className="bg-blue-50 p-4 rounded-md">
                  <h3 className="font-medium text-blue-900 mb-2">Search Summary</h3>
                  <p className="text-sm text-blue-700">
                    Searching for influencers for <strong>{selectedProduct?.name}</strong> in the <strong>{selectedProduct?.category}</strong> category.
                    We'll find creators with at least {Math.round(searchParams.min_fit_score * 100)}% brand fit.
                  </p>
                </div>
                <button
                  onClick={searchInfluencers}
                  disabled={loading}
                  className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Searching Influencers...' : 'Search Influencers'}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'results' && (
            <div>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Influencer Results</h2>
                <div className="flex space-x-3">
                  <button
                    onClick={contactInfluencers}
                    className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 flex items-center"
                  >
                    <Mail className="h-4 w-4 mr-2" />
                    Auto-Contact All
                  </button>
                </div>
              </div>
              
              <div className="grid gap-6">
                {influencers.map((influencer) => (
                  <div key={influencer.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-gray-900">{influencer.name}</h3>
                        <p className="text-gray-600">{influencer.channel_title}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                          influencer.status === 'approved' 
                            ? 'bg-green-100 text-green-800' 
                            : influencer.status === 'contacted'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {influencer.status}
                        </div>
                        {influencer.status === 'pending' && (
                          <button
                            onClick={() => approveInfluencer(influencer.match_id)}
                            className="text-green-600 hover:text-green-700"
                          >
                            <CheckCircle className="h-5 w-5" />
                          </button>
                        )}
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-primary-600">
                          {influencer.subscriber_count.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-500">Subscribers</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-primary-600">
                          {influencer.avg_views.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-500">Avg Views</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-primary-600">
                          {(influencer.engagement_rate * 100).toFixed(1)}%
                        </div>
                        <div className="text-sm text-gray-500">Engagement</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-primary-600">
                          {Math.round(influencer.fit_score * 100)}%
                        </div>
                        <div className="text-sm text-gray-500">Fit Score</div>
                      </div>
                    </div>
                    
                    <div className="flex justify-between items-center">
                      <div className="flex flex-wrap gap-2">
                        {influencer.content_categories.map((category, index) => (
                          <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                            {category}
                          </span>
                        ))}
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-green-600">
                          ${influencer.price_estimate.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-500">Est. Price</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
