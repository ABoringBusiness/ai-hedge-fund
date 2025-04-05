# AI Hedge Fund TypeScript SDK

A TypeScript SDK for interacting with the AI Hedge Fund application.

## Installation

```bash
npm install ai-hedge-fund-sdk
```

## Usage

```typescript
import { AIHedgeFundClient } from 'ai-hedge-fund-sdk';

// Create a client
const client = new AIHedgeFundClient({
  apiKey: 'your-api-key', // Optional
  baseUrl: 'http://your-api-url', // Optional, defaults to http://localhost:8000
});

// Run the hedge fund
async function runHedgeFund() {
  try {
    const result = await client.run({
      tickers: ['AAPL', 'MSFT', 'GOOGL'],
      startDate: '2023-01-01',
      endDate: '2023-03-31',
      initialCash: 100000,
      showReasoning: true,
      selectedAnalysts: ['warren_buffett', 'ben_graham'],
      modelName: 'gpt-4o',
      modelProvider: 'OpenAI',
    });
    
    console.log('Trade decisions:', result.decisions);
    console.log('Analyst signals:', result.analyst_signals);
  } catch (error) {
    console.error('Error running hedge fund:', error);
  }
}

// Get available analysts
async function getAnalysts() {
  try {
    const analysts = await client.getAnalysts();
    console.log('Available analysts:', analysts);
  } catch (error) {
    console.error('Error getting analysts:', error);
  }
}

// Get available models
async function getModels() {
  try {
    const models = await client.getModels();
    console.log('Available models:', models);
  } catch (error) {
    console.error('Error getting models:', error);
  }
}

runHedgeFund();
```

## API Reference

### AIHedgeFundClient

The main client for interacting with the AI Hedge Fund API.

#### Constructor

```typescript
new AIHedgeFundClient(config?: AIHedgeFundConfig)
```

Configuration options:
- `apiKey`: Optional API key for authentication
- `baseUrl`: Base URL of the API (default: 'http://localhost:8000')
- `timeout`: Request timeout in milliseconds (default: 30000)

#### Methods

##### run(options: RunOptions): Promise<HedgeFundResponse>

Run the hedge fund with the specified options.

Parameters:
- `options`: RunOptions object with the following properties:
  - `tickers`: Array of stock ticker symbols
  - `startDate`: Optional start date (YYYY-MM-DD)
  - `endDate`: Optional end date (YYYY-MM-DD)
  - `initialCash`: Optional initial cash amount (default: 100000)
  - `marginRequirement`: Optional margin requirement (default: 0)
  - `showReasoning`: Optional flag to show reasoning (default: false)
  - `selectedAnalysts`: Optional array of analyst names
  - `modelName`: Optional LLM model name (default: 'gpt-4o')
  - `modelProvider`: Optional LLM provider (default: 'OpenAI')

Returns:
- Promise resolving to a HedgeFundResponse object

##### getAnalysts(): Promise<string[]>

Get a list of available analysts.

Returns:
- Promise resolving to an array of analyst names

##### getModels(): Promise<string[]>

Get a list of available LLM models.

Returns:
- Promise resolving to an array of model names

## Types

The SDK exports the following TypeScript types:

- `AIHedgeFundConfig`: Configuration options for the client
- `Portfolio`: Portfolio information
- `Position`: Stock position information
- `RealizedGains`: Realized gains information
- `TradeDecision`: Trade decision information
- `AnalystSignal`: Analyst signal information
- `HedgeFundResponse`: Response from running the hedge fund
- `RunOptions`: Options for running the hedge fund