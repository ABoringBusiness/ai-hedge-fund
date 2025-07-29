# AI Real Estate Mastermind

This is a proof of concept for an AI-powered real estate investment platform. The goal of this project is to explore the use of AI to make residential real estate investment decisions. This project is for **educational** purposes only and is not intended for real investment advice.

## System Overview

This system employs several agents working together, each representing a famous real estate personality with their unique investment philosophy:

1. **Barbara Corcoran Agent** - The Queen of NYC Real Estate, focuses on location, market trends, and property potential
2. **Robert Kiyosaki Agent** - Rich Dad Poor Dad author, analyzes cash flow and passive income opportunities
3. **Grant Cardone Agent** - The 10X Real Estate Investor, seeks large multifamily properties with scale advantages
4. **Brandon Turner Agent** - BiggerPockets expert, focuses on house hacking and creative financing strategies
5. **Chip & Joanna Gaines Agent** - Fixer Upper specialists, evaluates renovation potential and design value-add
6. **Scott McGillivray Agent** - Income Property host, specializes in rental property analysis and tenant management
7. **Ryan Serhant Agent** - Luxury market specialist, focuses on high-end properties and premium positioning
8. **Nicole Curtis Agent** - Rehab Addict, specializes in historic properties and restoration opportunities
9. **Dave Ramsey Agent** - Conservative financial advisor, emphasizes debt-free investing and risk management
10. **Ben Mallah Agent** - Self-made investor, looks for distressed commercial properties with turnaround potential
11. **Graham Stephan Agent** - YouTube investor, focuses on house hacking and low-cost entry strategies
12. **Cash Flow Analyst** - Calculates rental income potential and operating expenses
13. **Market Trend Analyst** - Analyzes neighborhood growth patterns and appreciation potential
14. **Renovation Analyst** - Evaluates property condition and estimates renovation costs and ROI
15. **Risk Manager** - Calculates risk metrics and sets investment limits
16. **Portfolio Manager** - Makes final investment decisions and generates recommendations

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real investment or financial decisions
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a licensed real estate professional for investment decisions
- Past performance does not indicate future results

By using this software, you agree to use it solely for learning purposes.

## How to Install

Before you can run the AI Real Estate Mastermind, you'll need to install it and set up your API keys. These steps are common to both the full-stack web application and command line interface.

### 1. Clone the Repository

```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

### 2. Set Up Your API Keys

Create a `.env` file for your API keys:
```bash
# Create .env file for your API keys (in the root directory)
cp .env.example .env
```

Open and edit the `.env` file to add your API keys:
```bash
# For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
OPENAI_API_KEY=your-openai-api-key

# For running LLMs hosted by groq (deepseek, llama3, etc.)
GROQ_API_KEY=your-groq-api-key

# For getting real estate data to power the mastermind
REAL_ESTATE_API_KEY=your-real-estate-api-key
```

**Important**: You must set at least one LLM API key (`OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`, or `DEEPSEEK_API_KEY`) for the mastermind to work.

## How to Run

### ⌨️ Command Line Interface

For users who prefer working with command line tools, you can run the AI Real Estate Mastermind directly via terminal. This approach offers more granular control and is useful for automation, scripting, and integration purposes.

Choose one of the following installation methods:

#### Using Poetry

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

#### Using Docker

1. Make sure you have Docker installed on your system. If not, you can download it from [Docker's official website](https://www.docker.com/get-started).

2. Navigate to the docker directory:
```bash
cd docker
```

3. Build the Docker image:
```bash
# On Linux/Mac:
./run.sh build

# On Windows:
run.bat build
```

#### Running the AI Real Estate Mastermind (with Poetry)
```bash
poetry run python src/main.py --mode real_estate --property_ids 123,456,789
```

#### Running the AI Real Estate Mastermind (with Docker)
```bash
# Navigate to the docker directory first
cd docker

# On Linux/Mac:
./run.sh --mode real_estate --property_ids 123,456,789 main

# On Windows:
run.bat --mode real_estate --property_ids 123,456,789 main
```

You can also specify a `--show-reasoning` flag to print the reasoning of each agent to the console.

```bash
# With Poetry:
poetry run python src/main.py --mode real_estate --property_ids 123,456,789 --show-reasoning

# With Docker (from docker/ directory):
# On Linux/Mac:
./run.sh --mode real_estate --property_ids 123,456,789 --show-reasoning main

# On Windows:
run.bat --mode real_estate --property_ids 123,456,789 --show-reasoning main
```

### 🖥️ Web Application

The new way to run the AI Real Estate Mastermind is through our web application that provides a user-friendly interface. **This is recommended for most users, especially those who prefer visual interfaces over command line tools.**

#### For Mac/Linux:
```bash
cd app && ./run.sh --mode real_estate
```

If you get a "permission denied" error, run this first:
```bash
cd app && chmod +x run.sh && ./run.sh --mode real_estate
```

#### For Windows:
```bash
# Go to /app directory
cd app

# Run the app
\.run.bat --mode real_estate
```

**That's it!** These scripts will:
1. Check for required dependencies (Node.js, Python, Poetry)
2. Install all dependencies automatically  
3. Start both frontend and backend services
4. **Automatically open your web browser** to the application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

**Important**: Please keep your pull requests small and focused. This will make it easier to review and merge.

## Feature Requests

If you have a feature request, please open an [issue](https://github.com/virattt/ai-hedge-fund/issues) and make sure it is tagged with `enhancement`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.