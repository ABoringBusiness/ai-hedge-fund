"""Constants and utilities related to real estate analysts configuration."""

from src.real_estate_agents.barbara_corcoran import barbara_corcoran_agent

# Define analyst configuration - single source of truth
REAL_ESTATE_ANALYST_CONFIG = {
    "barbara_corcoran": {
        "display_name": "Barbara Corcoran",
        "description": "The Queen of NYC Real Estate",
        "investing_style": "Focuses on location, market trends, and property potential with an emphasis on buyer psychology.",
        "agent_func": barbara_corcoran_agent,
        "type": "analyst",
        "order": 0,
    },
    "robert_kiyosaki": {
        "display_name": "Robert Kiyosaki",
        "description": "Rich Dad Poor Dad Author",
        "investing_style": "Focuses on cash flow and passive income with an emphasis on financial education and tax advantages.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 1,
    },
    "grant_cardone": {
        "display_name": "Grant Cardone",
        "description": "The 10X Real Estate Investor",
        "investing_style": "Focuses on large multifamily properties with an emphasis on scale and professional management.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 2,
    },
    "brandon_turner": {
        "display_name": "Brandon Turner",
        "description": "BiggerPockets Expert",
        "investing_style": "Focuses on house hacking and creative financing with an emphasis on the BRRRR method.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 3,
    },
    "chip_joanna_gaines": {
        "display_name": "Chip & Joanna Gaines",
        "description": "Fixer Upper Specialists",
        "investing_style": "Focuses on renovation potential and design value-add with an emphasis on character preservation.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 4,
    },
    "scott_mcgillivray": {
        "display_name": "Scott McGillivray",
        "description": "Income Property Host",
        "investing_style": "Focuses on rental property analysis with an emphasis on cash flow and tenant management.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 5,
    },
    "ryan_serhant": {
        "display_name": "Ryan Serhant",
        "description": "Luxury Market Specialist",
        "investing_style": "Focuses on high-end properties with an emphasis on premium positioning and emotional connection.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 6,
    },
    "nicole_curtis": {
        "display_name": "Nicole Curtis",
        "description": "Rehab Addict",
        "investing_style": "Focuses on historic properties with an emphasis on authentic restoration and preservation.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 7,
    },
    "dave_ramsey": {
        "display_name": "Dave Ramsey",
        "description": "Conservative Financial Advisor",
        "investing_style": "Focuses on debt-free investing with an emphasis on risk minimization and long-term wealth building.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 8,
    },
    "ben_mallah": {
        "display_name": "Ben Mallah",
        "description": "Self-Made Investor",
        "investing_style": "Focuses on distressed properties with an emphasis on forced appreciation and quick turnarounds.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 9,
    },
    "graham_stephan": {
        "display_name": "Graham Stephan",
        "description": "YouTube Investor",
        "investing_style": "Focuses on house hacking and frugality with an emphasis on multiple income streams and efficiency.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 10,
    },
    "cash_flow_analyst": {
        "display_name": "Cash Flow Analyst",
        "description": "Rental Income Specialist",
        "investing_style": "Focuses on rental income potential, operating expenses, and cash-on-cash returns.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 11,
    },
    "market_trend_analyst": {
        "display_name": "Market Trend Analyst",
        "description": "Neighborhood Growth Specialist",
        "investing_style": "Focuses on neighborhood trends, population growth, and appreciation potential.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 12,
    },
    "renovation_analyst": {
        "display_name": "Renovation Analyst",
        "description": "Property Improvement Specialist",
        "investing_style": "Focuses on renovation costs, potential value increases, and renovation ROI.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 13,
    },
    "risk_manager": {
        "display_name": "Risk Manager",
        "description": "Risk Assessment Specialist",
        "investing_style": "Focuses on market risks, property risks, and financial risks to set investment limits.",
        "agent_func": None,  # To be implemented
        "type": "analyst",
        "order": 14,
    },
}

# Derive ANALYST_ORDER from ANALYST_CONFIG for backwards compatibility
REAL_ESTATE_ANALYST_ORDER = [(config["display_name"], key) for key, config in sorted(REAL_ESTATE_ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])]


def get_real_estate_analyst_nodes():
    """Get the mapping of analyst keys to their (node_name, agent_func) tuples."""
    return {key: (f"{key}_agent", config["agent_func"]) for key, config in REAL_ESTATE_ANALYST_CONFIG.items() if config["agent_func"] is not None}


def get_real_estate_agents_list():
    """Get the list of real estate agents for API responses."""
    return [
        {
            "key": key,
            "display_name": config["display_name"],
            "description": config["description"],
            "investing_style": config["investing_style"],
            "order": config["order"]
        }
        for key, config in sorted(REAL_ESTATE_ANALYST_CONFIG.items(), key=lambda x: x[1]["order"])
    ]