"""
PitchBook API client for accessing private company, investor, and deal data.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class PitchBookAPIClient:
    """
    Client for interacting with the PitchBook API to retrieve data about
    private companies, investors, deals, and market trends.
    """
    
    BASE_URL = "https://api.pitchbook.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the PitchBook API client.
        
        Args:
            api_key: PitchBook API key. If not provided, will look for PITCHBOOK_API_KEY in environment variables.
        """
        self.api_key = api_key or os.getenv("PITCHBOOK_API_KEY")
        if not self.api_key:
            logger.warning("PitchBook API key not found. API calls will fail.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> Dict:
        """
        Make a request to the PitchBook API.
        
        Args:
            endpoint: API endpoint to call
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            data: Request body for POST requests
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url, params=params)
            elif method == "POST":
                response = self.session.post(url, params=params, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to PitchBook API: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    def search_companies(self, query: str, filters: Optional[Dict] = None, 
                        limit: int = 10) -> List[Dict]:
        """
        Search for companies in the PitchBook database.
        
        Args:
            query: Search query
            filters: Additional filters (industry, location, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of company data
        """
        params = {
            "q": query,
            "limit": limit
        }
        
        if filters:
            params.update(filters)
        
        response = self._make_request("companies/search", params=params)
        return response.get("companies", [])
    
    def get_company_profile(self, company_id: str) -> Dict:
        """
        Get detailed profile information for a company.
        
        Args:
            company_id: PitchBook company ID
            
        Returns:
            Company profile data
        """
        return self._make_request(f"companies/{company_id}")
    
    def get_company_financials(self, company_id: str) -> Dict:
        """
        Get financial data for a company.
        
        Args:
            company_id: PitchBook company ID
            
        Returns:
            Company financial data
        """
        return self._make_request(f"companies/{company_id}/financials")
    
    def get_company_funding(self, company_id: str) -> List[Dict]:
        """
        Get funding rounds for a company.
        
        Args:
            company_id: PitchBook company ID
            
        Returns:
            List of funding rounds
        """
        response = self._make_request(f"companies/{company_id}/funding")
        return response.get("rounds", [])
    
    def search_investors(self, query: str, filters: Optional[Dict] = None, 
                        limit: int = 10) -> List[Dict]:
        """
        Search for investors in the PitchBook database.
        
        Args:
            query: Search query
            filters: Additional filters (type, location, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of investor data
        """
        params = {
            "q": query,
            "limit": limit
        }
        
        if filters:
            params.update(filters)
        
        response = self._make_request("investors/search", params=params)
        return response.get("investors", [])
    
    def get_investor_profile(self, investor_id: str) -> Dict:
        """
        Get detailed profile information for an investor.
        
        Args:
            investor_id: PitchBook investor ID
            
        Returns:
            Investor profile data
        """
        return self._make_request(f"investors/{investor_id}")
    
    def get_investor_portfolio(self, investor_id: str) -> List[Dict]:
        """
        Get portfolio companies for an investor.
        
        Args:
            investor_id: PitchBook investor ID
            
        Returns:
            List of portfolio companies
        """
        response = self._make_request(f"investors/{investor_id}/portfolio")
        return response.get("companies", [])
    
    def search_deals(self, filters: Optional[Dict] = None, 
                    limit: int = 10) -> List[Dict]:
        """
        Search for deals in the PitchBook database.
        
        Args:
            filters: Filters (deal type, date range, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of deal data
        """
        params = {"limit": limit}
        
        if filters:
            params.update(filters)
        
        response = self._make_request("deals/search", params=params)
        return response.get("deals", [])
    
    def get_deal_details(self, deal_id: str) -> Dict:
        """
        Get detailed information for a deal.
        
        Args:
            deal_id: PitchBook deal ID
            
        Returns:
            Deal details
        """
        return self._make_request(f"deals/{deal_id}")
    
    def get_market_trends(self, industry: Optional[str] = None, 
                         region: Optional[str] = None,
                         time_period: str = "1Y") -> Dict:
        """
        Get market trends and analytics.
        
        Args:
            industry: Industry filter
            region: Geographic region filter
            time_period: Time period for trends (1M, 3M, 6M, 1Y, 5Y)
            
        Returns:
            Market trend data
        """
        params = {"time_period": time_period}
        
        if industry:
            params["industry"] = industry
        
        if region:
            params["region"] = region
        
        return self._make_request("market/trends", params=params)
    
    def get_industry_comparables(self, company_id: str, 
                               limit: int = 10) -> List[Dict]:
        """
        Get comparable companies in the same industry.
        
        Args:
            company_id: PitchBook company ID
            limit: Maximum number of results to return
            
        Returns:
            List of comparable companies
        """
        params = {"limit": limit}
        
        response = self._make_request(f"companies/{company_id}/comparables", params=params)
        return response.get("companies", [])