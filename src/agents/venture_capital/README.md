# Venture Capital Analyst

The Venture Capital Analyst is an AI agent specialized in evaluating startups and early-stage companies for potential investment. This agent focuses on high-growth potential companies, innovative technologies, and emerging markets.

## Capabilities

The Venture Capital Analyst can:

1. Assess founding teams and their capabilities
2. Evaluate product-market fit and technology differentiation
3. Analyze market size, growth potential, and competitive landscape
4. Review business models and go-to-market strategies
5. Estimate valuation, funding requirements, and potential returns

## Usage

To use the Venture Capital Analyst, you need to provide data about startups in the state:

```python
state["data"]["startups"] = [
    {
        "name": "Startup X",
        "industry": "FinTech",
        "founded": 2022,
        "stage": "Seed",
        "funding": "$2M",
        "team_size": 15,
        "founders": [
            {"name": "Jane Doe", "background": "Ex-Google, Stanford CS"},
            {"name": "John Smith", "background": "Serial entrepreneur, MIT"}
        ],
        "product": "AI-powered personal finance platform",
        "traction": "10,000 beta users, 25% MoM growth",
        "description": "Building the next generation of...",
        # Additional data as needed
    },
    # More startups...
]
```

The analyst will then process this data and provide investment recommendations.

## Integration

The Venture Capital Analyst is integrated into the AI Hedge Fund workflow and can be selected as one of the analysts when running the application.

## Output

The analyst produces forward-looking analysis for each startup, including:

- Founding team assessment
- Product and technology evaluation
- Market opportunity analysis
- Traction and growth metrics review
- Investment recommendation with risk/return profile

This output is stored in the state and can be used by other agents in the workflow, particularly the Portfolio Management agent for making investment decisions.