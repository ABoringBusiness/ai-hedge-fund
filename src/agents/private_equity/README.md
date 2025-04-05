# Private Equity Analyst

The Private Equity Analyst is an AI agent specialized in evaluating private companies for potential investment opportunities. This agent focuses on analyzing companies that are not publicly traded, looking for value creation opportunities and potential returns.

## Capabilities

The Private Equity Analyst can:

1. Evaluate company financials and growth metrics
2. Assess management teams and their track records
3. Analyze market dynamics and competitive positioning
4. Identify potential value creation opportunities
5. Estimate exit strategies and potential returns

## Usage

To use the Private Equity Analyst, you need to provide data about private companies in the state:

```python
state["data"]["private_companies"] = [
    {
        "name": "Company A",
        "industry": "Software",
        "founded": 2015,
        "revenue": "$50M",
        "growth_rate": "30%",
        "employees": 200,
        "funding": "$25M Series B",
        "description": "Enterprise SaaS platform for...",
        # Additional data as needed
    },
    # More companies...
]
```

The analyst will then process this data and provide investment recommendations.

## Integration

The Private Equity Analyst is integrated into the AI Hedge Fund workflow and can be selected as one of the analysts when running the application.

## Output

The analyst produces structured analysis for each company, including:

- Business model and market position assessment
- Financial metrics and growth trajectory analysis
- Management team evaluation
- Risk assessment and mitigation strategies
- Valuation and investment recommendations

This output is stored in the state and can be used by other agents in the workflow, particularly the Portfolio Management agent for making investment decisions.