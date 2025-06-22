from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import asyncio
from typing import List, Optional, Dict, Any
from urllib.parse import quote_plus
import json
from bs4 import BeautifulSoup
import re

app = FastAPI(
    title="Aggregate Search Engine",
    description="A FastAPI-based aggregate search engine with multiple shortcuts",
    version="1.0.0"
)

# Search engine configurations
SEARCH_ENGINES = {
    # AI Search Engines
    "andi": "https://andisearch.com/search?q={}",
    "brave": "https://search.brave.com/search?q={}",
    "ds": "https://search.deepseek.com/search?q={}",
    "felo": "https://felo.ai/search?q={}",
    "gg": "https://www.google.com/search?q={}",
    "komo": "https://komo.ai/search?q={}",
    "p": "https://www.perplexity.ai/search?q={}",
    "ph": "https://www.phind.com/search?q={}",
    "you": "https://you.com/search?q={}",
    
    # Development & Design
    "gh": "https://github.com/search?q={}",
    "pht": "https://www.producthunt.com/search?q={}",
    "tf": "https://taaft.com/search?q={}",
    "gw": "https://godly.website/search?q={}",
    "mb": "https://mobbin.com/browse?q={}",
    "v0": "https://v0.dev/search?q={}",
    "sp": "https://community.spline.design/search?q={}",
    
    # Social & Entertainment
    "x": "https://x.com/search?q={}",
    
    # Education
    "ud": "https://www.udemy.com/courses/search/?q={}&price=price-free",
}

# Engine categories for better organization
ENGINE_CATEGORIES = {
    "AI Search": ["andi", "brave", "ds", "felo", "gg", "komo", "p", "ph", "you"],
    "Development": ["gh", "pht", "tf", "gw", "mb", "v0", "sp"],
    "Social & Entertainment": ["x"],
    "Education": ["ud"]
}

class SearchResult:
    def __init__(self, engine: str, url: str, status_code: int, content: str = "", error: str = ""):
        self.engine = engine
        self.url = url
        self.status_code = status_code
        self.content = content
        self.error = error
        self.parsed_results = []

    def parse_results(self):
        """Basic result parsing - can be extended for specific engines"""
        if self.status_code != 200 or not self.content:
            return
        
        try:
            soup = BeautifulSoup(self.content, 'html.parser')
            
            # Generic parsing - extract titles and links
            results = []
            
            # Common selectors for different engines
            selectors = {
                'github': {'title': 'a[data-testid="results-list"] .text-normal', 'link': 'a[data-testid="results-list"]'},
                'google': {'title': 'h3', 'link': 'a'},
                'generic': {'title': 'h1, h2, h3, h4', 'link': 'a'}
            }
            
            # Use appropriate selector based on engine
            if self.engine == 'gh':
                selector = selectors['github']
            elif self.engine == 'gg':
                selector = selectors['google']
            else:
                selector = selectors['generic']
            
            titles = soup.select(selector['title'])[:10]  # Limit to 10 results
            links = soup.select(selector['link'])[:10]
            
            for i, title in enumerate(titles):
                if i < len(links):
                    results.append({
                        'title': title.get_text(strip=True),
                        'link': links[i].get('href', ''),
                        'snippet': title.get_text(strip=True)[:200] + '...' if len(title.get_text(strip=True)) > 200 else title.get_text(strip=True)
                    })
            
            self.parsed_results = results
        except Exception as e:
            self.error = f"Parsing error: {str(e)}"

async def fetch_search_result(session: httpx.AsyncClient, engine: str, query: str) -> SearchResult:
    """Fetch search results from a single engine"""
    if engine not in SEARCH_ENGINES:
        return SearchResult(engine, "", 0, error="Unknown engine shortcut")
    
    url = SEARCH_ENGINES[engine].format(quote_plus(query))
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = await session.get(url, headers=headers, timeout=10.0)
        result = SearchResult(engine, url, response.status_code, response.text)
        result.parse_results()
        return result
        
    except httpx.TimeoutException:
        return SearchResult(engine, url, 0, error="Request timeout")
    except Exception as e:
        return SearchResult(engine, url, 0, error=str(e))

@app.get("/")
async def root():
    """Root endpoint with GitGod.ai interface"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GitGod.ai - AI-Powered Search Engine</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                background: #0d1117;
                color: #e6edf3;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }}
            
            .header {{
                background: #161b22;
                border-bottom: 1px solid #30363d;
                padding: 1rem 2rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}
            
            .logo {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 1.5rem;
                font-weight: 600;
                color: #58a6ff;
            }}
            
            .logo-icon {{
                width: 32px;
                height: 32px;
                background: linear-gradient(135deg, #58a6ff, #7c3aed);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
            }}
            
            .main-container {{
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 2rem;
                max-width: 800px;
                margin: 0 auto;
                width: 100%;
            }}
            
            .hero-section {{
                text-align: center;
                margin-bottom: 3rem;
            }}
            
            .hero-title {{
                font-size: 3rem;
                font-weight: 700;
                background: linear-gradient(135deg, #58a6ff, #7c3aed, #f78166);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1rem;
            }}
            
            .hero-subtitle {{
                font-size: 1.2rem;
                color: #8b949e;
                margin-bottom: 2rem;
            }}
            
            .search-container {{
                width: 100%;
                max-width: 600px;
                margin-bottom: 3rem;
            }}
            
            .search-box {{
                position: relative;
                background: #21262d;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 1rem;
                transition: all 0.2s ease;
            }}
            
            .search-box:hover {{
                border-color: #58a6ff;
                box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
            }}
            
            .search-input {{
                width: 100%;
                background: transparent;
                border: none;
                outline: none;
                color: #e6edf3;
                font-size: 1.1rem;
                padding: 0.5rem 0;
            }}
            
            .search-input::placeholder {{
                color: #8b949e;
            }}
            
            .search-actions {{
                display: flex;
                gap: 0.5rem;
                margin-top: 1rem;
                flex-wrap: wrap;
            }}
            
            .search-btn {{
                background: #238636;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                text-decoration: none;
                display: inline-block;
            }}
            
            .search-btn:hover {{
                background: #2ea043;
                transform: translateY(-1px);
            }}
            
            .search-btn.secondary {{
                background: #21262d;
                border: 1px solid #30363d;
                color: #e6edf3;
            }}
            
            .search-btn.secondary:hover {{
                background: #30363d;
                border-color: #58a6ff;
            }}
            
            .features-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                width: 100%;
                margin-bottom: 3rem;
            }}
            
            .feature-card {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 1.5rem;
                transition: all 0.2s ease;
            }}
            
            .feature-card:hover {{
                border-color: #58a6ff;
                transform: translateY(-2px);
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            }}
            
            .feature-icon {{
                font-size: 2rem;
                margin-bottom: 1rem;
            }}
            
            .feature-title {{
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #e6edf3;
            }}
            
            .feature-desc {{
                color: #8b949e;
                line-height: 1.5;
            }}
            
            .engines-section {{
                width: 100%;
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 2rem;
                margin-bottom: 2rem;
            }}
            
            .engines-title {{
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                color: #e6edf3;
                text-align: center;
            }}
            
            .category {{
                margin-bottom: 2rem;
            }}
            
            .category h3 {{
                color: #58a6ff;
                font-size: 1.1rem;
                margin-bottom: 0.75rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid #30363d;
            }}
            
            .engines {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
            }}
            
            .engine {{
                background: #21262d;
                color: #e6edf3;
                padding: 0.4rem 0.8rem;
                border-radius: 6px;
                font-size: 0.85rem;
                border: 1px solid #30363d;
                transition: all 0.2s ease;
            }}
            
            .engine:hover {{
                background: #30363d;
                border-color: #58a6ff;
            }}
            
            .footer {{
                text-align: center;
                padding: 2rem;
                color: #8b949e;
                border-top: 1px solid #30363d;
            }}
            
            .api-link {{
                color: #58a6ff;
                text-decoration: none;
                font-weight: 500;
            }}
            
            .api-link:hover {{
                text-decoration: underline;
            }}
            
            @media (max-width: 768px) {{
                .hero-title {{
                    font-size: 2rem;
                }}
                
                .main-container {{
                    padding: 1rem;
                }}
                
                .search-actions {{
                    justify-content: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">
                <div class="logo-icon">🚀</div>
                <span>GitGod.ai</span>
            </div>
            <a href="/docs" class="api-link">API Docs</a>
        </div>
        
        <div class="main-container">
            <div class="hero-section">
                <h1 class="hero-title">GitGod.ai</h1>
                <p class="hero-subtitle">AI-Powered Multi-Engine Search Platform</p>
            </div>
            
            <div class="search-container">
                <div class="search-box">
                    <input type="text" class="search-input" placeholder="Search across 25+ engines instantly..." id="searchInput">
                    <div class="search-actions">
                        <button class="search-btn" onclick="searchAll()">🚀 Search All Engines</button>
                        <button class="search-btn secondary" onclick="searchGitHub()">🐙 GitHub</button>
                        <button class="search-btn secondary" onclick="searchGoogle()">🔍 Google</button>
                        <button class="search-btn secondary" onclick="searchAI()">🤖 AI Search</button>
                    </div>
                </div>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Lightning Fast</div>
                    <div class="feature-desc">Search across 25+ engines simultaneously with optimized performance</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-title">Smart Categories</div>
                    <div class="feature-desc">AI, Development, Social, and Education engines organized intelligently</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔗</div>
                    <div class="feature-title">Browser Integration</div>
                    <div class="feature-desc">Add as custom search engine in Chrome, Firefox, and Safari</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🛠️</div>
                    <div class="feature-title">Developer API</div>
                    <div class="feature-desc">RESTful API with JSON responses for seamless integration</div>
                </div>
            </div>
            
            <div class="engines-section">
                <h2 class="engines-title">🔍 Available Search Engines</h2>
    """
    
    for category, engines in ENGINE_CATEGORIES.items():
        html_content += f"""
                <div class="category">
                    <h3>{category}</h3>
                    <div class="engines">
        """
        for engine in engines:
            html_content += f'<span class="engine">{engine}</span>'
        html_content += "</div></div>"
    
    html_content += """
            </div>
        </div>
        
        <div class="footer">
            <p>Powered by GitGod.ai • <a href="/docs" class="api-link">API Documentation</a> • <a href="/opensearch.xml" class="api-link">OpenSearch</a></p>
        </div>
        
        <script>
            function getSearchQuery() {
                const input = document.getElementById('searchInput');
                const query = input.value.trim();
                if (!query) {
                    alert('Please enter a search query');
                    return null;
                }
                return encodeURIComponent(query);
            }
            
            function searchAll() {
                const query = getSearchQuery();
                if (query) {
                    window.open(`/browser-search?q=${query}&engine=all`, '_blank');
                }
            }
            
            function searchGitHub() {
                const query = getSearchQuery();
                if (query) {
                    window.open(`/browser-search?q=${query}&engine=gh&redirect=true`, '_blank');
                }
            }
            
            function searchGoogle() {
                const query = getSearchQuery();
                if (query) {
                    window.open(`/browser-search?q=${query}&engine=gg&redirect=true`, '_blank');
                }
            }
            
            function searchAI() {
                const query = getSearchQuery();
                if (query) {
                    window.open(`/multi-search?q=${query}&engines=p,you,andi,felo&parse=true`, '_blank');
                }
            }
            
            // Enter key support
            document.getElementById('searchInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchAll();
                }
            });
            
            // Focus search input on page load
            document.addEventListener('DOMContentLoaded', function() {
                document.getElementById('searchInput').focus();
            });
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/search")
async def single_search(
    q: str = Query(..., description="Your search query"),
    engine: str = Query(..., description="Engine shortcut (e.g., 'gh', 'gg', 'you')"),
    parse: bool = Query(False, description="Whether to parse and extract structured results")
):
    """Search using a single engine"""
    async with httpx.AsyncClient() as client:
        result = await fetch_search_result(client, engine, q)
        
        response_data = {
            "query": q,
            "engine": result.engine,
            "url": result.url,
            "status_code": result.status_code,
            "error": result.error if result.error else None
        }
        
        if parse and result.parsed_results:
            response_data["results"] = result.parsed_results
        elif not parse:
            response_data["content"] = result.content[:1000] + "..." if len(result.content) > 1000 else result.content
        
        return response_data

@app.get("/multi-search")
async def multi_search(
    q: str = Query(..., description="Your search query"),
    engines: str = Query(..., description="Comma-separated engine shortcuts (e.g., 'gh,gg,you')"),
    parse: bool = Query(False, description="Whether to parse and extract structured results")
):
    """Search across multiple engines simultaneously"""
    engine_list = [engine.strip() for engine in engines.split(",")]
    
    # Validate engines
    invalid_engines = [engine for engine in engine_list if engine not in SEARCH_ENGINES]
    if invalid_engines:
        raise HTTPException(status_code=400, detail=f"Invalid engines: {invalid_engines}")
    
    async with httpx.AsyncClient() as client:
        tasks = [fetch_search_result(client, engine, q) for engine in engine_list]
        results = await asyncio.gather(*tasks)
        
        response_data = {
            "query": q,
            "engines": engine_list,
            "results": []
        }
        
        for result in results:
            result_data = {
                "engine": result.engine,
                "url": result.url,
                "status_code": result.status_code,
                "error": result.error if result.error else None
            }
            
            if parse and result.parsed_results:
                result_data["parsed_results"] = result.parsed_results
            elif not parse:
                result_data["content_preview"] = result.content[:500] + "..." if len(result.content) > 500 else result.content
            
            response_data["results"].append(result_data)
        
        return response_data

@app.get("/category-search")
async def category_search(
    q: str = Query(..., description="Your search query"),
    category: str = Query(..., description="Engine category (e.g., 'AI Search', 'Development')"),
    parse: bool = Query(False, description="Whether to parse and extract structured results")
):
    """Search across all engines in a specific category"""
    if category not in ENGINE_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Available: {list(ENGINE_CATEGORIES.keys())}")
    
    engines = ENGINE_CATEGORIES[category]
    engines_str = ",".join(engines)
    
    return await multi_search(q=q, engines=engines_str, parse=parse)

@app.get("/engines")
async def list_engines():
    """List all available search engines and categories"""
    return {
        "engines": SEARCH_ENGINES,
        "categories": ENGINE_CATEGORIES,
        "total_engines": len(SEARCH_ENGINES)
    }

@app.get("/browser-search")
async def browser_search(
    q: str = Query(..., description="Search query from browser"),
    engine: str = Query("all", description="Engine shortcut or 'all' for all engines"),
    redirect: bool = Query(False, description="Whether to redirect to single engine (only works with specific engine)")
):
    """Browser-compatible search endpoint for adding as custom search engine"""
    if engine == "all":
        # Search all engines and return aggregate results page
        search_links = []
        for eng_key, url_template in SEARCH_ENGINES.items():
            search_url = url_template.format(quote_plus(q))
            search_links.append({
                "engine": eng_key,
                "url": search_url,
                "name": get_engine_name(eng_key)
            })
        
        # Create HTML page with all search links
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GitGod.ai - Search Results for "{q}"</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                    background: #0d1117;
                    color: #e6edf3;
                    min-height: 100vh;
                    padding: 2rem;
                }}
                
                .header {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 2rem;
                    padding-bottom: 1rem;
                    border-bottom: 1px solid #30363d;
                }}
                
                .logo {{
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: #58a6ff;
                }}
                
                .logo-icon {{
                    width: 32px;
                    height: 32px;
                    background: linear-gradient(135deg, #58a6ff, #7c3aed);
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.2rem;
                }}
                
                .back-btn {{
                    background: #21262d;
                    color: #e6edf3;
                    border: 1px solid #30363d;
                    padding: 0.5rem 1rem;
                    border-radius: 6px;
                    text-decoration: none;
                    font-size: 0.9rem;
                    transition: all 0.2s ease;
                }}
                
                .back-btn:hover {{
                    background: #30363d;
                    border-color: #58a6ff;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                
                .search-header {{
                    text-align: center;
                    margin-bottom: 2rem;
                }}
                
                .search-title {{
                    font-size: 2rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #58a6ff, #7c3aed, #f78166);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 0.5rem;
                }}
                
                .search-query {{
                    font-size: 1.2rem;
                    color: #8b949e;
                    margin-bottom: 1.5rem;
                }}
                
                .open-all {{
                    text-align: center;
                    margin-bottom: 2rem;
                }}
                
                .open-all button {{
                    background: #238636;
                    color: white;
                    border: none;
                    padding: 1rem 2rem;
                    border-radius: 8px;
                    font-size: 1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }}
                
                .open-all button:hover {{
                    background: #2ea043;
                    transform: translateY(-1px);
                    box-shadow: 0 4px 12px rgba(46, 160, 67, 0.3);
                }}
                
                .category {{
                    margin: 2rem 0;
                }}
                
                .category-title {{
                    font-size: 1.3rem;
                    font-weight: 600;
                    color: #58a6ff;
                    margin-bottom: 1rem;
                    padding-bottom: 0.5rem;
                    border-bottom: 1px solid #30363d;
                }}
                
                .search-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                    gap: 1rem;
                }}
                
                .search-card {{
                    background: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 8px;
                    padding: 1rem;
                    transition: all 0.2s ease;
                }}
                
                .search-card:hover {{
                    border-color: #58a6ff;
                    transform: translateY(-2px);
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
                }}
                
                .engine-name {{
                    font-weight: 600;
                    color: #e6edf3;
                    margin-bottom: 0.5rem;
                    font-size: 1rem;
                }}
                
                .search-link {{
                    color: #58a6ff;
                    text-decoration: none;
                    font-size: 0.85rem;
                    word-break: break-all;
                    line-height: 1.4;
                }}
                
                .search-link:hover {{
                    text-decoration: underline;
                }}
                
                @media (max-width: 768px) {{
                    body {{
                        padding: 1rem;
                    }}
                    
                    .search-title {{
                        font-size: 1.5rem;
                    }}
                    
                    .search-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">
                    <div class="logo-icon">🚀</div>
                    <span>GitGod.ai</span>
                </div>
                <a href="/" class="back-btn">← Back to Home</a>
            </div>
            
            <div class="container">
                <div class="search-header">
                    <h1 class="search-title">Search Results</h1>
                    <div class="search-query">Query: "{q}"</div>
                </div>
                
                <div class="open-all">
                    <button onclick="openAllLinks()">🚀 Open All Search Results</button>
                </div>
        """
        
        # Group by categories
        for category, engines in ENGINE_CATEGORIES.items():
            html_content += f'<div class="category"><div class="category-title">{category}</div><div class="search-grid">'
            for engine in engines:
                if engine in SEARCH_ENGINES:
                    search_url = SEARCH_ENGINES[engine].format(quote_plus(q))
                    engine_name = get_engine_name(engine)
                    html_content += f"""
                    <div class="search-card">
                        <div class="engine-name">{engine_name}</div>
                        <a href="{search_url}" target="_blank" class="search-link">{search_url}</a>
                    </div>
                    """
            html_content += '</div></div>'
        
        html_content += """
                <script>
                function openAllLinks() {
                    const links = document.querySelectorAll('.search-link');
                    links.forEach(link => {
                        window.open(link.href, '_blank');
                    });
                }
                </script>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
    
    else:
        # Single engine search
        if engine not in SEARCH_ENGINES:
            engine = "gg"  # Default to Google if invalid engine
        
        search_url = SEARCH_ENGINES[engine].format(quote_plus(q))
        
        if redirect:
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url=search_url, status_code=302)
        else:
            return {"query": q, "engine": engine, "redirect_url": search_url}

def get_engine_name(engine_key: str) -> str:
    """Get human-readable name for engine"""
    engine_names = {
        "andi": "Andi Search",
        "brave": "Brave Search",
        "ds": "DeepSeek",
        "felo": "Felo AI",
        "gg": "Google",
        "komo": "Komo.ai",
        "p": "Perplexity AI",
        "ph": "Phind",
        "you": "You.com",
        "gh": "GitHub",
        "pht": "Product Hunt",
        "tf": "Taaft",
        "gw": "Godly.website",
        "mb": "Mobbin",
        "v0": "v0.dev",
        "sp": "Spline Community",

        "x": "X.com (Twitter)",
        "ud": "Free Udemy"
    }
    return engine_names.get(engine_key, engine_key.upper())

@app.get("/opensearch.xml")
async def opensearch_descriptor():
    """OpenSearch descriptor for browser integration"""
    xml_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
    <ShortName>Aggregate Search</ShortName>
    <Description>Search multiple engines with shortcuts</Description>
    <Tags>search aggregate multi-engine</Tags>
    <Contact>admin@localhost</Contact>
    <Url type="text/html" template="http://localhost:8001/browser-search?q={{searchTerms}}&amp;engine=gg"/>
    <Url type="application/x-suggestions+json" template="http://localhost:8001/suggestions?q={{searchTerms}}"/>
    <Image height="16" width="16" type="image/x-icon">data:image/x-icon;base64,AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///wAAAAA</Image>
</OpenSearchDescription>
    """.strip()
    
    from fastapi.responses import Response
    return Response(content=xml_content, media_type="application/opensearchdescription+xml")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "engines_available": len(SEARCH_ENGINES)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)