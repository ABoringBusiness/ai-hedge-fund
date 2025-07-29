import sys

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from colorama import Fore, Style, init
import questionary
from src.graph.state import AgentState
from src.utils.display import print_real_estate_output
from src.utils.real_estate_analysts import REAL_ESTATE_ANALYST_ORDER, get_real_estate_analyst_nodes
from src.utils.progress import progress
from src.llm.models import LLM_ORDER, OLLAMA_LLM_ORDER, get_model_info, ModelProvider

import argparse
from datetime import datetime
import json

# Load environment variables from .env file
load_dotenv()

init(autoreset=True)


def parse_real_estate_response(response):
    """Parses a JSON string and returns a dictionary."""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error parsing response: {response}{Style.RESET_ALL}")
        return {}


def create_real_estate_graph(agents_to_include=None, use_ollama=False):
    """Creates a graph of agents for real estate analysis."""
    # Initialize the graph
    workflow = StateGraph(AgentState)

    # Get the analyst nodes
    analyst_nodes = get_real_estate_analyst_nodes()

    # Filter the nodes if agents_to_include is specified
    if agents_to_include:
        analyst_nodes = {k: v for k, v in analyst_nodes.items() if k in agents_to_include}

    # Add all the analyst nodes to the graph
    for node_name, agent_func in analyst_nodes.values():
        workflow.add_node(node_name, agent_func)

    # Connect all analyst nodes to the portfolio manager
    for node_name, _ in analyst_nodes.values():
        workflow.add_edge(node_name, END)

    return workflow


def main():
    """Main function to run the AI Real Estate Mastermind."""
    parser = argparse.ArgumentParser(description="AI Real Estate Mastermind")
    parser.add_argument(
        "--property_ids",
        type=str,
        help="Comma-separated list of property IDs to analyze",
        required=True,
    )
    parser.add_argument(
        "--show-reasoning",
        action="store_true",
        help="Show the reasoning of each agent",
    )
    parser.add_argument(
        "--ollama",
        action="store_true",
        help="Use Ollama for local LLM inference",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model to use for LLM inference",
        default=None,
    )
    parser.add_argument(
        "--model-provider",
        type=str,
        help="Model provider to use for LLM inference",
        choices=[provider.value for provider in ModelProvider],
        default=None,
    )
    parser.add_argument(
        "--agents",
        type=str,
        help="Comma-separated list of agents to include",
        default=None,
    )

    args = parser.parse_args()

    # Parse property IDs
    property_ids = args.property_ids.split(",")

    # Parse agents to include
    agents_to_include = args.agents.split(",") if args.agents else None

    # Set up the model
    model_name = args.model
    model_provider = args.model_provider

    if args.ollama:
        if not model_name:
            # If no model is specified, use the first one in the list
            model_name = OLLAMA_LLM_ORDER[0][0]
        model_provider = ModelProvider.OLLAMA.value
        ensure_ollama_and_model(model_name)
    else:
        if not model_name:
            # If no model is specified, use the first one in the list
            model_name = LLM_ORDER[0][0]
        if not model_provider:
            # If no provider is specified, use the default for the model
            model_info = get_model_info(model_name)
            model_provider = model_info["provider"].value if model_info else ModelProvider.OPENAI.value

    # Create the graph
    graph = create_real_estate_graph(agents_to_include, args.ollama)
    graph = graph.compile()

    # Initialize the state
    state = {
        "messages": [],
        "data": {
            "properties": property_ids,
            "analyst_signals": {},
        },
        "metadata": {
            "show_reasoning": args.show_reasoning,
            "model_name": model_name,
            "model_provider": model_provider,
        },
    }

    # Run the graph
    print(f"{Fore.GREEN}Running AI Real Estate Mastermind...{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Analyzing properties: {', '.join(property_ids)}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Using model: {model_name} ({model_provider}){Style.RESET_ALL}")
    print()

    # Register a progress handler to print updates
    def progress_handler(agent_name, property_id, status, analysis=None, timestamp=None):
        if property_id:
            print(f"{Fore.YELLOW}{agent_name}: {status} for property {property_id}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}{agent_name}: {status}{Style.RESET_ALL}")

    progress.register_handler(progress_handler)

    try:
        # Run the graph
        result = graph.invoke(state)

        # Print the results
        if result and result.get("messages"):
            final_message = result["messages"][-1]
            if hasattr(final_message, "content"):
                decisions = parse_real_estate_response(final_message.content)
                print_real_estate_output(decisions, result["data"]["analyst_signals"])
            else:
                print(f"{Fore.RED}Error: Final message has no content{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: No results returned from the graph{Style.RESET_ALL}")
    finally:
        # Unregister the progress handler
        progress.unregister_handler(progress_handler)


if __name__ == "__main__":
    main()