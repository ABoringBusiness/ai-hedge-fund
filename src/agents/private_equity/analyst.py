from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from src.llm.models import get_llm_model
from src.graph.state import AgentState
from src.utils.progress import progress

PRIVATE_EQUITY_SYSTEM_PROMPT = """You are a Private Equity Analyst AI agent. Your role is to analyze private companies for potential investment opportunities.

Your expertise includes:
1. Evaluating company financials and growth metrics
2. Assessing management teams and their track records
3. Analyzing market dynamics and competitive positioning
4. Identifying potential value creation opportunities
5. Estimating exit strategies and potential returns

For each company you analyze, provide:
- A comprehensive analysis of the business model and market position
- Key financial metrics and growth trajectory
- Strengths and weaknesses of the management team
- Potential risks and mitigating factors
- Valuation assessment and investment recommendation

Your output should be structured, data-driven, and actionable for investment decision-making.
"""

def private_equity_analyst_agent(state: AgentState) -> AgentState:
    """Private Equity Analyst agent that evaluates private companies for investment opportunities."""
    progress.update("Running Private Equity Analyst...")
    
    # Get the LLM model based on metadata
    llm = get_llm_model(
        model_name=state["metadata"].get("model_name", "gpt-4o"),
        model_provider=state["metadata"].get("model_provider", "OpenAI"),
    )
    
    # Extract relevant data from state
    companies = state["data"].get("private_companies", [])
    if not companies:
        # If no private companies data is provided, return state unchanged
        progress.update("No private companies data provided. Skipping Private Equity Analyst.")
        return state
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PRIVATE_EQUITY_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "Analyze the following private companies for potential investment: {companies}. Consider their financials, management, market position, and growth potential."),
        ]
    )
    
    # Create the chain
    chain = prompt | llm | StrOutputParser()
    
    # Run the chain
    response = chain.invoke(
        {
            "messages": state["messages"],
            "companies": companies,
        }
    )
    
    # Update the state with the analysis
    state["messages"].append(HumanMessage(content="Please analyze these private companies for potential investment."))
    state["messages"].append(AIMessage(content=response))
    
    # Store the analysis in the state data
    if "analyst_signals" not in state["data"]:
        state["data"]["analyst_signals"] = {}
    
    state["data"]["analyst_signals"]["private_equity_analyst"] = {
        "analysis": response,
        "companies": companies,
    }
    
    progress.update("Private Equity Analyst completed analysis.")
    return state