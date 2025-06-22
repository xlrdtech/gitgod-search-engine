# 🔍 FastAPI Aggregate Search Engine

A powerful FastAPI-based aggregate search engine that allows you to search across multiple platforms using simple shortcuts. Search GitHub, Google, Perplexity, Product Hunt, and many more with a unified API.

## ✨ Features

- **25+ Search Engines**: Support for AI search engines, development platforms, social media, and educational sites
- **Single & Multi-Engine Search**: Search one engine or aggregate results from multiple engines
- **Category-Based Search**: Search all engines in a specific category (AI Search, Development, etc.)
- **Result Parsing**: Optional structured result extraction from HTML responses
- **Fast Async Operations**: Built with FastAPI and httpx for high performance
- **Interactive Documentation**: Auto-generated API docs with Swagger UI
- **Web Interface**: Simple HTML interface for easy testing

## 🚀 Quick Start

### Installation

1. **Clone or download the project**
```bash
cd /path/to/project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the server**
```bash
uvicorn main:app --reload
```

4. **Access the application**
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## 🔧 Available Search Engines

### AI Search Engines
| Shortcut | Engine | Description |
|----------|--------|--------------|
| `andi` | Andi Search | AI-powered search |
| `brave` | Brave Search | Privacy-focused search |
| `ds` | DeepSeek | AI search engine |
| `felo` | Felo AI | AI-powered search |
| `gg` | Google | Traditional Google search |
| `komo` | Komo.ai | AI search assistant |
| `p` | Perplexity AI | AI-powered research |
| `ph` | Phind | Developer-focused AI search |
| `you` | You.com | AI search engine |

### Development & Design
| Shortcut | Platform | Description |
|----------|----------|--------------|
| `gh` | GitHub | Code repositories |
| `pht` | Product Hunt | Product discovery |
| `tf` | Taaft | Design inspiration |
| `gw` | Godly.website | Web design showcase |
| `mb` | Mobbin | Mobile app designs |
| `v0` | v0.dev | AI-generated UI components |
| `sp` | Spline Community | 3D design community |

### Social & Entertainment
| Shortcut | Platform | Description |
|----------|----------|--------------|

| `x` | X.com (Twitter) | Social media search |

### Education
| Shortcut | Platform | Description |
|----------|----------|--------------|
| `ud` | Free Udemy | Free online courses |

## 📖 API Usage

### Single Engine Search
Search using one specific engine:

```bash
GET /search?q=YOUR_QUERY&engine=SHORTCUT
```

**Examples:**
```bash
# Search GitHub for Python projects
curl "http://localhost:8000/search?q=python&engine=gh"

# Search Perplexity for FastAPI tutorials
curl "http://localhost:8000/search?q=fastapi%20tutorial&engine=p"

# Search with result parsing
curl "http://localhost:8000/search?q=react&engine=gh&parse=true"
```

### Multi-Engine Search
Search across multiple engines simultaneously:

```bash
GET /multi-search?q=YOUR_QUERY&engines=ENGINE1,ENGINE2,ENGINE3
```

**Examples:**
```bash
# Search multiple AI engines
curl "http://localhost:8000/multi-search?q=machine%20learning&engines=p,you,gg"

# Search development platforms
curl "http://localhost:8000/multi-search?q=react%20components&engines=gh,v0,mb"
```

### Category Search
Search all engines in a specific category:

```bash
GET /category-search?q=YOUR_QUERY&category=CATEGORY_NAME
```

**Available Categories:**
- `AI Search`
- `Development`
- `Social & Entertainment`
- `Education`

**Examples:**
```bash
# Search all AI engines
curl "http://localhost:8000/category-search?q=artificial%20intelligence&category=AI%20Search"

# Search all development platforms
curl "http://localhost:8000/category-search?q=vue.js&category=Development"
```

### List Available Engines
Get information about all available engines:

```bash
GET /engines
```

## 🔧 Configuration

### Adding New Search Engines

To add a new search engine, modify the `SEARCH_ENGINES` dictionary in `main.py`:

```python
SEARCH_ENGINES = {
    # ... existing engines
    "new_shortcut": "https://example.com/search?q={}",
}
```

Also update the `ENGINE_CATEGORIES` if needed:

```python
ENGINE_CATEGORIES = {
    "Your Category": ["new_shortcut"],
    # ... existing categories
}
```

### Customizing Result Parsing

The `SearchResult.parse_results()` method can be extended for engine-specific parsing:

```python
def parse_results(self):
    if self.engine == 'your_engine':
        # Custom parsing logic for your engine
        pass
    else:
        # Default parsing logic
        pass
```

## 🌐 Response Format

### Single Search Response
```json
{
  "query": "python",
  "engine": "gh",
  "url": "https://github.com/search?q=python",
  "status_code": 200,
  "content": "HTML content...",
  "error": null
}
```

### Multi-Search Response
```json
{
  "query": "fastapi",
  "engines": ["gh", "gg"],
  "results": [
    {
      "engine": "gh",
      "url": "https://github.com/search?q=fastapi",
      "status_code": 200,
      "content_preview": "HTML preview...",
      "error": null
    }
  ]
}
```

### Parsed Results (with parse=true)
```json
{
  "query": "react",
  "engine": "gh",
  "url": "https://github.com/search?q=react",
  "status_code": 200,
  "results": [
    {
      "title": "facebook/react",
      "link": "https://github.com/facebook/react",
      "snippet": "A declarative, efficient, and flexible JavaScript library..."
    }
  ],
  "error": null
}
```

## 🛠️ Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running with Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t search-engine .
docker run -p 8000:8000 search-engine
```

## 🔒 Security Considerations

- **Rate Limiting**: Consider implementing rate limiting for production use
- **CORS**: Configure CORS settings based on your frontend requirements
- **Input Validation**: Query parameters are URL-encoded for safety
- **Timeout Handling**: Requests timeout after 10 seconds to prevent hanging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new search engines or improve existing functionality
4. Test your changes
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- HTTP client powered by [httpx](https://www.python-httpx.org/)
- HTML parsing with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

**Happy Searching! 🔍**