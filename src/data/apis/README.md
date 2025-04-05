# API Integrations

This directory contains API clients for external data sources used by the AI Hedge Fund.

## PitchBook API

The PitchBook API client provides access to comprehensive data on private companies, investors, deals, and market trends. This integration enables the AI Hedge Fund to make informed investment decisions in the private markets.

### Features

- **Company Data**: Search for private companies and retrieve detailed profiles, financials, and funding history
- **Investor Data**: Access information about investors, their profiles, and portfolio companies
- **Deal Data**: Search for and analyze recent deals across various sectors
- **Market Trends**: Get insights into industry trends and market dynamics
- **Comparables**: Find and analyze comparable companies in the same industry

### Usage

To use the PitchBook API, you need to set up your API key in the `.env` file:

```
PITCHBOOK_API_KEY=your_api_key_here
```

Then you can use the client in your code:

```python
from src.data.apis.pitchbook import PitchBookAPIClient

# Initialize the client
client = PitchBookAPIClient()

# Search for companies
companies = client.search_companies("Stripe")

# Get company profile
profile = client.get_company_profile("company_id")

# Get market trends
trends = client.get_market_trends(industry="Fintech")
```

For convenience, utility functions are provided in `src/utils/pitchbook_data.py` that combine multiple API calls to get comprehensive data:

```python
from src.utils.pitchbook_data import get_private_company_data, get_industry_analysis

# Get comprehensive data about a company
company_data = get_private_company_data("Stripe")

# Get industry analysis
industry_data = get_industry_analysis("Fintech")
```

### Integration with Analysts

The PitchBook data is particularly useful for the Private Equity and Venture Capital analyst agents, which can use this data to evaluate investment opportunities in private markets.