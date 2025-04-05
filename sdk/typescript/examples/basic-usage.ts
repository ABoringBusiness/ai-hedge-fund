import { AIHedgeFundClient } from '../src';

// Create a client
const client = new AIHedgeFundClient({
  baseUrl: 'http://localhost:8000',
});

async function main() {
  try {
    // Get available analysts
    const analysts = await client.getAnalysts();
    console.log('Available analysts:', analysts);

    // Get available models
    const models = await client.getModels();
    console.log('Available models:', models);

    // Run the hedge fund
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
    
    console.log('Trade decisions:');
    result.decisions.forEach(decision => {
      console.log(`${decision.action} ${decision.quantity} shares of ${decision.ticker}`);
      if (decision.reasoning) {
        console.log(`Reasoning: ${decision.reasoning}`);
      }
      console.log('---');
    });
    
    console.log('Analyst signals:');
    Object.entries(result.analyst_signals).forEach(([analyst, signals]) => {
      console.log(`${analyst}:`);
      signals.forEach(signal => {
        console.log(`  ${signal.ticker}: ${signal.signal} (Confidence: ${signal.confidence})`);
        if (signal.reasoning) {
          console.log(`  Reasoning: ${signal.reasoning}`);
        }
      });
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

main();