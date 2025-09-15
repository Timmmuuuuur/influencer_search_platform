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
    min_fit_score: 0.3
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <Head>
        <title>InfluencerAI - AI-Powered Creator Discovery</title>
        <meta name="description" content="AI-powered influencer discovery and outreach platform" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </Head>

      {/* Header */}
      <header className="bg-white/80 backdrop-blur-lg shadow-lg border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg blur opacity-75"></div>
                <TrendingUp className="relative h-8 w-8 text-white bg-gradient-to-r from-blue-600 to-purple-600 p-1.5 rounded-lg" />
              </div>
              <div className="ml-3">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">InfluencerAI</h1>
                <p className="text-xs text-gray-500 font-medium">AI-Powered Creator Discovery</p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              {selectedCompany && (
                <div className="flex items-center space-x-2 bg-blue-50 px-3 py-2 rounded-full">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span className="text-sm font-medium text-blue-700">{selectedCompany.name}</span>
                </div>
              )}
              {selectedProduct && (
                <div className="flex items-center space-x-2 bg-purple-50 px-3 py-2 rounded-full">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <span className="text-sm font-medium text-purple-700">{selectedProduct.name}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Steps */}
        <div className="mb-12">
          <div className="flex items-center justify-center space-x-8 max-w-4xl mx-auto">
            {[
              { key: 'company', label: 'Company Setup', icon: Users, color: 'from-blue-500 to-blue-600' },
              { key: 'product', label: 'Add Product', icon: Plus, color: 'from-green-500 to-green-600' },
              { key: 'search', label: 'Search Influencers', icon: Search, color: 'from-purple-500 to-purple-600' },
              { key: 'results', label: 'Review & Contact', icon: BarChart3, color: 'from-orange-500 to-orange-600' }
            ].map((step, index) => {
              const Icon = step.icon;
              const isActive = currentStep === step.key;
              const isCompleted = ['company', 'product', 'search', 'results'].indexOf(currentStep) > index;
              
              return (
                <div key={step.key} className="flex flex-col items-center">
                  <div className="relative mb-3">
                    {(isActive || isCompleted) && (
                      <div className={`absolute inset-0 bg-gradient-to-r ${step.color} rounded-full blur opacity-60 animate-pulse`}></div>
                    )}
                    <div className={`relative flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all duration-300 ${
                      isActive || isCompleted 
                        ? `bg-gradient-to-r ${step.color} border-transparent text-white shadow-lg transform scale-110` 
                        : 'bg-white border-gray-300 text-gray-400 hover:border-gray-400'
                    }`}>
                      <Icon className="h-6 w-6" />
                    </div>
                  </div>
                  <span className={`text-sm font-medium transition-colors duration-300 ${
                    isActive ? 'text-gray-900 font-semibold' : isCompleted ? 'text-gray-700' : 'text-gray-500'
                  }`}>
                    {step.label}
                  </span>
                  {index < 3 && (
                    <div className={`absolute top-6 left-1/2 w-24 h-0.5 transform translate-x-6 transition-colors duration-500 ${
                      isCompleted ? 'bg-gradient-to-r from-gray-400 to-gray-300' : 'bg-gray-200'
                    }`} style={{zIndex: -1}} />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white/70 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 p-8 transition-all duration-300 hover:shadow-3xl">
          {currentStep === 'company' && (
            <div className="animate-fade-in">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">Company Registration</h2>
                <p className="text-gray-600 max-w-2xl mx-auto">Let's start by setting up your company profile. We'll analyze your website to understand your brand and target audience.</p>
              </div>
              <div className="max-w-2xl mx-auto space-y-6">
                <div className="group">
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Company Name
                  </label>
                  <input
                    type="text"
                    value={companyForm.name}
                    onChange={(e) => setCompanyForm({...companyForm, name: e.target.value})}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 group-hover:border-gray-300"
                    placeholder="Enter your company name"
                  />
                </div>
                <div className="group">
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={companyForm.email}
                    onChange={(e) => setCompanyForm({...companyForm, email: e.target.value})}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 group-hover:border-gray-300"
                    placeholder="Enter your email address"
                  />
                </div>
                <div className="group">
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Website URL
                  </label>
                  <input
                    type="url"
                    value={companyForm.website}
                    onChange={(e) => setCompanyForm({...companyForm, website: e.target.value})}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 group-hover:border-gray-300"
                    placeholder="https://yourcompany.com"
                  />
                  <div className="mt-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                          <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                          </svg>
                        </div>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-blue-900">AI Brand Analysis</p>
                        <p className="text-sm text-blue-700 mt-1">We'll analyze your website to understand your brand, target audience, and create a tailored influencer matching strategy.</p>
                      </div>
                    </div>
                  </div>
                </div>
                <button
                  onClick={createCompany}
                  disabled={loading || !companyForm.name || !companyForm.email}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Creating Company...</span>
                    </>
                  ) : (
                    <>
                      <Users className="w-5 h-5" />
                      <span>Create Company & Analyze Brand</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'product' && (
            <div className="animate-fade-in">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent mb-3">Add Your Product</h2>
                <p className="text-gray-600 max-w-2xl mx-auto">Tell us about the product you want to promote. We'll use this information to find the perfect influencer matches.</p>
              </div>
              <div className="max-w-2xl mx-auto space-y-6">
                <div className="group">
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Product Name
                  </label>
                  <input
                    type="text"
                    value={productForm.name}
                    onChange={(e) => setProductForm({...productForm, name: e.target.value})}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:ring-4 focus:ring-green-100 transition-all duration-200 group-hover:border-gray-300"
                    placeholder="Enter your product name"
                  />
                </div>
                <div className="group">
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Product Description
                  </label>
                  <textarea
                    value={productForm.description}
                    onChange={(e) => setProductForm({...productForm, description: e.target.value})}
                    rows={4}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:ring-4 focus:ring-green-100 transition-all duration-200 group-hover:border-gray-300 resize-none"
                    placeholder="Describe your product, its benefits, and target audience..."
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="group">
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Category
                    </label>
                    <select
                      value={productForm.category}
                      onChange={(e) => setProductForm({...productForm, category: e.target.value})}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:ring-4 focus:ring-green-100 transition-all duration-200 group-hover:border-gray-300 appearance-none bg-white"
                    >
                      <option value="">Select category</option>
                      <option value="Technology">📱 Technology</option>
                      <option value="Beauty & Fashion">💄 Beauty & Fashion</option>
                      <option value="Gaming">🎮 Gaming</option>
                      <option value="Lifestyle">🌟 Lifestyle</option>
                      <option value="Food & Cooking">🍳 Food & Cooking</option>
                      <option value="Health & Fitness">💪 Health & Fitness</option>
                    </select>
                  </div>
                  <div className="group">
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Price Range
                    </label>
                    <select
                      value={productForm.price_range}
                      onChange={(e) => setProductForm({...productForm, price_range: e.target.value})}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-green-500 focus:ring-4 focus:ring-green-100 transition-all duration-200 group-hover:border-gray-300 appearance-none bg-white"
                    >
                      <option value="">Select price range</option>
                      <option value="Under $25">💵 Under $25</option>
                      <option value="$25-$50">💰 $25-$50</option>
                      <option value="$50-$100">💸 $50-$100</option>
                      <option value="$100-$250">💎 $100-$250</option>
                      <option value="$250+">👑 $250+</option>
                    </select>
                  </div>
                </div>
                <button
                  onClick={createProduct}
                  disabled={loading || !productForm.name || !productForm.description}
                  className="w-full bg-gradient-to-r from-green-600 to-blue-600 text-white py-4 px-6 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Adding Product...</span>
                    </>
                  ) : (
                    <>
                      <Plus className="w-5 h-5" />
                      <span>Add Product & Find Influencers</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'search' && (
            <div className="animate-fade-in">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">Search Parameters</h2>
                <p className="text-gray-600 max-w-2xl mx-auto">Fine-tune your search to find the most relevant influencers for your product.</p>
              </div>
              <div className="max-w-2xl mx-auto space-y-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="group">
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Maximum Results
                    </label>
                    <input
                      type="number"
                      value={searchParams.max_results}
                      onChange={(e) => setSearchParams({...searchParams, max_results: parseInt(e.target.value)})}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-200 group-hover:border-gray-300"
                      min="1"
                      max="50"
                    />
                    <p className="text-xs text-gray-500 mt-2">How many influencers to find (1-50)</p>
                  </div>
                  <div className="group">
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Minimum Fit Score
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="1"
                      value={searchParams.min_fit_score}
                      onChange={(e) => setSearchParams({...searchParams, min_fit_score: parseFloat(e.target.value)})}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-200 group-hover:border-gray-300"
                    />
                    <p className="text-xs text-gray-500 mt-2">Quality threshold (0.0 - 1.0)</p>
                  </div>
                </div>
                
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-2xl border border-purple-200">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                        <Search className="w-5 h-5 text-white" />
                      </div>
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-purple-900 mb-2">Search Summary</h3>
                      <div className="space-y-2 text-sm text-purple-700">
                        <p>🎯 <strong>Product:</strong> {selectedProduct?.name}</p>
                        <p>📂 <strong>Category:</strong> {selectedProduct?.category}</p>
                        <p>📊 <strong>Quality Threshold:</strong> {Math.round(searchParams.min_fit_score * 100)}% brand fit</p>
                        <p>🔢 <strong>Results:</strong> Up to {searchParams.max_results} influencers</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <button
                  onClick={searchInfluencers}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 px-6 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
                >
                  {loading ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Searching Influencers...</span>
                    </>
                  ) : (
                    <>
                      <Search className="w-5 h-5" />
                      <span>Find Perfect Influencers</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          )}

          {currentStep === 'results' && (
            <div className="animate-fade-in">
              <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-8 space-y-4 md:space-y-0">
                <div>
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-2">Influencer Results</h2>
                  <p className="text-gray-600">Found {influencers.length} perfect matches for your product</p>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={contactInfluencers}
                    className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-3 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 flex items-center space-x-2"
                  >
                    <Mail className="h-5 w-5" />
                    <span>Auto-Contact All</span>
                  </button>
                </div>
              </div>
              
              <div className="grid gap-6">
                {influencers.map((influencer) => (
                  <div key={influencer.id} className="bg-white/50 backdrop-blur-sm border-2 border-white/20 rounded-2xl p-6 hover:shadow-2xl hover:border-white/40 transition-all duration-300 transform hover:-translate-y-1">
                    <div className="flex justify-between items-start mb-6">
                      <div className="flex-1">
                        <h3 className="text-2xl font-bold text-gray-900 mb-1">{influencer.name}</h3>
                        <p className="text-gray-600 font-medium">{influencer.channel_title}</p>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className={`px-4 py-2 rounded-full text-sm font-semibold shadow-sm ${
                          influencer.status === 'approved' 
                            ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border border-green-200' 
                            : influencer.status === 'contacted'
                            ? 'bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-800 border border-blue-200'
                            : 'bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800 border border-yellow-200'
                        }`}>
                          {influencer.status}
                        </div>
                        {influencer.status === 'pending' && (
                          <button
                            onClick={() => approveInfluencer(influencer.match_id)}
                            className="p-2 text-green-600 hover:text-green-700 hover:bg-green-50 rounded-full transition-colors duration-200"
                          >
                            <CheckCircle className="h-6 w-6" />
                          </button>
                        )}
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                      <div className="text-center bg-gradient-to-br from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-100">
                        <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                          {influencer.subscriber_count.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-600 font-medium mt-1">Subscribers</div>
                      </div>
                      <div className="text-center bg-gradient-to-br from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-100">
                        <div className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                          {influencer.avg_views.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-600 font-medium mt-1">Avg Views</div>
                      </div>
                      <div className="text-center bg-gradient-to-br from-green-50 to-emerald-50 p-4 rounded-xl border border-green-100">
                        <div className="text-3xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                          {(influencer.engagement_rate * 100).toFixed(1)}%
                        </div>
                        <div className="text-sm text-gray-600 font-medium mt-1">Engagement</div>
                      </div>
                      <div className="text-center bg-gradient-to-br from-orange-50 to-red-50 p-4 rounded-xl border border-orange-100">
                        <div className="text-3xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                          {Math.round(influencer.fit_score * 100)}%
                        </div>
                        <div className="text-sm text-gray-600 font-medium mt-1">Fit Score</div>
                      </div>
                    </div>
                    
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
                      <div className="flex flex-wrap gap-2">
                        {influencer.content_categories.map((category, index) => (
                          <span key={index} className="px-3 py-1.5 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 text-sm font-medium rounded-full border border-gray-300 shadow-sm">
                            {category}
                          </span>
                        ))}
                      </div>
                      <div className="text-right bg-gradient-to-br from-green-50 to-emerald-50 p-4 rounded-xl border border-green-200">
                        <div className="text-3xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                          ${influencer.price_estimate.toLocaleString()}
                        </div>
                        <div className="text-sm text-gray-600 font-medium">Est. Price</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
      
      {/* Background decoration */}
      <div className="fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-1/2 -right-1/2 w-96 h-96 bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-1/2 -left-1/2 w-96 h-96 bg-gradient-to-br from-green-400/20 to-blue-400/20 rounded-full blur-3xl"></div>
      </div>
    </div>
  );
}
