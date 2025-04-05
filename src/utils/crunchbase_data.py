"""
Utility functions for retrieving and processing data from the Crunchbase API.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from src.data.apis.crunchbase import CrunchbaseAPIClient

logger = logging.getLogger(__name__)

# Initialize the Crunchbase API client
crunchbase_client = CrunchbaseAPIClient()

def get_startup_data(startup_name: str) -> Dict:
    """
    Get comprehensive data about a startup.
    
    Args:
        startup_name: Name of the startup to search for
        
    Returns:
        Dictionary containing startup data
    """
    try:
        # Search for the startup
        search_results = crunchbase_client.search_organizations(startup_name, limit=1)
        
        if not search_results:
            logger.warning(f"No results found for startup: {startup_name}")
            return {"name": startup_name, "error": "Startup not found"}
        
        startup_uuid = search_results[0]["identifier"]["uuid"]
        
        # Get detailed startup information
        profile = crunchbase_client.get_organization(startup_uuid)
        funding_rounds = crunchbase_client.get_organization_funding_rounds(startup_uuid)
        people = crunchbase_client.get_organization_people(startup_uuid)
        
        # Combine all data
        startup_data = {
            "profile": profile,
            "funding_rounds": funding_rounds,
            "people": people
        }
        
        return startup_data
    
    except Exception as e:
        logger.error(f"Error retrieving data for startup {startup_name}: {e}")
        return {"name": startup_name, "error": str(e)}

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
        search_results = crunchbase_client.search_investors(investor_name, limit=1)
        
        if not search_results:
            logger.warning(f"No results found for investor: {investor_name}")
            return {"name": investor_name, "error": "Investor not found"}
        
        investor_uuid = search_results[0]["identifier"]["uuid"]
        
        # Get detailed investor information
        profile = crunchbase_client.get_investor(investor_uuid)
        investments = crunchbase_client.get_investor_investments(investor_uuid)
        
        # Combine all data
        investor_data = {
            "profile": profile,
            "investments": investments
        }
        
        return investor_data
    
    except Exception as e:
        logger.error(f"Error retrieving data for investor {investor_name}: {e}")
        return {"name": investor_name, "error": str(e)}

def get_recent_funding_rounds(investment_type: Optional[str] = None, 
                             limit: int = 10) -> List[Dict]:
    """
    Get recent funding rounds matching specified criteria.
    
    Args:
        investment_type: Type of investment (e.g., "seed", "series_a", "series_b")
        limit: Maximum number of funding rounds to return
        
    Returns:
        List of recent funding rounds
    """
    try:
        filters = {}
        
        if investment_type:
            filters["investment_type"] = investment_type
        
        funding_rounds = crunchbase_client.search_funding_rounds(filters=filters, limit=limit)
        
        return funding_rounds
    
    except Exception as e:
        logger.error(f"Error retrieving recent funding rounds: {e}")
        return []

def get_recent_acquisitions(limit: int = 10) -> List[Dict]:
    """
    Get recent acquisitions.
    
    Args:
        limit: Maximum number of acquisitions to return
        
    Returns:
        List of recent acquisitions
    """
    try:
        acquisitions = crunchbase_client.search_acquisitions(limit=limit)
        
        return acquisitions
    
    except Exception as e:
        logger.error(f"Error retrieving recent acquisitions: {e}")
        return []

def get_startups_by_category(category: str, limit: int = 10) -> List[Dict]:
    """
    Get startups in a specific category.
    
    Args:
        category: Category name
        limit: Maximum number of startups to return
        
    Returns:
        List of startups in the category
    """
    try:
        filters = {
            "categories": category
        }
        
        startups = crunchbase_client.search_organizations("", filters=filters, limit=limit)
        
        return startups
    
    except Exception as e:
        logger.error(f"Error retrieving startups in category {category}: {e}")
        return []

def get_funding_trends(days: int = 90) -> Dict:
    """
    Analyze funding trends over a specified period.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Dictionary containing funding trend analysis
    """
    try:
        # Get recent funding rounds
        funding_rounds = crunchbase_client.search_funding_rounds(limit=100)
        
        # Analyze by investment type
        investment_types = {}
        for round in funding_rounds:
            investment_type = round.get("investment_type", "unknown")
            if investment_type not in investment_types:
                investment_types[investment_type] = {
                    "count": 0,
                    "total_raised": 0
                }
            
            investment_types[investment_type]["count"] += 1
            
            money_raised = round.get("money_raised", {}).get("value_usd", 0)
            if money_raised:
                investment_types[investment_type]["total_raised"] += money_raised
        
        # Calculate averages
        for investment_type, data in investment_types.items():
            if data["count"] > 0:
                data["average_raised"] = data["total_raised"] / data["count"]
        
        return {
            "period_days": days,
            "total_rounds": len(funding_rounds),
            "investment_types": investment_types
        }
    
    except Exception as e:
        logger.error(f"Error analyzing funding trends: {e}")
        return {"error": str(e)}