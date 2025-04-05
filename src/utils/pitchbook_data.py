"""
Utility functions for retrieving and processing data from the PitchBook API.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from src.data.apis.pitchbook import PitchBookAPIClient

logger = logging.getLogger(__name__)

# Initialize the PitchBook API client
pitchbook_client = PitchBookAPIClient()

def get_private_company_data(company_name: str) -> Dict:
    """
    Get comprehensive data about a private company.
    
    Args:
        company_name: Name of the company to search for
        
    Returns:
        Dictionary containing company data
    """
    try:
        # Search for the company
        search_results = pitchbook_client.search_companies(company_name, limit=1)
        
        if not search_results:
            logger.warning(f"No results found for company: {company_name}")
            return {"name": company_name, "error": "Company not found"}
        
        company_id = search_results[0]["id"]
        
        # Get detailed company information
        profile = pitchbook_client.get_company_profile(company_id)
        financials = pitchbook_client.get_company_financials(company_id)
        funding = pitchbook_client.get_company_funding(company_id)
        
        # Combine all data
        company_data = {
            "profile": profile,
            "financials": financials,
            "funding": funding
        }
        
        return company_data
    
    except Exception as e:
        logger.error(f"Error retrieving data for company {company_name}: {e}")
        return {"name": company_name, "error": str(e)}

def get_investor_data(investor_name: str) -> Dict:
    """
    Get comprehensive data about an investor.
    
    Args:
        investor_name: Name of the investor to search for
        
    Returns:
        Dictionary containing investor data
    """
    try:
        # Search for the investor
        search_results = pitchbook_client.search_investors(investor_name, limit=1)
        
        if not search_results:
            logger.warning(f"No results found for investor: {investor_name}")
            return {"name": investor_name, "error": "Investor not found"}
        
        investor_id = search_results[0]["id"]
        
        # Get detailed investor information
        profile = pitchbook_client.get_investor_profile(investor_id)
        portfolio = pitchbook_client.get_investor_portfolio(investor_id)
        
        # Combine all data
        investor_data = {
            "profile": profile,
            "portfolio": portfolio
        }
        
        return investor_data
    
    except Exception as e:
        logger.error(f"Error retrieving data for investor {investor_name}: {e}")
        return {"name": investor_name, "error": str(e)}

def get_recent_deals(deal_type: Optional[str] = None, 
                    industry: Optional[str] = None,
                    limit: int = 10) -> List[Dict]:
    """
    Get recent deals matching specified criteria.
    
    Args:
        deal_type: Type of deal (e.g., "VC", "PE", "M&A")
        industry: Industry filter
        limit: Maximum number of deals to return
        
    Returns:
        List of recent deals
    """
    try:
        filters = {}
        
        if deal_type:
            filters["deal_type"] = deal_type
        
        if industry:
            filters["industry"] = industry
        
        deals = pitchbook_client.search_deals(filters=filters, limit=limit)
        
        # Get detailed information for each deal
        detailed_deals = []
        for deal in deals:
            deal_details = pitchbook_client.get_deal_details(deal["id"])
            detailed_deals.append(deal_details)
        
        return detailed_deals
    
    except Exception as e:
        logger.error(f"Error retrieving recent deals: {e}")
        return []

def get_industry_analysis(industry: str) -> Dict:
    """
    Get comprehensive analysis of an industry.
    
    Args:
        industry: Industry to analyze
        
    Returns:
        Dictionary containing industry analysis
    """
    try:
        # Get market trends for the industry
        trends = pitchbook_client.get_market_trends(industry=industry)
        
        # Get recent deals in the industry
        deals = get_recent_deals(industry=industry, limit=5)
        
        # Combine data
        analysis = {
            "industry": industry,
            "trends": trends,
            "recent_deals": deals
        }
        
        return analysis
    
    except Exception as e:
        logger.error(f"Error retrieving industry analysis for {industry}: {e}")
        return {"industry": industry, "error": str(e)}

def get_comparable_companies(company_name: str) -> List[Dict]:
    """
    Get comparable companies for a given company.
    
    Args:
        company_name: Name of the company
        
    Returns:
        List of comparable companies
    """
    try:
        # Search for the company
        search_results = pitchbook_client.search_companies(company_name, limit=1)
        
        if not search_results:
            logger.warning(f"No results found for company: {company_name}")
            return []
        
        company_id = search_results[0]["id"]
        
        # Get comparable companies
        comparables = pitchbook_client.get_industry_comparables(company_id)
        
        return comparables
    
    except Exception as e:
        logger.error(f"Error retrieving comparable companies for {company_name}: {e}")
        return []