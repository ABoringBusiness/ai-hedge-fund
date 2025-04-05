from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from src.llm.models import get_llm_model
from src.graph.state import AgentState
from src.utils.progress import progress

VC_SYSTEM_PROMPT = """You are a Venture Capital Analyst AI agent. Your role is to evaluate startups and early-stage companies for potential investment.

Your expertise includes:
1. Assessing founding teams and their capabilities
2. Evaluating product-market fit and technology differentiation
3. Analyzing market size, growth potential, and competitive landscape
4. Reviewing business models and go-to-market strategies
5. Estimating valuation, funding requirements, and potential returns

For each startup you analyze, provide:
- An assessment of the founding team and their background
- Analysis of the product/service and its unique value proposition
- Evaluation of the market opportunity and competitive positioning
- Review of traction metrics and growth indicators
- Investment recommendation with potential risks and returns

Your output should be forward-looking, focused on growth potential, and tailored for early-stage investment decisions.
"""

def venture_capital_analyst_agent(state: AgentState) -> AgentState:
    """Venture Capital Analyst agent that evaluates startups for investment opportunities."""
    progress.update("Running Venture Capital Analyst...")
    
    # Get the LLM model based on metadata
    llm = get_llm_model(
        model_name=state["metadata"].get("model_name", "gpt-4o"),
        model_provider=state["metadata"].get("model_provider", "OpenAI"),
    )
    
    # Extract relevant data from state
    startups = state["data"].get("startups", [])
    if not startups:
        # If no startup data is provided, return state unchanged
        progress.update("No startup data provided. Skipping Venture Capital Analyst.")
        return state
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", VC_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "Analyze the following startups for potential investment: {startups}. Consider their team, product, market, traction, and growth potential."),
        ]
    )
    
    # Create the chain
    chain = prompt | llm | StrOutputParser()
    
    # Run the chain
    response = chain.invoke(
        {
            "messages": state["messages"],
            "startups": startups,
        }
    )
    
    # Update the state with the analysis
    state["messages"].append(HumanMessage(content="Please analyze these startups for potential investment."))
    state["messages"].append(AIMessage(content=response))
    
    # Store the analysis in the state data
    if "analyst_signals" not in state["data"]:
        state["data"]["analyst_signals"] = {}
    
    state["data"]["analyst_signals"]["venture_capital_analyst"] = {
        "analysis": response,
        "startups": startups,
    }
    
    progress.update("Venture Capital Analyst completed analysis.")
    return state