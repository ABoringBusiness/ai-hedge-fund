"""
Crunchbase API client for accessing startup and investor data.
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

class CrunchbaseAPIClient:
    """
    Client for interacting with the Crunchbase API to retrieve data about
    startups, investors, funding rounds, and acquisitions.
    """
    
    BASE_URL = "https://api.crunchbase.com/api/v4"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Crunchbase API client.
        
        Args:
            api_key: Crunchbase API key. If not provided, will look for CRUNCHBASE_API_KEY in environment variables.
        """
        self.api_key = api_key or os.getenv("CRUNCHBASE_API_KEY")
        if not self.api_key:
            logger.warning("Crunchbase API key not found. API calls will fail.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-cb-user-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> Dict:
        """
        Make a request to the Crunchbase API.
        
        Args:
            endpoint: API endpoint to call
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            data: Request body for POST requests
            
        Returns:
            API response as a dictionary
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Always include the API key in params
        if params is None:
            params = {}
        
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
            logger.error(f"Error making request to Crunchbase API: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    def search_organizations(self, query: str, filters: Optional[Dict] = None, 
                           limit: int = 10) -> List[Dict]:
        """
        Search for organizations (companies, startups) in the Crunchbase database.
        
        Args:
            query: Search query
            filters: Additional filters (industry, location, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of organization data
        """
        data = {
            "field_ids": ["identifier", "name", "short_description", "website", 
                         "location_identifiers", "founded_on", "funding_total", 
                         "funding_stage", "categories"],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "name",
                    "operator_id": "contains",
                    "values": [query]
                }
            ],
            "limit": limit
        }
        
        if filters:
            for field, value in filters.items():
                data["query"].append({
                    "type": "predicate",
                    "field_id": field,
                    "operator_id": "eq",
                    "values": [value]
                })
        
        response = self._make_request("searches/organizations", method="POST", data=data)
        return response.get("entities", [])
    
    def get_organization(self, uuid: str) -> Dict:
        """
        Get detailed information about an organization by UUID.
        
        Args:
            uuid: Crunchbase UUID for the organization
            
        Returns:
            Organization data
        """
        params = {
            "field_ids": ["identifier", "name", "short_description", "long_description", 
                         "website", "linkedin", "twitter", "facebook", "location_identifiers", 
                         "founded_on", "closed_on", "num_employees_enum", "operating_status", 
                         "funding_total", "funding_stage", "categories", "category_groups"]
        }
        
        return self._make_request(f"entities/organizations/{uuid}", params=params)
    
    def get_organization_funding_rounds(self, uuid: str) -> List[Dict]:
        """
        Get funding rounds for an organization.
        
        Args:
            uuid: Crunchbase UUID for the organization
            
        Returns:
            List of funding rounds
        """
        data = {
            "field_ids": ["identifier", "name", "announced_on", "money_raised", 
                         "investment_type", "lead_investor_identifiers", 
                         "investor_identifiers", "series"],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "organization_identifier",
                    "operator_id": "eq",
                    "values": [uuid]
                }
            ],
            "limit": 100
        }
        
        response = self._make_request("searches/funding_rounds", method="POST", data=data)
        return response.get("entities", [])
    
    def get_organization_people(self, uuid: str) -> List[Dict]:
        """
        Get people associated with an organization.
        
        Args:
            uuid: Crunchbase UUID for the organization
            
        Returns:
            List of people
        """
        data = {
            "field_ids": ["identifier", "first_name", "last_name", "title", 
                         "started_on", "ended_on", "organization_identifier"],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "organization_identifier",
                    "operator_id": "eq",
                    "values": [uuid]
                }
            ],
            "limit": 100
        }
        
        response = self._make_request("searches/people", method="POST", data=data)
        return response.get("entities", [])
    
    def search_investors(self, query: str, filters: Optional[Dict] = None, 
                        limit: int = 10) -> List[Dict]:
        """
        Search for investors in the Crunchbase database.
        
        Args:
            query: Search query
            filters: Additional filters (type, location, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of investor data
        """
        data = {
            "field_ids": ["identifier", "name", "short_description", "website", 
                         "location_identifiers", "investor_type", "investment_count"],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "name",
                    "operator_id": "contains",
                    "values": [query]
                }
            ],
            "limit": limit
        }
        
        if filters:
            for field, value in filters.items():
                data["query"].append({
                    "type": "predicate",
                    "field_id": field,
                    "operator_id": "eq",
                    "values": [value]
                })
        
        response = self._make_request("searches/investors", method="POST", data=data)
        return response.get("entities", [])
    
    def get_investor(self, uuid: str) -> Dict:
        """
        Get detailed information about an investor by UUID.
        
        Args:
            uuid: Crunchbase UUID for the investor
            
        Returns:
            Investor data
        """
        params = {
            "field_ids": ["identifier", "name", "short_description", "long_description", 
                         "website", "linkedin", "twitter", "facebook", "location_identifiers", 
                         "investor_type", "investment_count", "founded_on"]
        }
        
        return self._make_request(f"entities/investors/{uuid}", params=params)
    
    def get_investor_investments(self, uuid: str) -> List[Dict]:
        """
        Get investments made by an investor.
        
        Args:
            uuid: Crunchbase UUID for the investor
            
        Returns:
            List of investments
        """
        data = {
            "field_ids": ["identifier", "name", "announced_on", "money_raised", 
                         "investment_type", "organization_identifier", "series"],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "investor_identifiers",
                    "operator_id": "includes",
                    "values": [uuid]
                }
            ],
            "limit": 100
        }
        
        response = self._make_request("searches/funding_rounds", method="POST", data=data)
        return response.get("entities", [])
    
    def search_funding_rounds(self, filters: Optional[Dict] = None, 
                             limit: int = 10) -> List[Dict]:
        """
        Search for funding rounds in the Crunchbase database.
        
        Args:
            filters: Filters (investment type, date range, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of funding round data
        """
        data = {
            "field_ids": ["identifier", "name", "announced_on", "money_raised", 
                         "investment_type", "lead_investor_identifiers", 
                         "investor_identifiers", "organization_identifier", "series"],
            "query": [],
            "limit": limit,
            "order": [
                {
                    "field_id": "announced_on",
                    "sort": "desc"
                }
            ]
        }
        
        if filters:
            for field, value in filters.items():
                data["query"].append({
                    "type": "predicate",
                    "field_id": field,
                    "operator_id": "eq",
                    "values": [value]
                })
        
        response = self._make_request("searches/funding_rounds", method="POST", data=data)
        return response.get("entities", [])
    
    def search_acquisitions(self, filters: Optional[Dict] = None, 
                           limit: int = 10) -> List[Dict]:
        """
        Search for acquisitions in the Crunchbase database.
        
        Args:
            filters: Filters (date range, price range, etc.)
            limit: Maximum number of results to return
            
        Returns:
            List of acquisition data
        """
        data = {
            "field_ids": ["identifier", "name", "announced_on", "price", 
                         "acquirer_identifier", "acquiree_identifier"],
            "query": [],
            "limit": limit,
            "order": [
                {
                    "field_id": "announced_on",
                    "sort": "desc"
                }
            ]
        }
        
        if filters:
            for field, value in filters.items():
                data["query"].append({
                    "type": "predicate",
                    "field_id": field,
                    "operator_id": "eq",
                    "values": [value]
                })
        
        response = self._make_request("searches/acquisitions", method="POST", data=data)
        return response.get("entities", [])
    
    def get_category_groups(self) -> List[Dict]:
        """
        Get all category groups in Crunchbase.
        
        Returns:
            List of category groups
        """
        response = self._make_request("autocompletes/category_groups")
        return response.get("entities", [])
    
    def get_categories(self, category_group_uuid: Optional[str] = None) -> List[Dict]:
        """
        Get categories in Crunchbase, optionally filtered by category group.
        
        Args:
            category_group_uuid: Optional UUID of category group to filter by
            
        Returns:
            List of categories
        """
        params = {}
        if category_group_uuid:
            params["category_group_uuids"] = category_group_uuid
        
        response = self._make_request("autocompletes/categories", params=params)
        return response.get("entities", [])