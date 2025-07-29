from src.graph.state import AgentState, show_agent_reasoning
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import json
from typing_extensions import Literal
from src.utils.llm import call_llm
from src.utils.progress import progress
from src.utils.api_key import get_api_key_from_state
from src.tools.real_estate_api import (
    get_property_details,
    get_neighborhood_stats,
    get_comparable_properties,
    get_market_trends
)

class BarbaraCorcoran(BaseModel):
    signal: Literal["buy", "pass", "hold"]
    confidence: float
    reasoning: str


def barbara_corcoran_agent(state: AgentState, agent_id: str = "barbara_corcoran_agent"):
    """Analyzes properties using Barbara Corcoran's principles and LLM reasoning."""
    data = state["data"]
    properties = data["properties"]
    api_key = get_api_key_from_state(state, "REAL_ESTATE_API_KEY")
    
    # Collect all analysis for LLM reasoning
    analysis_data = {}
    corcoran_analysis = {}

    for property_id in properties:
        progress.update_status(agent_id, property_id, "Fetching property details")
        # Fetch required data
        property_details = get_property_details(property_id, api_key=api_key)
        
        progress.update_status(agent_id, property_id, "Analyzing neighborhood")
        neighborhood_stats = get_neighborhood_stats(property_details.zip_code, api_key=api_key)
        
        progress.update_status(agent_id, property_id, "Finding comparable properties")
        comps = get_comparable_properties(property_id, api_key=api_key)
        
        progress.update_status(agent_id, property_id, "Analyzing market trends")
        market_trends = get_market_trends(property_details.zip_code, api_key=api_key)
        
        progress.update_status(agent_id, property_id, "Analyzing location quality")
        location_analysis = analyze_location(neighborhood_stats, market_trends)
        
        progress.update_status(agent_id, property_id, "Analyzing property potential")
        potential_analysis = analyze_property_potential(property_details, comps)
        
        progress.update_status(agent_id, property_id, "Analyzing market timing")
        market_timing_analysis = analyze_market_timing(market_trends)
        
        progress.update_status(agent_id, property_id, "Analyzing unique selling points")
        usp_analysis = analyze_unique_selling_points(property_details, comps)
        
        # Calculate total score
        total_score = (
            location_analysis["score"] + 
            potential_analysis["score"] + 
            market_timing_analysis["score"] + 
            usp_analysis["score"]
        )
        
        # Update max possible score calculation
        max_possible_score = (
            location_analysis["max_score"] + 
            potential_analysis["max_score"] + 
            market_timing_analysis["max_score"] + 
            usp_analysis["max_score"]
        )

        # Combine all analysis results for LLM evaluation
        analysis_data[property_id] = {
            "property_id": property_id,
            "score": total_score,
            "max_score": max_possible_score,
            "property_details": property_details,
            "location_analysis": location_analysis,
            "potential_analysis": potential_analysis,
            "market_timing_analysis": market_timing_analysis,
            "usp_analysis": usp_analysis,
            "neighborhood_stats": neighborhood_stats,
            "comparable_properties": comps,
            "market_trends": market_trends
        }

        progress.update_status(agent_id, property_id, "Generating Barbara Corcoran analysis")
        corcoran_output = generate_corcoran_output(
            property_id=property_id,
            analysis_data=analysis_data,
            state=state,
            agent_id=agent_id,
        )

        # Store analysis in consistent format with other agents
        corcoran_analysis[property_id] = {
            "signal": corcoran_output.signal,
            "confidence": corcoran_output.confidence,
            "reasoning": corcoran_output.reasoning,
        }

        progress.update_status(agent_id, property_id, "Done", analysis=corcoran_output.reasoning)

    # Create the message
    message = HumanMessage(content=json.dumps(corcoran_analysis), name=agent_id)

    # Show reasoning if requested
    if state["metadata"]["show_reasoning"]:
        show_agent_reasoning(corcoran_analysis, agent_id)

    # Add the signal to the analyst_signals list
    state["data"]["analyst_signals"][agent_id] = corcoran_analysis

    progress.update_status(agent_id, None, "Done")

    return {"messages": [message], "data": state["data"]}


def analyze_location(neighborhood_stats: dict, market_trends: dict) -> dict:
    """Analyze location quality based on Barbara Corcoran's criteria."""
    if not neighborhood_stats or not market_trends:
        return {"score": 0, "max_score": 10, "details": "Insufficient location data"}

    score = 0
    max_score = 10
    reasoning = []

    # Check school ratings
    if neighborhood_stats.get("school_rating") and neighborhood_stats["school_rating"] > 8:
        score += 2
        reasoning.append(f"Excellent schools with rating of {neighborhood_stats['school_rating']}/10")
    elif neighborhood_stats.get("school_rating") and neighborhood_stats["school_rating"] > 6:
        score += 1
        reasoning.append(f"Good schools with rating of {neighborhood_stats['school_rating']}/10")
    else:
        reasoning.append("Average or below average schools")

    # Check crime rates
    if neighborhood_stats.get("crime_rate") and neighborhood_stats["crime_rate"] < 50:
        score += 2
        reasoning.append("Low crime rate area")
    elif neighborhood_stats.get("crime_rate") and neighborhood_stats["crime_rate"] < 100:
        score += 1
        reasoning.append("Moderate crime rate area")
    else:
        reasoning.append("Higher crime rate area")

    # Check walkability
    if neighborhood_stats.get("walk_score") and neighborhood_stats["walk_score"] > 80:
        score += 2
        reasoning.append(f"Excellent walkability score of {neighborhood_stats['walk_score']}/100")
    elif neighborhood_stats.get("walk_score") and neighborhood_stats["walk_score"] > 60:
        score += 1
        reasoning.append(f"Good walkability score of {neighborhood_stats['walk_score']}/100")
    else:
        reasoning.append("Limited walkability")

    # Check neighborhood trend
    if market_trends.get("price_trend") and market_trends["price_trend"] > 5:
        score += 2
        reasoning.append(f"Strong price appreciation of {market_trends['price_trend']}% annually")
    elif market_trends.get("price_trend") and market_trends["price_trend"] > 2:
        score += 1
        reasoning.append(f"Moderate price appreciation of {market_trends['price_trend']}% annually")
    else:
        reasoning.append("Flat or declining price trend")

    # Check amenities
    if neighborhood_stats.get("amenities_score") and neighborhood_stats["amenities_score"] > 8:
        score += 2
        reasoning.append("Excellent local amenities")
    elif neighborhood_stats.get("amenities_score") and neighborhood_stats["amenities_score"] > 6:
        score += 1
        reasoning.append("Good local amenities")
    else:
        reasoning.append("Limited local amenities")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(reasoning)
    }


def analyze_property_potential(property_details: dict, comps: list) -> dict:
    """Analyze property potential based on Barbara Corcoran's criteria."""
    if not property_details or not comps:
        return {"score": 0, "max_score": 8, "details": "Insufficient property data"}

    score = 0
    max_score = 8
    reasoning = []

    # Check layout and flow
    if property_details.get("layout_rating") and property_details["layout_rating"] > 8:
        score += 2
        reasoning.append("Excellent layout and flow")
    elif property_details.get("layout_rating") and property_details["layout_rating"] > 6:
        score += 1
        reasoning.append("Good layout with minor issues")
    else:
        reasoning.append("Problematic layout that may limit appeal")

    # Check natural light
    if property_details.get("natural_light") and property_details["natural_light"] > 8:
        score += 2
        reasoning.append("Abundant natural light")
    elif property_details.get("natural_light") and property_details["natural_light"] > 6:
        score += 1
        reasoning.append("Adequate natural light")
    else:
        reasoning.append("Limited natural light")

    # Check outdoor space
    if property_details.get("outdoor_space_rating") and property_details["outdoor_space_rating"] > 8:
        score += 2
        reasoning.append("Excellent outdoor space")
    elif property_details.get("outdoor_space_rating") and property_details["outdoor_space_rating"] > 6:
        score += 1
        reasoning.append("Adequate outdoor space")
    else:
        reasoning.append("Limited or problematic outdoor space")

    # Check renovation potential
    if property_details.get("renovation_potential") and property_details["renovation_potential"] > 8:
        score += 2
        reasoning.append("Excellent renovation potential")
    elif property_details.get("renovation_potential") and property_details["renovation_potential"] > 6:
        score += 1
        reasoning.append("Some renovation potential")
    else:
        reasoning.append("Limited renovation potential")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(reasoning)
    }


def analyze_market_timing(market_trends: dict) -> dict:
    """Analyze market timing based on Barbara Corcoran's criteria."""
    if not market_trends:
        return {"score": 0, "max_score": 6, "details": "Insufficient market data"}

    score = 0
    max_score = 6
    reasoning = []

    # Check inventory levels
    if market_trends.get("inventory_months") and market_trends["inventory_months"] < 3:
        score += 2
        reasoning.append(f"Hot seller's market with only {market_trends['inventory_months']} months of inventory")
    elif market_trends.get("inventory_months") and market_trends["inventory_months"] < 6:
        score += 1
        reasoning.append(f"Balanced market with {market_trends['inventory_months']} months of inventory")
    else:
        reasoning.append(f"Buyer's market with {market_trends.get('inventory_months', 'high')} months of inventory")

    # Check days on market trend
    if market_trends.get("days_on_market_trend") and market_trends["days_on_market_trend"] < 0:
        score += 2
        reasoning.append("Properties selling faster than previous periods")
    elif market_trends.get("days_on_market_trend") and market_trends["days_on_market_trend"] == 0:
        score += 1
        reasoning.append("Stable days on market")
    else:
        reasoning.append("Properties taking longer to sell")

    # Check price to list ratio
    if market_trends.get("price_to_list_ratio") and market_trends["price_to_list_ratio"] > 1:
        score += 2
        reasoning.append(f"Properties selling above asking price ({market_trends['price_to_list_ratio']})")
    elif market_trends.get("price_to_list_ratio") and market_trends["price_to_list_ratio"] > 0.95:
        score += 1
        reasoning.append(f"Properties selling close to asking price ({market_trends['price_to_list_ratio']})")
    else:
        reasoning.append(f"Properties selling below asking price ({market_trends.get('price_to_list_ratio', 'low')})")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(reasoning)
    }


def analyze_unique_selling_points(property_details: dict, comps: list) -> dict:
    """Analyze unique selling points based on Barbara Corcoran's criteria."""
    if not property_details or not comps:
        return {"score": 0, "max_score": 6, "details": "Insufficient property data"}

    score = 0
    max_score = 6
    reasoning = []

    # Check for unique features
    if property_details.get("unique_features") and len(property_details["unique_features"]) > 2:
        score += 2
        reasoning.append(f"Multiple unique features: {', '.join(property_details['unique_features'][:3])}")
    elif property_details.get("unique_features") and len(property_details["unique_features"]) > 0:
        score += 1
        reasoning.append(f"Some unique features: {', '.join(property_details['unique_features'])}")
    else:
        reasoning.append("No standout unique features")

    # Check for premium finishes
    if property_details.get("finish_quality") and property_details["finish_quality"] > 8:
        score += 2
        reasoning.append("Premium finishes throughout")
    elif property_details.get("finish_quality") and property_details["finish_quality"] > 6:
        score += 1
        reasoning.append("Good quality finishes")
    else:
        reasoning.append("Basic or dated finishes")

    # Check for views or special location
    if property_details.get("view_rating") and property_details["view_rating"] > 8:
        score += 2
        reasoning.append("Exceptional views or location advantage")
    elif property_details.get("view_rating") and property_details["view_rating"] > 6:
        score += 1
        reasoning.append("Pleasant views or good location advantage")
    else:
        reasoning.append("No special views or location advantage")

    return {
        "score": score,
        "max_score": max_score,
        "details": "; ".join(reasoning)
    }


def generate_corcoran_output(
    property_id: str,
    analysis_data: dict,
    state: AgentState,
    agent_id: str = "barbara_corcoran_agent",
) -> BarbaraCorcoran:
    """Get investment decision from LLM with Barbara Corcoran's principles"""
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are Barbara Corcoran, the Queen of NYC Real Estate and Shark Tank investor. Analyze real estate opportunities using my proven methodology:

                MY CORE PRINCIPLES:
                1. Location is Everything: "Location, location, location" isn't just a saying - it's the foundation of smart real estate investing.
                2. Market Timing: I built my empire by recognizing market trends before others did.
                3. Property Potential: I can walk into any property and immediately see what it could become.
                4. People Skills: Real estate is a people business - understanding what buyers want is crucial.
                5. Marketing Genius: The best property in the world won't sell itself - presentation matters.

                MY INVESTMENT CRITERIA:
                1. Neighborhood Trajectory: Is this area improving or declining? What are the signs?
                2. Comparable Properties: How does this property stack up against recent sales?
                3. Unique Selling Points: What makes this property special or gives it an edge?
                4. Buyer Psychology: Who is the ideal buyer for this property and what do they value?
                5. Value-Add Potential: Can simple changes dramatically increase the property's value?

                MY LANGUAGE & STYLE:
                - Straightforward and no-nonsense
                - Use colorful analogies from my experience
                - Reference my humble beginnings and self-made success
                - Emphasize gut feelings and instinct
                - Show enthusiasm for properties with clear potential
                - Be brutally honest about properties with fatal flaws

                CONFIDENCE LEVELS:
                - 90-100%: Prime location with clear upside and minimal risk
                - 70-89%: Good location with some value-add potential
                - 50-69%: Average property that needs the right buyer/strategy
                - 30-49%: Challenging property with significant issues
                - 10-29%: Poor investment with too many negatives to overcome

                Remember: I started with a $1,000 loan and built a $66 million real estate empire. I look for properties where others miss the potential, but I never ignore red flags or overvalue mediocre opportunities.
                """,
            ),
            (
                "human",
                """Analyze this real estate opportunity for property {property_id}:

                COMPREHENSIVE ANALYSIS DATA:
                {analysis_data}

                Please provide your investment decision in exactly this JSON format:
                {{
                  "signal": "buy" | "pass" | "hold",
                  "confidence": float between 0 and 100,
                  "reasoning": "string with your detailed Barbara Corcoran-style analysis"
                }}

                In your reasoning, be specific about:
                1. Your assessment of the location and neighborhood trajectory
                2. The property's potential and unique selling points
                3. Current market timing and conditions
                4. Who the ideal buyer would be and what they'd value
                5. Any value-add opportunities you see
                6. Any red flags or deal-breakers

                Write as Barbara Corcoran would speak - plainly, with conviction, and with specific references to the data provided.
                """,
            ),
        ]
    )

    prompt = template.invoke({"analysis_data": json.dumps(analysis_data, indent=2), "property_id": property_id})

    # Default fallback signal in case parsing fails
    def create_default_barbara_corcoran_signal():
        return BarbaraCorcoran(signal="pass", confidence=0.0, reasoning="Error in analysis, defaulting to pass")

    return call_llm(
        prompt=prompt,
        pydantic_model=BarbaraCorcoran,
        agent_name=agent_id,
        state=state,
        default_factory=create_default_barbara_corcoran_signal,
    )